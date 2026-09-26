"""Sightings ingest: resolve taxon keys, fetch GBIF and iNaturalist occurrences for a region's
woodland cells, filter for quality, and store per-cell counts.

    uv run python -m api.sightings.ingest resolve-taxa   # check config/sightings.yaml against
                                                          # each API's current taxonomy
    uv run python -m api.sightings.ingest fetch          # GBIF history + recent iNaturalist
    uv run python -m api.sightings.ingest profile        # counts, licenses, town-proximity bias

Raw responses are cached under ``$DATA_DIR/raw/{gbif,inaturalist}/<region>/`` (see
``api.sightings.http``); delete a taxon's cache directory to re-fetch it. The normalized table
lives in ``$DATA_DIR/sightings/<region>/`` (``api.sightings.store``). Every command is safe to
re-run.
"""

import argparse
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pandas as pd

from api.grid.places import read_istat_localities
from api.grid.region import load_region
from api.grid.sources import data_dir, load_sources
from api.grid.sources import fetch as download
from api.sightings.config import SightingsConfig, inaturalist_place_id, load_sightings_config
from api.sightings.filters import deduplicate_inaturalist, drop_low_quality, flag_near_localities
from api.sightings.gbif import (
    OCCURRENCE_COLUMNS,
    OccurrenceRequest,
    TaxonMatch,
    match_url,
    parse_occurrences,
    parse_taxon_match,
)
from api.sightings.gbif import (
    is_last_page as gbif_is_last_page,
)
from api.sightings.http import JsonClient, fetch_pages
from api.sightings.inaturalist import (
    OBSERVATION_COLUMNS,
    ObservationRequest,
    parse_observations,
)
from api.sightings.inaturalist import (
    is_last_page as inaturalist_is_last_page,
)
from api.sightings.store import RECORD_COLUMNS, SightingsStore, assign_cells

Log = Callable[[str], None]

COMMON_COLUMNS = [
    "source",
    "record_id",
    "species",
    "event_date",
    "lat",
    "lon",
    "coordinate_uncertainty_m",
    "basis_of_record",
    "license",
    "obscured",
    "fetched_at",
]


# --- resolve taxon keys --------------------------------------------------------------------


def resolve_taxa(
    client: JsonClient, config: SightingsConfig, log: Log = print
) -> dict[str, TaxonMatch]:
    """Look up every configured scientific name against GBIF's species match, and warn about any
    that no longer resolve exactly, or now point at a different key (a backbone change)."""
    matches = {}
    for species in config.species.values():
        for taxon in species.taxa:
            payload = client.get(
                match_url(config.gbif.match_endpoint, taxon.scientific_name, taxon.rank)
            )
            match = parse_taxon_match(taxon.scientific_name, payload)
            matches[taxon.scientific_name] = match
            if not match.is_exact:
                log(f"WARNING: {taxon.scientific_name} did not match exactly: {match}")
            elif match.resolved_key != taxon.gbif_taxon_key:
                log(
                    f"WARNING: {taxon.scientific_name} now resolves to {match.resolved_key}, "
                    f"config has {taxon.gbif_taxon_key} (update config/sightings.yaml)"
                )
            else:
                log(f"{taxon.scientific_name}: {match.resolved_key} (unchanged)")
    return matches


# --- normalize into the common schema ---------------------------------------------------------


def normalize_gbif(rows: pd.DataFrame, config: SightingsConfig) -> pd.DataFrame:
    """GBIF rows in the common schema, minus species a genus-level taxon excludes."""
    excluded = [
        species_key in config.excluded_gbif_species(taxon_key)
        for taxon_key, species_key in zip(rows["taxon_key"], rows["species_key"], strict=True)
    ]
    normalized = rows[~pd.Series(excluded, index=rows.index, dtype=bool)].copy()
    normalized["species"] = normalized["taxon_key"].map(config.species_of)
    normalized["obscured"] = False
    return normalized[[*COMMON_COLUMNS, "inaturalist_observation_id"]].reset_index(drop=True)


def normalize_inaturalist(rows: pd.DataFrame, config: SightingsConfig) -> pd.DataFrame:
    normalized = rows.copy()
    normalized["species"] = normalized["taxon_id"].map(config.species_of_inaturalist)
    normalized["basis_of_record"] = None
    return normalized[COMMON_COLUMNS]


def stale_gbif_record_ids(fetched: pd.DataFrame, stored: pd.DataFrame) -> list[str]:
    """GBIF records fetched this run that did not make it into the store, so any copy a looser
    earlier run stored must go."""
    return sorted(set(fetched["record_id"]) - set(stored["record_id"]))


# --- fetch ---------------------------------------------------------------------------------


def fetch_gbif(
    client: JsonClient,
    config: SightingsConfig,
    bbox: tuple[float, float, float, float],
    cache_root: Path,
    fetched_at: datetime,
    log: Log = print,
    *,
    cache_scope: str,
) -> pd.DataFrame:
    """GBIF occurrence records for every configured taxon, across a region's bbox.

    Cached under ``gbif/<cache_scope>/<taxon>``: the pages hold one bbox's records, so each region
    keeps its own (a shared cache would hand a second region the first one's pages).
    """
    frames = []
    for species in config.species.values():
        for taxon in species.taxa:
            template = OccurrenceRequest(
                endpoint=config.gbif.endpoint,
                taxon_key=taxon.gbif_taxon_key,
                bbox_wgs84=bbox,
                page_size=config.gbif.page_size,
            )
            cache_dir = cache_root / "gbif" / cache_scope / str(taxon.gbif_taxon_key)
            pages = fetch_pages(
                client,
                lambda offset, t=template: t.at_offset(offset).url(),
                cache_dir,
                config.gbif.page_size,
                gbif_is_last_page,
            )
            rows = parse_occurrences(pages, taxon.gbif_taxon_key, fetched_at)
            log(f"gbif {taxon.scientific_name}: {len(rows)} records")
            frames.append(rows)
    if not frames:
        return pd.DataFrame(columns=OCCURRENCE_COLUMNS)
    return pd.concat(frames, ignore_index=True)


def fetch_inaturalist(
    client: JsonClient,
    config: SightingsConfig,
    since: date,
    cache_root: Path,
    fetched_at: datetime,
    log: Log = print,
    *,
    place_id: int,
    cache_scope: str,
) -> pd.DataFrame:
    """The most recent iNaturalist observations in ``place_id`` for every configured taxon.

    Cached under ``<cache_scope>/<taxon>/<since>``, one scope per region because each region asks
    for its own place. ``since`` moves forward with every run (``today -
    recent_days``), so a cache directory is never reused across two different windows, and a
    same-day re-run that hits an already-complete cache is caught by tomorrow's overlapping
    window instead of re-fetching mid-day.
    """
    frames = []
    for species in config.species.values():
        for taxon in species.taxa:
            template = ObservationRequest(
                endpoint=config.inaturalist.endpoint,
                taxon_id=taxon.inaturalist_taxon_id,
                place_id=place_id,
                since=since,
                quality_grades=config.inaturalist.quality_grades,
                page_size=config.inaturalist.page_size,
            )
            page_size = config.inaturalist.page_size

            def url_for_offset(
                offset: int, t: ObservationRequest = template, size: int = page_size
            ) -> str:
                return t.at_page(offset // size + 1).url()

            cache_dir = (
                cache_root
                / "inaturalist"
                / cache_scope
                / str(taxon.inaturalist_taxon_id)
                / since.isoformat()
            )
            pages = fetch_pages(
                client, url_for_offset, cache_dir, page_size, inaturalist_is_last_page
            )
            rows = parse_observations(pages, taxon.inaturalist_taxon_id, fetched_at)
            log(f"inaturalist {taxon.scientific_name}: {len(rows)} records")
            frames.append(rows)
    if not frames:
        return pd.DataFrame(columns=OBSERVATION_COLUMNS)
    return pd.concat(frames, ignore_index=True)


# --- the full pipeline: fetch -> dedup -> filter -> flag -> assign -> store ---------------------


@dataclass
class FetchSummary:
    gbif_records: int = 0
    inaturalist_records: int = 0
    deduplicated: int = 0
    kept: int = 0
    stored: int = 0
    filter_counts: dict = field(default_factory=dict)


def run_fetch(
    client: JsonClient,
    config: SightingsConfig,
    region_id: str,
    root: Path | None = None,
    today: date | None = None,
    log: Log = print,
) -> FetchSummary:
    root = root or data_dir()
    region = load_region(region_id)
    today = today or datetime.now(UTC).date()
    fetched_at = datetime.now(UTC)
    cache_root = root / "raw"

    gbif_raw = fetch_gbif(
        client, config, region.bbox_wgs84, cache_root, fetched_at, log, cache_scope=region.id
    )
    since = today - timedelta(days=config.inaturalist.recent_days)
    inaturalist_raw = fetch_inaturalist(
        client,
        config,
        since,
        cache_root,
        fetched_at,
        log,
        place_id=inaturalist_place_id(region, config),
        cache_scope=region.id,
    )

    gbif_rows = normalize_gbif(gbif_raw, config)
    inaturalist_rows = normalize_inaturalist(inaturalist_raw, config)
    deduplicated = deduplicate_inaturalist(gbif_rows, inaturalist_rows)
    log(f"iNaturalist: {len(inaturalist_rows)} fetched, {len(deduplicated)} not already in GBIF")

    combined = pd.concat(
        [gbif_rows[COMMON_COLUMNS], deduplicated[COMMON_COLUMNS]], ignore_index=True
    )
    kept, filter_counts = drop_low_quality(
        combined,
        config.quality.max_coordinate_uncertainty_m,
        config.quality.exclude_basis_of_record,
    )
    log(f"quality filters: {filter_counts}")

    localities_archive = download(
        load_sources()["istat_localities"].download["url"],
        cache_root / "istat" / "LocalitaPuntuali_21.zip",
    )
    margin = 0.1
    lon_min, lat_min, lon_max, lat_max = region.bbox_wgs84
    localities = read_istat_localities(
        localities_archive,
        (lon_min - margin, lat_min - margin, lon_max + margin, lat_max + margin),
        region.grid.crs,
    )
    town_flags = flag_near_localities(kept, localities, config.quality.town_centroid_distance_m)
    kept = kept.assign(obscured=kept["obscured"].fillna(False) | town_flags)

    cells = pd.read_parquet(
        root / "grid" / region.id / "cells.parquet", columns=["cell_id", "woodland"]
    )
    assigned = assign_cells(kept, cells, crs=region.grid.crs, cell_size_m=region.grid.cell_size_m)
    stored_rows = assigned.rename(columns={"event_date": "date"})[RECORD_COLUMNS]

    store = SightingsStore(root / "sightings" / region.id)
    store.upsert(stored_rows)
    stale = stale_gbif_record_ids(gbif_raw, stored_rows[stored_rows["source"] == "gbif"])
    removed = store.remove("gbif", stale)
    if removed:
        log(f"removed {removed} previously stored GBIF records the filters now reject")
    write_meta(config, store, region.id)
    off_grid = len(kept) - len(stored_rows)
    log(f"stored: {len(stored_rows)} sightings ({off_grid} off the woodland grid)")

    return FetchSummary(
        gbif_records=len(gbif_rows),
        inaturalist_records=len(inaturalist_rows),
        deduplicated=len(deduplicated),
        kept=len(kept),
        stored=len(stored_rows),
        filter_counts=vars(filter_counts),
    )


def write_meta(config: SightingsConfig, store: SightingsStore, region: str) -> Path:
    """``meta.json`` next to the sightings table: every taxon, the quality thresholds applied, and
    each credited source's attribution (PRD → Licensing: every source is credited in the app)."""
    sources = load_sources()
    meta = {
        "region": region,
        "written_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "species": {
            key: {
                "common_name": species.common_name,
                "taxa": [
                    {
                        "scientific_name": taxon.scientific_name,
                        "gbif_taxon_key": taxon.gbif_taxon_key,
                        "inaturalist_taxon_id": taxon.inaturalist_taxon_id,
                    }
                    for taxon in species.taxa
                ],
            }
            for key, species in config.species.items()
        },
        "quality": {
            "max_coordinate_uncertainty_m": config.quality.max_coordinate_uncertainty_m,
            "town_centroid_distance_m": config.quality.town_centroid_distance_m,
        },
        "inaturalist_recent_days": config.inaturalist.recent_days,
        "sources": {
            source_id: {
                "name": sources[source_id].name,
                "homepage": sources[source_id].homepage,
                "license": sources[source_id].license,
                "attribution": sources[source_id].attribution,
            }
            for source_id in config.credits
        },
    }
    store.root.mkdir(parents=True, exist_ok=True)
    path = store.root / "meta.json"
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
    return path


# --- profile ---------------------------------------------------------------------------------


@dataclass
class ProfileStats:
    total: int
    by_species: dict[str, int]
    by_year: dict[int, int]
    by_month: dict[int, int]
    by_source: dict[str, int]
    by_license: dict[str, int]
    obscured: int
    mean_place_distance_km_sightings: float
    mean_place_distance_km_all_cells: float


def profile_stats(store: SightingsStore, cells: pd.DataFrame) -> ProfileStats:
    """Counts per species/year/month/source/license, and a spatial-bias check: are sightings
    closer to towns than woodland cells are on average? (PRD → Known data traps: sightings skew
    toward trails, towns and popular areas.) Cell-level ``place_distance_km`` only, never
    coordinates: the store doesn't keep any (PRD → Sightings privacy)."""
    files = store.record_files()
    if not files:
        return ProfileStats(0, {}, {}, {}, {}, {}, 0, float("nan"), float("nan"))
    rows = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
    joined = rows.merge(cells[["cell_id", "place_distance_km"]], on="cell_id", how="left")

    dates = pd.to_datetime(rows["date"])
    woodland = cells[cells["woodland"]] if "woodland" in cells else cells
    return ProfileStats(
        total=len(rows),
        by_species=rows.groupby("species").size().to_dict(),
        by_year=dates.dt.year.value_counts().sort_index().to_dict(),
        by_month=dates.dt.month.value_counts().sort_index().to_dict(),
        by_source=rows.groupby("source").size().to_dict(),
        by_license=rows["license"].value_counts(dropna=True).to_dict(),
        obscured=int(rows["obscured"].sum()),
        mean_place_distance_km_sightings=float(joined["place_distance_km"].mean()),
        mean_place_distance_km_all_cells=float(woodland["place_distance_km"].mean()),
    )


# --- CLI -------------------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", choices=["resolve-taxa", "fetch", "profile"])
    parser.add_argument("--region", default="tuscany")
    args = parser.parse_args()

    config = load_sightings_config()
    root = data_dir()
    client = JsonClient()
    started = time.monotonic()

    def log(message: str) -> None:
        print(f"[{time.monotonic() - started:7.1f}s] {message}", flush=True)

    if args.command == "resolve-taxa":
        resolve_taxa(client, config, log)
        return
    if args.command == "fetch":
        summary = run_fetch(client, config, args.region, root, log=log)
        log(f"done: {summary}")
        return

    region = load_region(args.region)
    cells = pd.read_parquet(
        root / "grid" / region.id / "cells.parquet",
        columns=["cell_id", "woodland", "place_distance_km"],
    )
    store = SightingsStore(root / "sightings" / region.id)
    stats = profile_stats(store, cells)
    log(f"profile: {stats}")


if __name__ == "__main__":
    main()
