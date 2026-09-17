"""Writes the FastAPI app's OpenAPI schema to api/openapi.json.

The checked-in file is the contract web/'s generated TypeScript client is
built from. Run after changing any route or response model:

    uv run python scripts/export_openapi.py

`tests/test_openapi_contract.py::test_openapi_json_is_up_to_date` fails CI if
this drifts from the app.
"""

from api.openapi_export import main

if __name__ == "__main__":
    main()
