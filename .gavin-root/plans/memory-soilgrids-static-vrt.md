---
order: 17408
kind: note
title: SoilGrids' WCS times out on a whole region; its static VRT does not
status: To Do
labels: memory
---
When `api.grid.build` fails on SoilGrids with HTTP 503, warp the three `phh2o` layers from `/vsicurl/https://files.isric.org/soilgrids/latest/data/phh2o/phh2o_<depth>_mean.vrt` into the cached `raw/soilgrids/<region>/phh2o_<depth>_mean.tif` (EPSG:4326, int16, 0 = no data, ~0.00226° pixels) and rerun the build; it takes seconds a layer.

Why: on 2026-09-28 the WCS answered 503 (a gateway timeout) for Calabria's whole bbox all morning while small requests passed; the static COGs behind it matched the WCS output within 0.02-0.04 pH (regions/calabria.md, Woodland grid).
