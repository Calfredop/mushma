"""INFC 2015 bosco area table (ha) keyed by region slug."""

from pathlib import Path

import yaml

INFC_FILE = Path(__file__).resolve().parent.parent / "config" / "infc2015.yaml"


def load_infc_bosco(path: Path = INFC_FILE) -> dict[str, int]:
    """Region slug → bosco area in hectares from the 2015 national inventory."""
    raw = yaml.safe_load(path.read_text())
    return {str(k): int(v) for k, v in raw["bosco_ha"].items()}
