from datetime import date
from io import StringIO

import pytest

from api.weather.siarl import parse_daily_rain, parse_stations, year_urls

STATIONS_HEADER = (
    "Cod staz;Regione;Provincia;Nome stazione;Comune;Località;ALTITUDINE;DATA_INI_OSS;"
    "DATA_END_OSS;lat;lon;Geojson;the_geom\n"
)
DAILY_HEADER = "Stazione;Grandezza;Data rilevazione;Valore;Indice di validita\n"


def test_parse_stations_reads_position_and_height() -> None:
    stations = parse_stations(
        StringIO(
            STATIONS_HEADER
            + "38;LAZIO;RI;ACCUMOLI;ACCUMOLI;TERRACINO;1176;1-ott-05;;42.68261;13.21003;"
            "{'type':'Point','coordinates':[13.21003,42.68261]};POINT (13.21003 42.68261)\n"
        )
    )

    assert list(stations.columns) == ["code", "name", "comune", "lat", "lon", "elevation_m"]
    row = stations.iloc[0]
    assert (row["code"], row["name"], row["comune"]) == ("38", "ACCUMOLI", "ACCUMOLI")
    assert row["lat"] == pytest.approx(42.68261)
    assert row["lon"] == pytest.approx(13.21003)
    assert row["elevation_m"] == 1176


def test_parse_stations_trims_padded_names() -> None:
    stations = parse_stations(
        StringIO(STATIONS_HEADER + "40;LAZIO;RM;AGOSTA ;AGOSTA;LA CISTERNA;476;;;41.99;13.03;;\n")
    )

    assert stations["name"].tolist() == ["AGOSTA"]


def test_parse_daily_rain_keeps_the_daily_total_of_exact_values() -> None:
    daily = parse_daily_rain(
        StringIO(
            DAILY_HEADER
            + "ACCUMOLI;PREC_TOTG;01/01/2023 00:00; 4.0;Dato esatto\n"
            + "ACCUMOLI;TEMPARIA2M_MAXG;01/01/2023 00:00; 14.1;Dato esatto\n"
            + "ACCUMOLI;PREC_TOTG;02/01/2023 00:00; 0.0;Dato esatto\n"
            + "ACCUMOLI;PREC_TOTG;03/01/2023 00:00; 12.0;Dato stimato\n"
        )
    )

    assert list(daily.columns) == ["name", "date", "mm"]
    assert daily["date"].tolist() == [date(2023, 1, 1), date(2023, 1, 2)]
    assert daily["mm"].tolist() == [4.0, 0.0]


def test_parse_daily_rain_reads_decimal_commas_of_the_older_files() -> None:
    daily = parse_daily_rain(
        StringIO(
            "Stazione;Grandezza;Data rilevazione;Valore;Indice di validità\n"
            + "AGOSTA ;PREC_TOTG;15/10/2018 00:00;12,6;Dato esatto\n"
        )
    )

    assert daily["name"].tolist() == ["AGOSTA"]
    assert daily["mm"].tolist() == [12.6]


def test_parse_daily_rain_drops_impossible_values() -> None:
    daily = parse_daily_rain(
        StringIO(
            DAILY_HEADER
            + "A;PREC_TOTG;01/01/2020 00:00;-1;Dato esatto\n"
            + "A;PREC_TOTG;02/01/2020 00:00;900;Dato esatto\n"
            + "A;PREC_TOTG;03/01/2020 00:00;;Dato esatto\n"
            + "A;PREC_TOTG;04/01/2020 00:00;3,2;Dato esatto\n"
        )
    )

    assert daily["date"].tolist() == [date(2020, 1, 4)]


def test_year_urls_lists_only_the_published_years_in_range() -> None:
    urls = year_urls(2015, 2024)

    assert sorted(urls) == [2016, 2018, 2020, 2021, 2023]
    assert all(url.startswith("https://dati.lazio.it/dataset/") for url in urls.values())
