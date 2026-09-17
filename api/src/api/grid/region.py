"""Region config: which area the grid covers and on what grid.

A region is one YAML file in ``config/regions/`` inside this package. Everything region-specific
(boundary, bbox, grid, and the data sources used to describe its cells) lives there, so another
region can be added by writing a new file rather than changing code.
"""

from dataclasses import dataclass
from pathlib import Path

import yaml
from pyproj import CRS

REGIONS_DIR = Path(__file__).resolve().parent.parent / "config" / "regions"


@dataclass(frozen=True)
class GridSpec:
    crs: str
    cell_size_m: int


@dataclass(frozen=True)
class BoundarySpec:
    source: str
    region_code: int


@dataclass(frozen=True)
class RegionConfig:
    id: str
    name: dict[str, str]
    timezone: str
    bbox_wgs84: tuple[float, float, float, float]
    grid: GridSpec
    boundary: BoundarySpec
    extra: dict


def load_region(name_or_path: str | Path) -> RegionConfig:
    """Load a region by name (``"tuscany"``) or from a YAML file path."""
    path = Path(name_or_path)
    if path.suffix not in {".yaml", ".yml"}:
        path = REGIONS_DIR / f"{name_or_path}.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"no region config for {name_or_path!r} at {path}")

    raw = yaml.safe_load(path.read_text())
    lon_min, lat_min, lon_max, lat_max = (float(v) for v in raw["bbox_wgs84"])
    if not (lon_min < lon_max and lat_min < lat_max):
        raise ValueError(f"bbox_wgs84 must be [lon_min, lat_min, lon_max, lat_max], got {raw}")

    grid = GridSpec(crs=str(raw["grid"]["crs"]), cell_size_m=int(raw["grid"]["cell_size_m"]))
    if grid.cell_size_m <= 0:
        raise ValueError(f"grid.cell_size_m must be positive, got {grid.cell_size_m}")
    if not CRS.from_user_input(grid.crs).is_projected:
        raise ValueError(f"grid.crs must be a projected CRS (metres), got {grid.crs}")

    known = {"id", "name", "timezone", "bbox_wgs84", "grid", "boundary"}
    return RegionConfig(
        id=str(raw["id"]),
        name=dict(raw["name"]),
        timezone=str(raw["timezone"]),
        bbox_wgs84=(lon_min, lat_min, lon_max, lat_max),
        grid=grid,
        boundary=BoundarySpec(
            source=str(raw["boundary"]["source"]),
            region_code=int(raw["boundary"]["region_code"]),
        ),
        extra={k: v for k, v in raw.items() if k not in known},
    )
