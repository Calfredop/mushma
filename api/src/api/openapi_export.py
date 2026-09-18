"""Renders the FastAPI app's OpenAPI schema; used by scripts/export_openapi.py
and by the contract test that checks the checked-in file is current."""

import json
from pathlib import Path

from api.main import app

OPENAPI_JSON_PATH = Path(__file__).resolve().parent.parent.parent / "openapi.json"


def render_openapi_json() -> str:
    return json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n"


def main() -> None:
    OPENAPI_JSON_PATH.write_text(render_openapi_json())
