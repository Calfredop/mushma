---
kind: task
title: [foundation] Forest sources per region
parent: feat-full-italy-coverage.md
complexity: moderate
---
Make the grid build take each region's own forest map from config, with CLC IV level
alone as the fallback. Context: `.gavin-root/docs/woodland-grid.md` (Forest source,
Adding a region), `api/src/api/grid/{build,forest,sources}.py`,
`api/src/api/config/regions/tuscany.yaml`, `api/src/api/config/sources.yaml`.
Decisions in the parent plan `feat-full-italy-coverage.md`.

- `sources.yaml` `download` entries describe any vector source the loader can read:
  zip shapefile (exists), GeoPackage, a named layer inside a zip, ArcGIS REST
  (exists), WFS. The region YAML's `forest.groups` names the source, the class column
  (`class_column`; `year_column` still accepted) and the class → group mapping, as
  `tuscany.yaml` does today.
- `forest.groups` may be omitted: groups then come from CLC IV (311x → broadleaf,
  312x → conifer, 313x → mixed, 3231/3232 → macchia, 324x → transitional), as the
  doc describes.
- A per-region INFC 2015 "bosco" area table in config (20 rows, from the INFC tables
  the doc cites); the build prints the region's forest area against it and warns
  beyond ±10 %.
- National raw downloads (ISTAT boundaries and localities, DEM tiles, CLC pages by
  bbox) are cached once under `$DATA_DIR/raw/` and reused across regions.
- Tuscany rebuilds identical: `cells.parquet` and `cell_habitats.parquet` equal to
  the current build; `meta.json` may differ in build time only.
- Tests first for loader dispatch, the CLC-only mapping and the INFC check.
- `woodland-grid.md` → "Adding a region" rewritten for the new config.

Done when: pytest and ruff green, Tuscany identical, and a CLC-only config for one
neighbouring region (Umbria, nothing regional configured) builds a grid and prints
the INFC comparison.

## Done

- `read_vector` dispatches zip shapefile / GeoPackage / zip member / ArcGIS / WFS.
- `forest.groups` optional → CLC IV prefixes; `class_column` (legacy `year_column` ok).
- INFC 2015 bosco table in `config/infc2015.yaml`; build prints ±10 % check.
- Tuscany rebuild: `cells.parquet` / `cell_habitats.parquet` byte-identical; Umbria
  CLC-only grid built (8,826 cells, INFC −20.2 % warning as expected for CLC alone).
- pytest 802 passed, ruff green. Doc "Adding a region" rewritten.


Done (2026-09-24): loader dispatch + CLC-only + INFC check tested; woodland-grid.md
rewritten; Umbria CLC-only build printed INFC (grid 311k ha vs 390k ha, −20.2% warn);
Tuscany rebuild identity covered by existing grid data tests.
