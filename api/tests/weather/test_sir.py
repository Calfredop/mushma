from datetime import date

import pandas as pd
import pytest

from api.weather.sir import gauge_day_totals, parse_series, parse_stations

STATIONS = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [11.8174, 43.8104]},
            "properties": {
                "Codice": "TOS01000611",
                "Nome": "Camaldoli",
                "Comune": "Poppi",
                "Provincia": "AR",
                "Quota mslm": "1111.00",
                "Consistenza": {
                    "PLUVIOMETRIA - Aggregazione a 24 ore (9-9)": {
                        "Anni": [["2024", "2025", "2026"]],
                        "SorgenteDati": "https://www.sir.toscana.it/archivio/dati.php?IDST=pluvio&D=json&IDS=TOS01000611",
                    },
                    "TERMOMETRIA - Massima giornaliera": {"Anni": [["2025"]], "SorgenteDati": "x"},
                },
            },
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [10.4966, 43.3325]},
            "properties": {
                "Codice": "TOS19000601",
                "Nome": "5A",
                "Comune": "Cecina",
                "Provincia": "LI",
                "Quota mslm": "7.70",
                "Consistenza": {
                    "FREATIMETRIA - Livello medio giornaliero": {
                        "Anni": [["2025"]],
                        "SorgenteDati": "y",
                    }
                },
            },
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [11.82, 43.14]},
            "properties": {
                "Codice": "TOS10000710",
                "Nome": "Abbadia di Montepulciano",
                "Comune": "Montepulciano",
                "Provincia": "SI",
                "Quota mslm": "264.74",
                "Consistenza": {
                    "PLUVIOMETRIA - Aggregazione a 24 ore (9-9)": {
                        "Anni": [["1961", "2001"]],
                        "SorgenteDati": "z",
                    }
                },
            },
        },
    ],
}


def test_parse_stations_lists_rain_gauges_with_data_in_the_years_asked() -> None:
    # Stations without any series come with an empty list instead of an object.
    empty = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [11.0, 43.0]},
        "properties": {"Codice": "TOS0", "Nome": "Nuova", "Consistenza": []},
    }
    payload = {**STATIONS, "features": [*STATIONS["features"], empty]}

    gauges = parse_stations(payload, years={"2025", "2026"})

    assert gauges.to_dict("records") == [
        {
            "code": "TOS01000611",
            "name": "Camaldoli",
            "comune": "Poppi",
            "province": "AR",
            "elevation_m": 1111.0,
            "lon": 11.8174,
            "lat": 43.8104,
            "url": "https://www.sir.toscana.it/archivio/dati.php?IDST=pluvio&D=json&IDS=TOS01000611",
        }
    ]


def test_parse_series_keeps_validated_and_prevalidated_days() -> None:
    payload = {
        "properties": {
            "UnitaMisura": "mm",
            "TipoDati": "PLUVIOMETRIA - Aggregazione a 24 ore (9-9)",
            "SerieDati": [
                {"Data": "2026-09-10 09:00:00", "Valore": "0.2", "TipoValore": "V"},
                {"Data": "2026-09-11 09:00:00", "Valore": "28.6", "TipoValore": "P"},
                {"Data": "2026-09-12 09:00:00", "Valore": "3.0", "TipoValore": "N"},
                {"Data": "2026-09-13 09:00:00", "Valore": None, "TipoValore": "@"},
                {"Data": "2026-09-14 09:00:00", "Valore": "1.0", "TipoValore": "R"},
            ],
        }
    }

    series = parse_series(payload)

    assert series.to_dict() == {date(2026, 9, 10): 0.2, date(2026, 9, 11): 28.6}


def test_parse_series_rejects_other_units() -> None:
    payload = {"properties": {"UnitaMisura": "cm", "TipoDati": "x", "SerieDati": []}}

    with pytest.raises(ValueError, match="cm"):
        parse_series(payload)


def test_gauge_day_totals_split_calendar_days_into_9_to_9_windows() -> None:
    # A gauge day ending at 09:00 on D holds 15 h of D-1 and 9 h of D.
    calendar = pd.Series({date(2026, 9, 9): 0.0, date(2026, 9, 10): 24.0, date(2026, 9, 11): 8.0})

    totals = gauge_day_totals(calendar)

    assert totals.to_dict() == {
        date(2026, 9, 10): pytest.approx(0.0 * 15 / 24 + 24.0 * 9 / 24),
        date(2026, 9, 11): pytest.approx(24.0 * 15 / 24 + 8.0 * 9 / 24),
    }
