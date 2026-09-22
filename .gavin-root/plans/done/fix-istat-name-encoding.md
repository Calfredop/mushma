---
order: 1024
kind: task
title: Grid · Fix mojibake in ISTAT comune and locality names
status: Done
priority: medium
complexity: simple
---
Traces to PRD → Architecture (Areas: hotspots are labelled by comune and nearest named place) and Milestone 4.

Found by M3 · Model v1 on 2026-09-17 while defining sanity-check areas. In `api/data/grid/tuscany/cells.parquet`, UTF-8 names from the ISTAT shapefiles were decoded as Latin-1:

- 2 comuni: `Castel San NiccolÃ²` (Castel San Niccolò), `Castelfranco PiandiscÃ²` (Castelfranco Piandiscò)
- 36 `place_name` localities, e.g. `Campiglio di SammommÃ¨`, `CÃ  Raffaello`, `ComunitÃ  di recupero sociale Emmaus`

`name.encode("latin-1").decode("utf-8")` recovers them, which confirms the cause. The readers are in `api/src/api/grid/places.py` (`gpd.read_file` of the ISTAT boundaries zip and the Basi territoriali localities), which pass no encoding.

Write a failing test first (a shapefile fixture with an accented name, read back intact), fix the reader (e.g. `encoding="utf-8"`, or honour the `.cpg`), rebuild the grid (`uv run python -m api.grid.build --region tuscany`, about 1.5 min warm), and check that `cells.parquet` and `cells_wgs84.geojson` have no `Ã`/`Â` left. Sightings' `flag_near_localities` reads the same localities but only uses geometry, so it is unaffected. Hotspot labels (M4) would show the broken names until this lands.
