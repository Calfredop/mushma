---
order: 13312
kind: note
labels: memory
title: A CDS region's rain scale must list era5_land_cds
status: To Do
---
Superseded 2026-10-01: the rain scale is now one national field (`model.yaml → precipitation_scale.field`) whose `sources` list `era5_land_cds` and `era5_seamless`; regions set no `model.precipitation_scale` block (`.gavin-root/docs/rain-scale-field.md`). Do not adopt; archive.

Was: Every region whose history is CDS sets `model.precipitation_scale` in its YAML with `sources: [era5_land_cds, era5_seamless]` (a gauge fit, or `enabled: false` until one exists); never leave it to the national block.

Why: scoring multiplies the rain normals by the scale whatever their source but the daily rain only for the listed sources (`api/src/api/model/inputs.py`, `load_weather`), and the national block lists `era5_seamless` only, so a CDS region without its own block would read its 30-day rain against normals 1.3-1.6 times too wet (found on the Sicilia card, 2026-09-28).
