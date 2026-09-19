---
kind: note
labels: memory
title: MapLibre 6 must be served verbatim, not bundled
status: To Do
---
Never let Vite pre-bundle or re-bundle `maplibre-gl` 6: keep it in `optimizeDeps.exclude` and served from `/vendor/maplibre-gl-<version>/` in builds (`web/vite.config.ts` → `vendorMaplibre`).

Why: MapLibre 6 starts its web worker from `maplibre-gl-worker.mjs` next to its own module; once bundled, the worker URL breaks (or the bundled copy and the worker disagree) and the map silently never fires `load`, with no console error.
