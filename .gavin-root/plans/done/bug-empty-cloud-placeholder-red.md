---
kind: task
title: [bug] empty cloud placeholder tints the region red
status: Done
priority: medium
complexity: trivial
---
`EMPTY_CLOUD_DATA_URL` in `web/src/map/cloudRaster.ts` (from commit 9df9b29) is documented as a "tiny transparent PNG", but its one pixel decodes to RGBA (255, 0, 0, 127): half-transparent red. The `cells-cloud-raster` image source stretches it over the region bounds whenever no cloud is drawn (scores still loading, the API down, a day with no cells), so the whole region shows a flat red-pink tint. It also hides the satellite view while scores load.

Repro: run `pnpm dev` with no API on :8000 and open /toscana: the map is red until scores arrive (they never do).

Fix: replace it with a fully transparent 1×1 PNG (alpha 0), and add a test that decodes the placeholder and checks alpha is 0.
