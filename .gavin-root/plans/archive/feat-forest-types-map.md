---
kind: task
title: [feat] forest types on the map (analysis mode)
status: Done
complexity: moderate
---
In analysis mode, let the map show each woodland cell's forest type (tipo di bosco): faggeta, castagneto, cerreta, abetina and so on, so a forager can see what the woods are, not only how well they suit a species.

## What exists

- Analysis mode draws the species' factors from `GET /factors`, one chip per factor, each shown as the factor's 0–1 value (opacity) in its family colour (`web/src/score/indicators.ts`, `web/src/components/IndicatorPanel.tsx`). The `habitat` chip shows the species' *fit* to the woods, not the woods themselves.
- Grid data (`api/data/grid/tuscany/`): `cell_habitats.parquet` holds `(cell_id, habitat, fraction)` per cell. `cells.parquet` has `dominant_habitat` and `dominant_fraction`. The grid build already writes `cells_wgs84.geojson` with `dominant_habitat`, but no route serves it.
- The forest-type vocabulary (14 types) is in `api/src/api/config/habitats.yaml`.
- Commit 3b04ae6 (card `feat-tipo-di-bosco`) added the parts to reuse:
  - it/en names for every type under `forest.types.*`;
  - the `HabitatShare` model on `/spot` and `/cells/{id}`;
  - `forestMix` in `web/src/score/habitats.ts` and the `useForestTypes` hook.

## To decide (with the human, before building)

- **What to show:** the dominant type per cell only, or the mix (e.g. the dominant type with its share as opacity).
- **Where it sits:** a separate "Bosco" layer toggle next to the factor chips, or a chip among them. The data doesn't depend on the species or the day, unlike every chip today.
- **Colours:** 14 categorical colours that stay readable over the basemap and hillshade and pass the colour-blindness check in `.gavin-root/docs/visual-direction.md` → Analysis mode. Grouping them by broad group (broadleaf, conifer, mixed, macchia, transitional) is an option.
- **Delivery:** a new static route cached like `/comuni` (it changes only when the grid is rebuilt), or the existing `cells_wgs84.geojson`. Keep the whole-region payload well under the PRD's ~1 MB compressed budget.

## Conventions

- Build the API route test-first, with a contract test.
- Regenerate `api/openapi.json` and `web/src/api/schema.ts`.
- Put every string through i18n, in both it and en.
- Add a legend for the types.
- Never make edibility claims.
- Credits don't change: the data comes from the same forest and land-cover sources.
