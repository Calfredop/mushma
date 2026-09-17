# Sightings ingest: GBIF + iNaturalist profile

Build date: 2026-09-17. Card: M2 · Sightings ingest. Traces to PRD → Model (Validation, Known data
traps), Features 4 (hotspots) and 6 (history), Sightings privacy, Milestone 2.

Public sightings of porcini, ovoli and gallinacci in Tuscany, from GBIF (which already carries
research-grade iNaturalist records) plus a direct iNaturalist call for the last two weeks GBIF
hasn't caught up with yet. This page records the taxa, the quality filters, what the first pull
looks like, and the biases to keep in mind before using it as backtest ground truth.

## At a glance

| | |
|---|---|
| Taxa | 6 GBIF usage keys across 3 species (porcini is 4: *B. edulis, aereus, reticulatus* incl. the *aestivalis* synonym, *pinophilus*) |
| GBIF records fetched (Tuscany bbox) | 206 |
| iNaturalist records fetched (last 14 days, not yet in GBIF) | 2 |
| Passed quality filters | 187 of 208 (90 %) |
| Landed on a woodland cell | **134** (29 outside the grid's bbox-vs-polygon slack, 24 on a non-woodland cell) |
| Obscured (town-centroid pin) | 3 of 134 (2 %) |
| Span | 2004–2026, 90 % from 2019 on |
| Storage | `api/data/sightings/tuscany/records/species=<species>/year=<yyyy>/data.parquet`, no coordinates |

Commands (from `api/`; `DATA_DIR` moves the data as for the grid and weather):

```sh
uv run python -m api.sightings.ingest resolve-taxa   # check config against each API's taxonomy
uv run python -m api.sightings.ingest fetch          # GBIF history + recent iNaturalist -> store
uv run python -m api.sightings.ingest profile        # counts, licenses, town-proximity bias
```

## Changes since the first pull (M3 · Model v1, 2026-09-17)

Two traps the species research had flagged were fixed before the backtest used these records as
ground truth. The profile below describes the first pull as it was.

- **Soil-DNA samples dropped.** `quality.exclude_basis_of_record: [MATERIAL_SAMPLE]` removes the 28
  "Global soil organisms" records (all 2019, all porcini). They record mycelium in a soil core, not a
  fruiting body on a day. `fetch` also deletes stored GBIF records a tightened filter now rejects.
- **Gallinacci widened to the genus.** The taxon is now *Cantharellus* (GBIF 9623860, rank GENUS;
  iNaturalist 47348) minus *C. cinereus* (9226626) and *C. melanoxeros* (5249532), which GBIF files
  under *Cantharellus*. Tuscan "*C. cibarius*" is mostly *C. pallens* and *C. alborufescens*
  (species-ecology.md, key finding 4), and the rules target *C. cibarius* s.l. GBIF records now
  carry their own `species_key` so the exclusion works on genus searches.
- **Result.** 121 stored sightings (was 134): porcini 61 (was 89), ovoli 29, gallinacci 31 (was
  16). From 2016 on, as unique cell-days: porcini 44, ovoli 25, gallinacci 26.

## Taxa

`config/sightings.yaml` pins each species' GBIF usage key and iNaturalist taxon id, resolved once
against each API's own species match and re-checked (unchanged) on 2026-09-17:

| species | scientific name | GBIF key | iNaturalist id |
|---|---|---|---|
| porcini | *Boletus edulis* | 5954958 | 48701 |
| porcini | *Boletus aereus* | 8733688 | 333772 |
| porcini | *Boletus reticulatus* (covers the *aestivalis* synonym) | 5954691 | 350216 |
| porcini | *Boletus pinophilus* | 5954949 | 335942 |
| ovoli | *Amanita caesarea* | 5240269 | 204588 |
| gallinacci | *Cantharellus cibarius* | 5249504 | 47347 |

*Boletus aestivalis* resolves to the accepted usage key for *B. reticulatus* in the GBIF backbone
(`matchType: EXACT`, `status: SYNONYM`), so the porcini group is four keys, not five.
`resolve-taxa` re-checks every key on demand and warns if a backbone change would move one, so a
future re-run catches drift instead of silently mis-scoping a search.

## Fetch

- **GBIF** (`api.sightings.gbif`): `occurrence/search` per taxon key, scoped to Tuscany's bbox
  (`decimalLatitude`/`decimalLongitude`, the region config's `bbox_wgs84`), `hasCoordinate=true`,
  `hasGeospatialIssue=false`. The bbox is a rectangle, not Tuscany's polygon, so it also catches
  the neighbouring Apennines (Emilia-Romagna, Liguria, Umbria); the woodland-grid join afterwards
  drops anything outside Tuscany or off the grid (see Coverage below). Pages are cached under
  `raw/gbif/<taxon_key>/page_*.json` with a completion marker, mirroring
  `api.grid.sources.fetch_arcgis_features`: delete a taxon's directory to re-fetch it.
- **iNaturalist** (`api.sightings.inaturalist`): `observations`, scoped to taxon id + place id
  (13073, Toscana) + `d1=<today - recent_days>`, `quality_grade=research,needs_id`, `geo=true`.
  Cached per `<taxon>/<since date>`; `since` moves forward every run, so a stale cache is never
  reused across two different windows, and a same-day rerun that skips a mid-day submission is
  caught by tomorrow's overlapping 14-day window instead.
- **Dedup** (`api.sightings.filters.deduplicate_inaturalist`): a GBIF record from the iNaturalist
  Research-Grade dataset (`50c9509d-22c7-4a22-a47d-8c48425ef4a7`) carries the iNaturalist
  observation id in `catalogNumber`; any direct iNaturalist fetch with that id is dropped. On this
  pull both of the 2 new iNaturalist records were genuinely new (0 duplicates), since GBIF's copy
  of iNaturalist data lags by days to weeks.

## Quality filters

`api.sightings.filters.drop_low_quality`, threshold `max_coordinate_uncertainty_m: 1000` (the
cell's own size):

| dropped for | count |
|---|---|
| missing event date | 3 |
| missing coordinates | 0 |
| too imprecise (uncertainty > 1000 m, or the source flagged it obscured) | 20 |
| **kept** | **187 of 208** |
| (missing uncertainty, kept but flagged for the profile) | 61 |

The 20 dropped for imprecision ranged 1,636–29,562 m; none were flagged `obscured` by iNaturalist
on this pull (Tuscan porcini/ovoli/gallinacci aren't geoprivacy-sensitive taxa), so every drop here
was a plain coordinate-uncertainty call. A *missing* uncertainty (61 records, 29 % of the input)
is not treated as coarse and is not dropped: 28 of the 61 come from one structured survey dataset
("Global soil organisms", precisely-coordinated material samples that simply carry no
`coordinateUncertaintyInMeters` field at all, not obscured citizen-science pins), and most of the
rest are iNaturalist-sourced GBIF records that never got a `positional_accuracy` value set by the
observer. Treating "unknown" as "coarse" would have thrown away almost a third of the usable data
for a field GBIF itself leaves blank on legitimately precise records.

One historical GBIF quirk: a few very old specimen records give `eventDate` as a *range*
(`"1701/1783"`, precision to the century) instead of a single date.
`api.sightings.gbif._event_date` takes the range's start and falls back to "no date" (dropped) when
even that isn't a full calendar date — this is what the 3 missing-date drops were, all pre-1800
herbarium specimens irrelevant to a weather-driven model anyway.

**Town-centroid flag** (`api.sightings.filters.flag_near_localities`, threshold 75 m): checked
against the same ISTAT inhabited-locality points the grid uses
(`api.grid.places.read_istat_localities`). 3 of the 187 quality-passing records (2 %) sit within
75 m of a named locality — plausibly a placeholder pin rather than the actual find. These are kept
but marked `obscured` in the store rather than dropped, alongside any record a source itself flags
as geoprivacy-obscured (none did, on this pull). The town-centroid effect turned out too small to
explain the near-town/near-trail bias the PRD names as a known trap (see Coverage bias below) — most
of that bias, if any, is not coming from placeholder pins.

## Coverage: from bbox to stored cell

| stage | count |
|---|---|
| fetched (GBIF + new iNaturalist) | 208 |
| passed quality filters | 187 |
| outside the woodland grid's actual coverage (bbox included neighbouring regions) | −29 |
| inside Tuscany but on a non-woodland cell | −24 |
| **stored** (one woodland cell each) | **134** |

The 29 "outside the grid" records are the bbox-vs-polygon slack described above (a rectangle drawn
around Tuscany also nets the Reggio Emilia/Parma Apennines and a strip of Liguria); they carry no
signal for a Tuscany model and are correctly dropped rather than mis-assigned to a nearby Tuscan
cell. The 24 "non-woodland cell" records are inside Tuscany but land on a 1 km cell the grid's
forest-fraction rule didn't classify as mostly forest (a mushroom found at a wood's edge, in a
hedgerow, or on a cell that's mostly agricultural) — the model only scores woodland cells, so these
can't validate anything and are dropped rather than forced onto a neighbouring cell.

## What the first pull looks like

- **By species**: porcini 89, ovoli 29, gallinacci 16 (stored, woodland cells only). Porcini
  dominates, matching it being both the best-recorded species overall and the union of 4 taxa.
- **By source**: 132 GBIF, 2 iNaturalist-direct. Datasets behind the GBIF share (206 fetched, before
  filters): iNaturalist Research-Grade (165), a "Global soil organisms" survey (28, all 2019,
  explaining most of that year's spike), Observation.org (3), a fungal-diversity monitoring project
  (FunDive, 2) and six herbaria/museum/atlas datasets (1–2 each, some back to the 1860s) — a useful
  reminder that "GBIF" isn't one source with one bias profile.
- **By year**: 90 % from 2019 on; 2019 itself is inflated by the one-off soil survey rather than an
  unusually good porcini year. Pre-2019 years are single digits or the survey's herbarium
  specimens — too sparse to backtest individually, as the PRD's "sparse species-days are noisy"
  warning anticipates.
- **By month**: September (49) and October (56) hold 78 % of dated records, matching the porcini/
  ovoli autumn window; a long tail from May to December matches gallinacci's longer season.
- **Licenses**: CC BY-NC 4.0 92, CC0 29, CC BY 4.0 11, plus `cc-by` and `cc-by-nc` 1 each — the last
  two are iNaturalist's own short-form codes from the two direct-fetch records, distinct strings
  from GBIF's full CC URLs for the same licences. The store keeps whichever string the source gave
  (a formatting detail for a future credits page to normalize, not a data-quality issue).
- **Spatial bias check**: mean distance-to-nearest-locality is **1.75 km for stored sightings vs.
  1.75 km across all Tuscan woodland cells** — no detectable town-proximity bias in this pull, at
  the resolution a 1 km cell and its `place_distance_km` can see. This is a genuinely useful,
  slightly surprising finding against the PRD's "sightings skew toward trails, towns and popular
  areas" caution: at only ~200 records the check has very little power to detect a real effect, and
  it can only compare cell-to-nearest-locality, not proximity to trails or roads specifically (that
  data isn't in the grid). Re-run this check after the backfill grows; don't read the current parity
  as ruling the bias out.

## Storage and privacy

`api.sightings.store.SightingsStore` keeps one row per kept sighting:
`(species, cell_id, date, source, record_id, license, obscured, fetched_at)`. `assign_cells` is the
only place raw coordinates are read — it projects WGS84 to EPSG:3035, floors to the cell's own
corner (`api.grid.cells.cell_id`), and the coordinates are dropped in the same step. No table this
module writes carries a coordinate, so a future API reading through
`SightingsStore.counts_by_cell` (species, cell_id, count only) cannot leak more precision than a
1 km cell even by accident (PRD → Sightings privacy: counts per cell, never coordinates, never
re-sharpened).

## Known gaps and hand-offs

- **Small n.** 134 stored sightings across 3 species and ~10 years is thin for a per-species,
  per-season backtest. M3's train/hold-out split (PRD → Validation) should expect wide confidence
  intervals, especially for gallinacci (16) and pre-2019 seasons.
- **License string formats differ by source** (GBIF: full CC URLs; iNaturalist direct: short
  codes). Not normalized; a credits page reading `license` per record should handle both, or this
  should be normalized before M4's API ships it.
- **Bbox vs. polygon slack** costs 29 fetched-and-filtered records nothing (correctly dropped), but
  means every taxon's occurrence count from `fetch_gbif`'s log line overstates Tuscany's true count
  by however much the neighbouring Apennines contribute; use the *stored* counts, not the raw fetch
  counts, for anything Tuscany-specific.
- **Town-centroid and geoprivacy flags are both quiet on this pull** (3 town-centroid, 0
  source-obscured) — not evidence they won't matter as the dataset grows or if a more sensitive
  taxon is ever added; keep the filter.
- **M3 · Model v1.** Read ground truth with `SightingsStore.counts_by_cell(con)`, joined to scored
  cell-days by `(species, cell_id, date)` for the lift/AUC backtest against a habitat-only baseline.
- **M4 · API + daily pipeline.** Schedule `ingest fetch` daily (or per M4's cadence) before scoring,
  after the weather update. Show `meta.json` → `sources` on the credits page, as the weather module
  does.

## Sources and licences

| source | licence | attribution |
|---|---|---|
| GBIF occurrence records | per-record (CC0, CC BY 4.0 or CC BY-NC 4.0) | "Occurrence data © GBIF.org contributors, gbif.org" |
| iNaturalist observations | per-record (mostly CC BY-NC 4.0) | "Observations © iNaturalist.org contributors, inaturalist.org" |

The app credits live in `api/src/api/config/sources.yaml` (`gbif`, `inaturalist`) and are copied
into `meta.json` by `api.sightings.ingest.write_meta`. Per-record licences never reach the UI: PRD
→ Sightings privacy limits what leaves the store to counts per cell, well short of anything a
per-record licence would apply to.
