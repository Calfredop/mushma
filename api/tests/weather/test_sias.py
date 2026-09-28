import zipfile
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

from api.weather.sias import month_urls, parse_month, parse_stations, series_of

HEADER = '"ID_STAZ";"ID_PAR";"DATARIL";"VALORE"\n'


def month_zip(tmp_path: Path, rows: list[str], name: str = "sias.zip") -> Path:
    path = tmp_path / name
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("sias-precipitazioni_csv_2019_11.csv", HEADER + "".join(rows))
    return path


def hours(station: str, day: str, values: list[float]) -> list[str]:
    return [
        f'"{station}";"65";"{day} {hour:02d}:00:00.0";"{value:.2f}"\n'
        for hour, value in enumerate(values)
    ]


def test_parse_month_sums_the_hours_of_whole_days() -> None:
    rain = [0.0] * 20 + [1.2, 3.4, 0.0, 0.4]
    daily = parse_month_rows(
        hours("683", "2019-11-02", rain) + hours("684", "2019-11-02", [0] * 24)
    )

    assert list(daily.columns) == ["code", "date", "mm"]
    assert daily["code"].tolist() == ["683", "684"]
    assert daily["date"].tolist() == [date(2019, 11, 2)] * 2
    assert daily["mm"].tolist() == pytest.approx([5.0, 0.0])


def test_parse_month_drops_days_missing_hours() -> None:
    """From mid-2020 the monthly files hold only the first hours of each day: such a day is
    missing, not dry."""
    daily = parse_month_rows(
        hours("683", "2020-11-01", [0.0] * 9) + hours("683", "2020-11-02", [0.5] * 24)
    )

    assert daily["date"].tolist() == [date(2020, 11, 2)]
    assert daily["mm"].tolist() == pytest.approx([12.0])


def test_parse_month_keeps_rain_only() -> None:
    rows = hours("683", "2019-11-02", [1.0] * 24)
    rows += [r.replace('"65"', '"80"') for r in hours("683", "2019-11-03", [90.0] * 24)]

    daily = parse_month_rows(rows)

    assert daily["date"].tolist() == [date(2019, 11, 2)]


def parse_month_rows(rows: list[str]) -> pd.DataFrame:
    import tempfile

    with tempfile.TemporaryDirectory() as folder:
        return parse_month(month_zip(Path(folder), rows))


def test_parse_month_reads_an_empty_month(tmp_path: Path) -> None:
    """The portal lists January-May 2019 as zips holding only the header."""
    daily = parse_month(month_zip(tmp_path, []))

    assert daily.empty
    assert list(daily.columns) == ["code", "date", "mm"]


def test_parse_stations_reads_codes_heights_and_positions(tmp_path: Path) -> None:
    path = tmp_path / "stations.zip"
    text = (
        '"ID_STAZ";"DESC_STAZ";"ALTIT";"X_LON";"Y_LAT";"COMUNE_CODISTAT";"COMUNE_NOME";'
        '"PROVINCIA_IDPROVINCIAISTAT";"PROVINCIA_SIGLAPROVINCIA"\n'
        '"1466";"Cesaro Monte Soro";"1840";"14.6913891";"37.9336128";"083018";"CESARO";'
        '"083";"ME"\n'
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("elenco-sensori-meteo_csv_rsd.csv", text.encode("latin-1"))

    stations = parse_stations(path)

    assert list(stations.columns) == ["code", "name", "elevation_m", "lon", "lat"]
    row = stations.iloc[0]
    assert (row["code"], row["name"], row["elevation_m"]) == ("1466", "Cesaro Monte Soro", 1840.0)
    assert (row["lon"], row["lat"]) == pytest.approx((14.6913891, 37.9336128))


def test_month_urls_cover_the_published_months_in_the_range() -> None:
    urls = month_urls(date(2018, 12, 15), date(2019, 7, 2))

    assert [label for label, _ in urls] == ["2019_06", "2019_07"]
    assert urls[0][1].endswith("/sias-precipitazioni_csv_2019_06.zip")


def test_series_of_indexes_one_stations_days() -> None:
    daily = pd.DataFrame(
        {
            "code": ["683", "684", "683"],
            "date": [date(2019, 11, 2), date(2019, 11, 2), date(2019, 11, 3)],
            "mm": [5.0, 0.0, 1.5],
        }
    )

    series = series_of(daily, "683")

    assert series.to_dict() == {date(2019, 11, 2): 5.0, date(2019, 11, 3): 1.5}
