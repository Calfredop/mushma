---
title: [deploy] The API image cannot import rasterio (libexpat.so.1 missing)
status: To Do
priority: low
complexity: simple
---
Found on 2026-10-01 while re-scoring history on the server for `fix-rain-calibration-region-borders.md`. Inside the production API container (`docker compose run --rm api python …` in `/opt/mushma/deploy`), any import that reaches `rasterio` fails:

```
File "/app/src/api/regions/onboard.py", line 28, in <module>
  from api.grid.forest import INFC_TOLERANCE, compare_infc_bosco, forest_area_ha
File "/app/src/api/grid/forest.py", line 10, in <module>
  import rasterio.features
File "/app/.venv/lib/python3.13/site-packages/rasterio/__init__.py", line 25, in <module>
  from rasterio._base import DatasetBase
ImportError: libexpat.so.1: cannot open shared object file: No such file or directory
```

The image is `ghcr.io/astral-sh/uv:python3.13-bookworm-slim` (`api/Dockerfile`), and the slim Debian base has no `libexpat1`. The rasterio wheel bundles GDAL but links the system expat. The `grid` dependency group is a default group (`pyproject.toml → default-groups`), so `uv sync --no-dev` installs rasterio anyway.

**Impact today:** none on serving. The API, the daily job, scoring and the history build never import rasterio. But on the server you cannot run `api.regions.onboard`, `api.grid.*`, or anything importing them (for example `onboard.history_score_range`). Today's re-score script had to work around it.

- [ ] Decide: install the library (`RUN apt-get update && apt-get install -y --no-install-recommends libexpat1 && rm -rf /var/lib/apt/lists/*` before `uv sync`), or keep the grid tooling out of the server image (`uv sync --no-group grid`, which saves image size; then onboarding stays a laptop job by design, so say so in the README)
- [ ] Add a check that fails the deploy if the chosen state breaks: for example `docker compose run --rm api python -c "import rasterio"` in `deploy/deploy-api.sh` if rasterio is kept, or a test that the served routes never import `api.grid.forest` if it is dropped
- [ ] Deploy and confirm on the server with the same command that failed: `docker compose run --rm -T api python -c "import api.regions.onboard"`
