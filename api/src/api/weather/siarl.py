"""SIARL (ARSIAL) agrometeo gauges: the open daily rain for Lazio's reanalysis check.

The Region's agrometeorological service publishes its 95 stations as open data (CC BY 4.0,
dati.lazio.it, "Rete Agrometeorologica" and "Serie Storica Agrometeo"): a station list with
position and height, and one CSV per year with a row per station, quantity and day (``PREC_TOTG``
is the day's rain in mm). Older years write decimal commas, newer ones points.

Only some yearly files download: 2017, 2019 and 2022 answer HTTP 500 on the portal (September
2026), and 2021 and 2023 stop at the end of July and June. ``year_urls`` lists the ones that
work from 2016, the start of the CDS history. Every published value is flagged "Dato esatto";
anything else, and totals outside 0 to ``MAX_PLAUSIBLE_MM``, is dropped.

The Region's Protezione Civile publishes a denser network's daily rain too (about 220 gauges,
"Serie storica dato pluviometrico"), but its station list, the only source of the gauges'
positions, answers HTTP 500, so it cannot be placed on the grid.
"""

from typing import IO

import pandas as pd

DATASET = "https://dati.lazio.it/dataset"
STATIONS_URL = (
    f"{DATASET}/4f4194c2-8432-4f99-aab3-2b07da7df3fd/resource/"
    "1373f7a6-f208-40f0-8d0c-e41cf25d2599/download/anagraficastazioniagrometeoarsial.csv"
)
_SERIES = f"{DATASET}/d705a845-4a94-4682-9e40-a7b860c45778/resource"
YEAR_URLS = {
    2016: f"{_SERIES}/59af9fa7-77eb-4ced-b3d4-2f6d159ccfa2/download/opdata16.csv",
    2018: f"{_SERIES}/46dd1809-0642-4cac-9db1-cce1c895c0b1/download/opdata18.csv",
    2020: f"{_SERIES}/3a95b075-8ccc-4865-923d-e7bf988a7218/download/opdata20.csv",
    2021: f"{_SERIES}/086fdb8b-5ffe-4351-95f2-a94657edcf9d/download/opdata21-1.csv",
    2023: f"{_SERIES}/1cd6887b-8b6e-49ef-9689-b3ca6c790a23/download/arsial_2023.csv",
}
RAIN = "PREC_TOTG"
EXACT = "Dato esatto"
MAX_PLAUSIBLE_MM = 500.0
ENCODING = "latin-1"


def year_urls(first: int, last: int) -> dict[int, str]:
    """The published yearly files from ``first`` to ``last``, by year."""
    return {year: url for year, url in YEAR_URLS.items() if first <= year <= last}


def parse_stations(source: str | IO) -> pd.DataFrame:
    """Station list: ``code, name, comune, lat, lon, elevation_m``."""
    raw = pd.read_csv(source, sep=";", encoding=ENCODING, dtype={"Cod staz": str})
    stations = pd.DataFrame(
        {
            "code": raw["Cod staz"].str.strip(),
            "name": raw["Nome stazione"].str.strip(),
            "comune": raw["Comune"].str.strip(),
            "lat": raw["lat"].astype("float64"),
            "lon": raw["lon"].astype("float64"),
            "elevation_m": raw["ALTITUDINE"],
        }
    )
    return stations.reset_index(drop=True)


def parse_daily_rain(source: str | IO) -> pd.DataFrame:
    """Daily rain per station name: ``name, date, mm``, exact values only."""
    raw = pd.read_csv(source, sep=";", encoding=ENCODING, dtype=str, keep_default_na=False)
    raw.columns = ["name", "quantity", "when", "value", "validity"]
    rows = raw[(raw["quantity"] == RAIN) & (raw["validity"].str.strip() == EXACT)]
    mm = pd.to_numeric(rows["value"].str.strip().str.replace(",", "."), errors="coerce")
    keep = mm.notna() & (mm >= 0) & (mm <= MAX_PLAUSIBLE_MM)
    rows = rows[keep]
    return pd.DataFrame(
        {
            "name": rows["name"].str.strip().to_numpy(),
            "date": pd.to_datetime(rows["when"], format="%d/%m/%Y %H:%M").dt.date.to_numpy(),
            "mm": mm[keep].to_numpy(dtype="float64"),
        }
    )
