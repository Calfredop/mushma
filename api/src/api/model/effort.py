"""Observer effort: how many fungi of any kind people recorded on iNaturalist each day.

Sightings pile up on the days people go out (weekends, October), whatever the conditions. The
backtest weights its same-cell background days by this series, a target-group background: a day
counts as a fair alternative to the sighting's day in proportion to how many fungi were recorded on
it. Aggregate daily counts only; no observation or coordinate is read or kept. Cached per year
under ``$DATA_DIR/raw/inaturalist/effort/``.
"""

import json
import urllib.parse
from datetime import date, timedelta
from pathlib import Path
from typing import Protocol

import pandas as pd

HISTOGRAM_ENDPOINT = "https://api.inaturalist.org/v1/observations/histogram"
FUNGI_TAXON_ID = 47170  # iNaturalist kingdom Fungi (includes lichens)


class Client(Protocol):
    def get(self, url: str) -> dict: ...


def histogram_url(place_id: int, year: int) -> str:
    params = {
        "place_id": place_id,
        "taxon_id": FUNGI_TAXON_ID,
        "verifiable": "true",
        "date_field": "observed",
        "interval": "day",
        "d1": f"{year}-01-01",
        "d2": f"{year}-12-31",
    }
    return f"{HISTOGRAM_ENDPOINT}?{urllib.parse.urlencode(params)}"


def daily_effort(client: Client, place_id: int, years: list[int], cache_dir: Path) -> pd.Series:
    """Fungi observations per day for every day of ``years``, 0 where none were recorded."""
    counts: dict[date, int] = {}
    for year in years:
        path = cache_dir / f"fungi_place{place_id}_{year}.json"
        if path.exists():
            payload = json.loads(path.read_text())
        else:
            payload = client.get(histogram_url(place_id, year))
            path.parent.mkdir(parents=True, exist_ok=True)
            partial = path.with_name(path.name + ".part")
            partial.write_text(json.dumps(payload))
            partial.replace(path)
        by_day = payload.get("results", {}).get("day", {})
        day = date(year, 1, 1)
        while day.year == year:
            counts[day] = int(by_day.get(day.isoformat(), 0))
            day += timedelta(days=1)
    return pd.Series(counts, dtype="int64").sort_index()
