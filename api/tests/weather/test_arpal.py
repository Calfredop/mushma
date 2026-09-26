"""ARPA Liguria (OMIRL) daily rain for the Liguria gauge check."""

from datetime import date

import pandas as pd
import pytest

from api.weather.arpal import (
    gauge_stations,
    parse_daily_report,
    parse_omirl_stations,
    parse_station_list,
    utc_day_totals,
)

REPORT = """

"Stazione",CHIAVARI - CAPERANA
"Parametro",PRECIPITAZIONE - PRECIPITAZIONE CUMULATA (mm)
Nessun dato presente

"Stazione",SANTUARIO DI SAVONA
"Parametro",PRECIPITAZIONE - PRECIPITAZIONE CUMULATA (mm)

"Inizio rilevazione","Fine rilevazione","Valore","Dataset","Valido"
"05/01/2025","05/01/2025",".2","Tutti i dati","Sì"
"06/01/2025","06/01/2025","29.8","Tutti i dati","Sì"
"07/01/2025","07/01/2025","","Tutti i dati","Sì"
"08/01/2025","08/01/2025","4","Tutti i dati","No"

"Stazione",BORZONE
"Parametro",PRECIPITAZIONE - PRECIPITAZIONE CUMULATA (mm)

"Inizio rilevazione","Fine rilevazione","Valore","Dataset","Valido"
"05/01/2025","05/01/2025","0","Tutti i dati","Sì"
"""

STATION_LIST = (
    "<TABLE><TR><TD><B>CODICE STAZIONE</B></TD><TD><B>NOME STAZIONE</B></TD>"
    "<TD><B>PROVINCIA</B></TD><TD><B>BACINO</B></TD><TD><B>QUOTA (m)</B></TD></TR>"
    '<TR><TD ALIGN=center><a href="x.asp?stazione=ME00233" target="_new">BRZON</a></TD>'
    "<TD ALIGN=center>BORZONE</TD><TD ALIGN=center>GENOVA</TD><TD ALIGN=center>ENTELLA</TD>"
    '<TD class="right_trasp">386</TD><TR>'
    '<TR><TD ALIGN=center><a href="x.asp?stazione=ME00001" target="_new">SSAVO</a></TD>'
    "<TD ALIGN=center>SANTUARIO DI SAVONA</TD><TD ALIGN=center>SAVONA</TD>"
    '<TD ALIGN=center>LETIMBRO</TD><TD class="right_trasp">120</TD><TR>'
    '<TR><TD ALIGN=center><a href="x.asp?stazione=ME00002" target="_new">SSAV0</a></TD>'
    "<TD ALIGN=center>SANTUARIO DI SAVONA</TD><TD ALIGN=center>SAVONA</TD>"
    '<TD ALIGN=center>LETIMBRO</TD><TD class="right_trasp">121</TD><TR>'
    "</TABLE>"
)

OMIRL = [
    {"shortCode": "BRZON", "name": "Borzone", "lat": 44.42, "lon": 9.39, "alt": 386},
    {"shortCode": "SSAVO", "name": "Santuario", "lat": 44.33, "lon": 8.44, "alt": 120},
]


def test_parse_daily_report_keeps_valid_values_per_station() -> None:
    rows = parse_daily_report(REPORT)

    assert list(rows.columns) == ["station_name", "date", "rain_mm"]
    savona = rows[rows["station_name"] == "SANTUARIO DI SAVONA"].set_index("date")["rain_mm"]
    assert savona.to_dict() == {date(2025, 1, 5): 0.2, date(2025, 1, 6): 29.8}
    assert set(rows["station_name"]) == {"SANTUARIO DI SAVONA", "BORZONE"}


def test_parse_station_list_reads_codes_names_and_heights() -> None:
    stations = parse_station_list(STATION_LIST)

    assert list(stations["code"]) == ["BRZON", "SSAVO", "SSAV0"]
    assert list(stations["name"]) == ["BORZONE", "SANTUARIO DI SAVONA", "SANTUARIO DI SAVONA"]
    assert list(stations["elevation_m"]) == [386.0, 120.0, 121.0]


def test_parse_omirl_stations_reads_coordinates() -> None:
    stations = parse_omirl_stations(OMIRL)

    assert stations.set_index("code").loc["BRZON", ["lat", "lon"]].tolist() == [44.42, 9.39]


def test_gauge_stations_resolve_a_shared_name_through_the_code_omirl_knows() -> None:
    gauges = gauge_stations(
        parse_daily_report(REPORT), parse_station_list(STATION_LIST), parse_omirl_stations(OMIRL)
    )

    by_name = gauges.set_index("name")
    assert by_name.loc["SANTUARIO DI SAVONA", "code"] == "SSAVO"
    assert by_name.loc["BORZONE", ["lat", "lon", "elevation_m"]].tolist() == [44.42, 9.39, 386.0]


def test_utc_day_totals_shift_local_days_by_the_rome_offset() -> None:
    # A UTC day starts 1 h (winter) or 2 h (summer) after local midnight, so it takes that many
    # hours from the next local day, assuming rain spread evenly over a day.
    calendar = pd.Series(
        {
            date(2025, 1, 6): 24.0,
            date(2025, 1, 7): 0.0,
            date(2025, 7, 6): 0.0,
            date(2025, 7, 7): 24.0,
        }
    )

    totals = utc_day_totals(calendar)

    assert totals[date(2025, 1, 6)] == pytest.approx(23.0)
    assert totals[date(2025, 7, 6)] == pytest.approx(2.0)
    assert date(2025, 1, 7) not in totals.index  # its next local day is missing
