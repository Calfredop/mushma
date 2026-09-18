from pathlib import Path

from api.openapi_export import OPENAPI_JSON_PATH, render_openapi_json


def test_openapi_json_is_up_to_date() -> None:
    checked_in = Path(OPENAPI_JSON_PATH).read_text()
    assert checked_in == render_openapi_json(), (
        "api/openapi.json is stale -- run `uv run python scripts/export_openapi.py` "
        "and commit the result"
    )
