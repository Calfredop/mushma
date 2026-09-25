"""Compare CDS daily history against stored Open-Meteo era5_seamless for one year.

    uv run python -m api.weather.checks cds_vs_seamless --region tuscany --year 2024

Writes RMSE / bias per variable to stdout and under ``checks/cds_vs_seamless_<year>.json``.
Tolerances (from weather-history-cds.md): temperatures ~0.3 °C RMSE,
wet 3-day rain r ≥ 0.95, ET0 and VPD within ~10 %.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from api.weather.cds import SOURCE_ID
from api.weather.ingest import region_paths
from api.weather.store import WeatherStore

TEMP_VARS = (
    "temperature_2m_min",
    "temperature_2m_max",
    "temperature_2m_mean",
    "soil_temperature_0_to_7cm_mean",
)
RAIN = "precipitation_sum"
PCT_VARS = ("et0_fao_evapotranspiration", "vapour_pressure_deficit_max")


def _load_year(store: WeatherStore, source: str, year: int) -> pd.DataFrame:
    path = store.partition_path(source, year)
    if not path.exists():
        raise FileNotFoundError(f"missing {path}")
    return pd.read_parquet(path)


def compare_year(store: WeatherStore, year: int) -> dict:
    cds = _load_year(store, SOURCE_ID, year)
    seamless = _load_year(store, "era5_seamless", year)
    merged = cds.merge(
        seamless,
        on=["point_id", "date", "variable"],
        suffixes=("_cds", "_om"),
        how="inner",
    )
    if merged.empty:
        raise RuntimeError(f"no overlapping rows for {year} between {SOURCE_ID} and era5_seamless")

    report: dict = {"year": year, "rows": len(merged), "variables": {}}
    for variable, group in merged.groupby("variable"):
        a = group["value_cds"].to_numpy(dtype=float)
        b = group["value_om"].to_numpy(dtype=float)
        mask = np.isfinite(a) & np.isfinite(b)
        a, b = a[mask], b[mask]
        if len(a) == 0:
            continue
        bias = float(np.mean(a - b))
        rmse = float(np.sqrt(np.mean((a - b) ** 2)))
        entry: dict = {"n": int(len(a)), "bias": bias, "rmse": rmse}
        if variable == RAIN:
            # Wet 3-day totals: roll sum per point, keep windows with OM ≥ 10 mm.
            frame = group.assign(date=pd.to_datetime(group["date"])).sort_values(
                ["point_id", "date"]
            )
            rolls = []
            for _, part in frame.groupby("point_id"):
                part = part.set_index("date").sort_index()
                cds3 = part["value_cds"].rolling("3D").sum()
                om3 = part["value_om"].rolling("3D").sum()
                wet = om3 >= 10.0
                if wet.any():
                    rolls.append(pd.DataFrame({"cds": cds3[wet], "om": om3[wet]}))
            if rolls:
                wet = pd.concat(rolls)
                entry["wet_3d_r"] = float(wet["cds"].corr(wet["om"]))
                entry["wet_3d_n"] = int(len(wet))
        if variable in PCT_VARS:
            denom = np.maximum(np.abs(b), 1e-6)
            entry["mean_abs_pct"] = float(np.mean(np.abs(a - b) / denom) * 100.0)
        report["variables"][variable] = entry

    report["pass"] = _judge(report)
    return report


def _judge(report: dict) -> dict:
    """Apply the spike-doc tolerances; return per-check bools."""
    checks = {}
    vars_ = report["variables"]
    for name in TEMP_VARS:
        if name in vars_:
            checks[f"{name}_rmse_le_0.3"] = vars_[name]["rmse"] <= 0.3
    if RAIN in vars_ and "wet_3d_r" in vars_[RAIN]:
        checks["rain_wet_3d_r_ge_0.95"] = vars_[RAIN]["wet_3d_r"] >= 0.95
    for name in PCT_VARS:
        if name in vars_ and "mean_abs_pct" in vars_[name]:
            checks[f"{name}_pct_le_10"] = vars_[name]["mean_abs_pct"] <= 10.0
    checks["all"] = all(checks.values()) if checks else False
    return checks


def main_compare(region: str, year: int) -> Path:
    _, store, _ = region_paths(region)
    report = compare_year(store, year)
    out_dir = store.root / "checks"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"cds_vs_seamless_{year}.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return path
