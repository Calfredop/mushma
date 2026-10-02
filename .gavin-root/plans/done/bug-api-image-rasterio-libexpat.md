---
title: [deploy] The API image cannot import rasterio (libexpat.so.1 missing)
status: Done
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

- [x] Decide: install the library (`RUN apt-get update && apt-get install -y --no-install-recommends libexpat1 && rm -rf /var/lib/apt/lists/*` before `uv sync`), or keep the grid tooling out of the server image (`uv sync --no-group grid`, which saves image size; then onboarding stays a laptop job by design, so say so in the README)
  Decision: install `libexpat1`. `--no-group grid` is not an option: `import api.main` loads geopandas, pyproj and shapely (all in the `grid` group), so the served API needs the group. Only rasterio is unused when serving, and splitting it into its own group would save a few MB for more churn. Keeping it also lets the server run `api.regions.onboard` and `history_score_range`. Reproduced locally with `docker build` (the `import rasterio` failure from the card) and confirmed the fix: after the change `import rasterio` and `import api.regions.onboard` both work in the rebuilt image.
- [x] Add a check that fails the deploy if the chosen state breaks: for example `docker compose run --rm api python -c "import rasterio"` in `deploy/deploy-api.sh` if rasterio is kept, or a test that the served routes never import `api.grid.forest` if it is dropped
  Done: `deploy/deploy-api.sh` runs `docker compose exec -T api python -c "import api.regions.onboard"` (after the Redis check, `</dev/null` because of the stdin note in that script) and exits 1 with a pointer to `api/Dockerfile` if it fails, so the "server: done" guard fires.
- [x] Deploy and confirm on the server with the same command that failed: `docker compose run --rm -T api python -c "import api.regions.onboard"`
  Done 2026-10-02: fix committed as `0beb997` and deployed with `deploy/deploy-api.sh` (the new "checking the grid tooling imports" step passed, smoke tests 200). On the server, `docker compose run --rm -T api python -c "import api.regions.onboard, rasterio"` in `/opt/mushma/deploy` now prints `onboard ok, rasterio 1.5.1`.
- [x] Decision: The libexpat1 fix (api/Dockerfile) and the new import check (deploy/deploy-api.sh) are ready, uncommitted. May I commit them, push main to origin and run deploy/deploy-api.sh to production, then confirm `docker compose run --rm -T api python -c "import api.regions.onboard"` on the server?
  Options: A) Yes, commit, push and deploy B) Commit and push only, I will deploy C) No, leave it uncommitted
  Answer (2026-10-02): Yes, commit, push and deploy
