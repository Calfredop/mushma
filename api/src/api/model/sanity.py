"""Sanity check: do the stored scores agree with seasons Tuscan foragers and local news remembered?

    uv run python -m api.model.sanity --label v1

Each contrast pairs two windows of the porcini group score (an area, one or more seasons, a date
range) and states which one local sources say was better. A window's value is its mean score over
its woodland cell-days; a list of several seasons is that area's normal for the window. Contrasts
and areas were written down, from the sources cited, before any area score was looked at. A
contrast holding is a sanity check, not validation: the sources are news and forager blogs, often
about a single valley, and several describe a record season in Coldiretti's recycled wording.
"""

import argparse
import time
from dataclasses import dataclass, field
from datetime import date

import duckdb
import pandas as pd

from api.grid.sources import data_dir
from api.model.store import ScoreStore


def fix_mojibake(name: str) -> str:
    """Undo UTF-8 text read as Latin-1 (``Castel San NiccolÃ²``), which the grid's ISTAT names
    carry until the grid reader is fixed; clean names pass through."""
    if "Ã" not in name and "Â" not in name:
        return name
    try:
        return name.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


@dataclass(frozen=True)
class Area:
    comuni: list[str] = field(default_factory=list)
    provinces: list[str] = field(default_factory=list)  # "*" for the whole region
    excluding: list[str] = field(default_factory=list)  # comuni left out of the provinces


def area_cells(cells: pd.DataFrame, area: Area) -> set[str]:
    woodland = cells[cells["woodland"]]
    names = woodland["comune_name"].fillna("").map(fix_mojibake)
    chosen = names.isin(area.comuni)
    if area.provinces:
        in_provinces = (
            pd.Series(True, index=woodland.index)
            if "*" in area.provinces
            else woodland["province"].isin(area.provinces)
        )
        chosen |= in_provinces & ~names.isin(area.excluding)
    return set(woodland.loc[chosen, "cell_id"])


@dataclass(frozen=True)
class Window:
    area: str
    seasons: list[int]
    start: str  # MM-DD
    end: str  # MM-DD, same year

    def bounds(self, season: int) -> tuple[date, date]:
        return date.fromisoformat(f"{season}-{self.start}"), date.fromisoformat(
            f"{season}-{self.end}"
        )


@dataclass(frozen=True)
class Contrast:
    id: str
    claim: str
    source: str
    higher: Window
    lower: Window


GARFAGNANA = [
    "Camporgiano",
    "Careggine",
    "Castelnuovo di Garfagnana",
    "Castiglione di Garfagnana",
    "Fabbriche di Vergemoli",
    "Fosciandora",
    "Gallicano",
    "Minucciano",
    "Molazzana",
    "Piazza al Serchio",
    "Pieve Fosciana",
    "San Romano in Garfagnana",
    "Sillano Giuncugnano",
    "Vagli Sotto",
    "Villa Collemandina",
]
LUNIGIANA = [
    "Aulla",
    "Bagnone",
    "Casola in Lunigiana",
    "Comano",
    "Filattiera",
    "Fivizzano",
    "Fosdinovo",
    "Licciana Nardi",
    "Mulazzo",
    "Podenzana",
    "Pontremoli",
    "Tresana",
    "Villafranca in Lunigiana",
    "Zeri",
]
CASENTINO = [
    "Bibbiena",
    "Castel Focognano",
    "Castel San Niccolò",
    "Chitignano",
    "Chiusi della Verna",
    "Montemignaio",
    "Ortignano Raggiolo",
    "Poppi",
    "Pratovecchio Stia",
    "Talla",
]
MUGELLO = [
    "Barberino di Mugello",
    "Borgo San Lorenzo",
    "Dicomano",
    "Firenzuola",
    "Marradi",
    "Palazzuolo sul Senio",
    "Scarperia e San Piero",
    "Vicchio",
]
AMIATA = [
    "Abbadia San Salvatore",
    "Arcidosso",
    "Castel del Piano",
    "Castell'Azzara",
    "Castiglione d'Orcia",
    "Piancastagnaio",
    "Radicofani",
    "Roccalbegna",
    "Santa Fiora",
    "Seggiano",
    "Semproniano",
]

AREAS: dict[str, Area] = {
    "garfagnana": Area(comuni=GARFAGNANA),
    "lunigiana": Area(comuni=LUNIGIANA),
    "northwest": Area(comuni=GARFAGNANA + LUNIGIANA),
    "casentino": Area(comuni=CASENTINO),
    "arezzo_outside_casentino": Area(provinces=["AR"], excluding=CASENTINO),
    "siena_and_arezzo": Area(provinces=["SI", "AR"], excluding=CASENTINO + AMIATA),
    "mugello": Area(comuni=MUGELLO),
    "amiata": Area(comuni=AMIATA),
    "vallombrosa": Area(comuni=["Reggello"]),
    "abetone": Area(comuni=["Abetone Cutigliano"]),
    "tuscany": Area(provinces=["*"]),
}

NORMAL = list(range(2017, 2026))  # the seasons scored for the check

CONTRASTS: list[Contrast] = [
    Contrast(
        "casentino_2023",
        "2023: Casentino was the one good area of Arezzo province; the rest had an 'annata nera'",
        "https://www.lanazione.it/arezzo/cronaca/lisola-felice-per-i-porcini-e-qui-tanti-cercatori-affollano-le-foreste-per-lesperto-e-una-stagione-al-top-56a1b784",
        Window("casentino", [2023], "09-15", "10-31"),
        Window("arezzo_outside_casentino", [2023], "09-15", "10-31"),
    ),
    Contrast(
        "northwest_2023",
        "2023: excellent in Lunigiana and Garfagnana, 'in piccola misura' near Siena and Arezzo",
        "https://funghimagazine.it/aggiornamento-porcini-12-10-2023/",
        Window("northwest", [2023], "09-15", "10-31"),
        Window("siena_and_arezzo", [2023], "09-15", "10-31"),
    ),
    Contrast(
        "october_2021",
        "October 2021: an extraordinary flush in Garfagnana, an 'infame stagione' at Vallombrosa",
        "https://www.giornaledibarga.it/2021/10/incredibile-nascita-di-funghi-nelle-selve-della-garfagnana-e-della-media-vallle-357672/",
        Window("garfagnana", [2021], "10-01", "10-31"),
        Window("vallombrosa", [2021], "10-01", "10-31"),
    ),
    Contrast(
        "drought_2017",
        "2017: a drought year, foragers 'a mani vuote'; autumn 2018 followed a very wet August",
        "https://www.ilgiunco.net/2018/09/19/funghi-e-boom-in-toscana-e-in-maremma-autunno-record-dopo-le-piogge-di-agosto/",
        Window("tuscany", [2018], "09-01", "10-31"),
        Window("tuscany", [2017], "09-01", "10-31"),
    ),
    Contrast(
        "abetone_2017_2019",
        "Abetone, October: 'niente funghi' in 2017, 'bosco ricoperto di funghi' in 2019",
        "https://funghintoscana.blogspot.com/2017/10/fine-corsa.html",
        Window("abetone", [2019], "10-01", "10-31"),
        Window("abetone", [2017], "10-01", "10-31"),
    ),
    Contrast(
        "casentino_2024",
        "September 2024: a record season in Casentino",
        "https://www.lanazione.it/arezzo/cronaca/lisola-felice-dei-funghi-e-qui-il-casentino-come-le-dolomiti-annata-con-produzione-da-record-5a57ebf8",
        Window("casentino", [2024], "09-01", "09-30"),
        Window("casentino", NORMAL, "09-01", "09-30"),
    ),
    Contrast(
        "mugello_2024_2025",
        "Mugello, early September: no season yet after a dry 2024 summer, 'stagione d'oro' in 2025",
        "https://www.lanazione.it/firenze/cronaca/stagione-doro-per-il-fungo-00cfcaa5",
        Window("mugello", [2025], "09-01", "09-15"),
        Window("mugello", [2024], "09-01", "09-15"),
    ),
    Contrast(
        "northwest_2025_timing",
        "2025: an early boom in Lunigiana and Garfagnana (late August, early September), then a "
        "poor October of heat and drying wind",
        "https://funghimagazine.it/aggiornamento-nascite-funghi-23-10-2025/",
        Window("northwest", [2025], "08-25", "09-15"),
        Window("northwest", [2025], "10-01", "10-31"),
    ),
    Contrast(
        "amiata_2025_timing",
        "2025: Amiata at its peak in early September, October poor",
        "https://funghimagazine.it/buttata-record-2025-annata-eccezionale-per-i-porcini/",
        Window("amiata", [2025], "08-25", "09-15"),
        Window("amiata", [2025], "10-01", "10-31"),
    ),
    Contrast(
        "garfagnana_2019",
        "Garfagnana 2019: a record September and October",
        "https://www.lanazione.it/lucca/cronaca/raccolta-funghi-c08befa0",
        Window("garfagnana", [2019], "09-01", "10-31"),
        Window("garfagnana", NORMAL, "09-01", "10-31"),
    ),
    Contrast(
        "vallombrosa_2022",
        "Vallombrosa, late October 2022: 'secco strasecco', never seen anything like it",
        "https://funghintoscana.blogspot.com/2022/11/fine-dei-giochi.html",
        Window("vallombrosa", NORMAL, "10-15", "10-31"),
        Window("vallombrosa", [2022], "10-15", "10-31"),
    ),
]


def _window_mean(scores: pd.DataFrame, cells: set[str], window: Window) -> tuple[float, int]:
    days = pd.to_datetime(scores["date"]).dt.date
    in_window = pd.Series(False, index=scores.index)
    for season in window.seasons:
        start, end = window.bounds(season)
        in_window |= (days >= start) & (days <= end)
    rows = scores.loc[in_window & scores["cell_id"].isin(cells), "score"]
    return (float(rows.mean()) if len(rows) else float("nan")), int(len(rows))


def evaluate_contrasts(
    contrasts: list[Contrast],
    scores: pd.DataFrame,
    cells: pd.DataFrame,
    areas: dict[str, Area] = AREAS,
) -> pd.DataFrame:
    """One row per contrast: both windows' mean scores and whether the higher one is higher."""
    resolved = {name: area_cells(cells, area) for name, area in areas.items()}
    rows = []
    for contrast in contrasts:
        high, high_n = _window_mean(scores, resolved[contrast.higher.area], contrast.higher)
        low, low_n = _window_mean(scores, resolved[contrast.lower.area], contrast.lower)
        rows.append(
            {
                "id": contrast.id,
                "claim": contrast.claim,
                "higher_mean": high,
                "lower_mean": low,
                "higher_cell_days": high_n,
                "lower_cell_days": low_n,
                "holds": bool(high > low),
                "source": contrast.source,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--label", required=True)
    parser.add_argument("--region", default="tuscany")
    parser.add_argument("--group", default="porcini")
    args = parser.parse_args()
    started = time.monotonic()
    root = data_dir()
    cells = pd.read_parquet(
        root / "grid" / args.region / "cells.parquet",
        columns=["cell_id", "comune_name", "province", "woodland"],
    )
    seasons = sorted({s for c in CONTRASTS for w in (c.higher, c.lower) for s in w.seasons})
    store = ScoreStore(root / "scores" / args.region)
    scores = store.read(
        duckdb.connect(), args.group, date(min(seasons), 1, 1), date(max(seasons), 12, 31)
    ).df()
    result = evaluate_contrasts(CONTRASTS, scores, cells)
    out = root / "backtest" / args.region / args.label
    out.mkdir(parents=True, exist_ok=True)
    result.to_csv(out / f"sanity_{args.group}.csv", index=False)
    print(result[["id", "higher_mean", "lower_mean", "holds"]].to_string(index=False))
    print(f"[{time.monotonic() - started:.1f}s] {int(result['holds'].sum())}/{len(result)} hold")


if __name__ == "__main__":
    main()
