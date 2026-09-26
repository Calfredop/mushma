import json
from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest

from api.weather.arpal import utc_day_totals
from api.weather.checks import compare_gauge, lapse_regression, leave_out_errors
from api.weather.points import point_id
from api.weather.sir import gauge_day_totals

DAYS = [date(2024, 10, 1) + timedelta(days=i) for i in range(3)]


def _nodes() -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(7)
    for i in range(11):
        for j in range(11):
            lat, lon = round(43.0 + i / 10, 6), round(11.0 + j / 10, 6)
            rows.append((point_id(lat, lon), lat, lon, float(rng.uniform(0, 1500))))
    return pd.DataFrame(rows, columns=["point_id", "lat", "lon", "z"])


def _field(nodes: pd.DataFrame, cooling_per_km: float) -> pd.DataFrame:
    """A temperature that is linear in lat/lon and cools with height; the day adds an offset."""
    rows = []
    for k, day in enumerate(DAYS):
        values = (
            20 + k - 2 * (nodes.lat - 43) + 0.5 * (nodes.lon - 11) - cooling_per_km * nodes.z / 1000
        )
        rows += [
            (pid, day, "temperature_2m_mean", v)
            for pid, v in zip(nodes.point_id, values, strict=True)
        ]
    return pd.DataFrame(rows, columns=["point_id", "date", "variable", "value"])


def test_lapse_regression_recovers_the_cooling_rate_across_nodes() -> None:
    nodes = _nodes()

    rates = lapse_regression(_field(nodes, cooling_per_km=4.5), nodes)

    assert set(rates["date"]) == set(DAYS)
    assert rates["cooling_per_km"].to_numpy() == pytest.approx(4.5)


def test_leave_out_is_exact_for_a_linear_field_with_the_right_lapse_rate() -> None:
    nodes = _nodes()
    daily = _field(nodes, cooling_per_km=4.5)

    right = leave_out_errors(daily, nodes, stride=2, lapse_rates={"temperature_2m_mean": 4.5})
    wrong = leave_out_errors(daily, nodes, stride=2, lapse_rates={"temperature_2m_mean": 0.0})

    assert right.loc["temperature_2m_mean", "rmse"] == pytest.approx(0.0, abs=1e-9)
    assert wrong.loc["temperature_2m_mean", "rmse"] > 0.1
    assert right.loc["temperature_2m_mean", "targets"] > 0


def test_compare_gauge_measures_bias_and_agreement_on_gauge_days() -> None:
    days = pd.date_range("2025-01-01", periods=120).date
    rng = np.random.default_rng(3)
    calendar = pd.Series(rng.gamma(0.4, 12, len(days)), index=days)
    gauge = gauge_day_totals(calendar)

    metrics = compare_gauge(0.8 * calendar, gauge)

    assert metrics["days"] == 119
    assert metrics["ratio"] == pytest.approx(0.8)
    assert metrics["daily_corr"] == pytest.approx(1.0)
    assert metrics["wet3_hit_rate"] <= 1.0


def test_compare_gauge_takes_the_gauge_network_day_cut() -> None:
    days = pd.date_range("2025-01-01", periods=60).date
    rng = np.random.default_rng(5)
    calendar = pd.Series(rng.gamma(0.4, 12, len(days)), index=days)
    gauge = utc_day_totals(calendar)

    metrics = compare_gauge(0.5 * calendar, gauge, day_totals=utc_day_totals)

    assert metrics["days"] == 59
    assert metrics["ratio"] == pytest.approx(0.5)
    assert metrics["daily_corr"] == pytest.approx(1.0)


def test_umbria_reads_the_servizio_idrografico_network(tmp_path) -> None:
    import zipfile
    from datetime import date

    from api.weather.checks import GAUGE_NETWORKS

    header = (
        '"ID_SENSORE_DETTAGLIO","ID_TIPOLOGIA_SENSORE","STRUMENTO","TIPO_STRUMENTO",'
        '"UNITA_MISURA","ID_STAZIONE","NOME_STAZIONE","COMUNE","LATITUDINE","LONGITUDINE",'
        '"ANNO","MESE","GIORNO","CUMDAY"\n'
    )
    rows = "".join(
        f'1,"20207","Pluviometro","Pluviometro","mm",485400,"Castelluccio di Norcia","NORCIA",'
        f"42.829,13.214,2025,1,{day},{day / 10}\n"
        for day in range(1, 11)
    )
    folder = tmp_path / "umbria_sir"
    folder.mkdir()
    with zipfile.ZipFile(folder / "storico_giornalieri.zip", "w") as archive:
        archive.writestr("rilevazioni.csv", header + rows)

    network = GAUGE_NETWORKS["umbria"](tmp_path, date(2025, 1, 1), date(2025, 1, 10))

    assert network.gauges["code"].tolist() == ["485400"]
    assert {"lat", "lon", "name"} <= set(network.gauges.columns)
    gauge = next(network.gauges.itertuples())
    series = network.series(gauge)
    assert series[date(2025, 1, 3)] == pytest.approx(0.3)
    days = pd.Series([1.0, 2.0], index=[date(2025, 1, 1), date(2025, 1, 2)])
    assert network.day_totals(days).tolist() == pytest.approx([1.0, 2.0])


def test_emilia_romagna_reads_arpae_gauges_on_0900_days(tmp_path) -> None:
    import gzip

    from api.weather.checks import GAUGE_NETWORKS

    line = json.dumps(
        {
            "network": "simnpr",
            "lon": 1036000,
            "lat": 4448000,
            "date": "2025-10-01T08:00:00Z",
            "data": [
                {"vars": {"B01019": {"v": "Bosco"}, "B07030": {"v": 983.0}}},
                {"timerange": [1, 0, 86400], "vars": {"B13011": {"v": 12.4}}},
            ],
        }
    )
    archive = tmp_path / "arpae" / "2025-10.json.gz"
    archive.parent.mkdir()
    with gzip.open(archive, "wt") as out:
        out.write(line + "\n")

    network = GAUGE_NETWORKS["emilia_romagna"](tmp_path, date(2025, 10, 1), date(2025, 10, 31))

    gauge = next(network.gauges.itertuples())
    assert gauge.name == "Bosco"
    assert network.series(gauge).to_dict() == {date(2025, 10, 1): 12.4}
    assert network.day_totals is gauge_day_totals
