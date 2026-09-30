---
order: 20480
kind: task
title: [bug] map label says Toscana on every region
status: Done
priority: low
complexity: simple
---
The conditions map's accessible label is hard-coded to Tuscany: `map.label` is "Mappa dell'indice delle condizioni in Toscana" (it.json) / "Map of conditions scores across Tuscany" (en.json), used by `web/src/map/ConditionsMap.tsx` as the map region's `aria-label`. On /piemonte, /umbria, etc. screen readers announce the map as Tuscany's.

Make the label take the active region (interpolate the region's name, using `regionLocative` for Italian prepositions like "nelle Marche"), keep it/en complete, and cover it with a light test.
