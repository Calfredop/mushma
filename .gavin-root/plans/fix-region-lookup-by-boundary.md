---
title: [web] Find a point's region by its boundary, not its bbox
status: To Do
priority: medium
complexity: moderate
---
Found by the Liguria and Marche cards (`.gavin-root/docs/regions/liguria.md` and `marche.md` → Known limitations).

`findRegionAt` (web/src/regions/index.ts) and `offerOrOpen` (App.tsx) decide a point's region by bounding box, first match in registry order, current region first. Neighbouring bboxes overlap a lot: Marche's [12.18, 42.68, 13.92, 43.97] shares its whole western half with Umbria's [11.89, 42.36, 13.27, 43.62], which covers Fabriano, Camerino, Cagli, Apecchio and the Sibillini, most of Marche's woodland. So from the hub or from `/toscana`, a GPS fix or a search near Fabriano offers Umbria; inside `/umbria`, a tap there opens Umbria's forecast for a point outside Umbria's grid. Each region added makes it worse (Lazio, Abruzzo and Emilia-Romagna overlap Marche and Umbria too).

- [ ] Ship each region's simplified boundary (ISTAT 2025 generalised, simplified to ~200–500 m, a few KB per region) where the web can read it: a static GeoJSON per region built from the grid build's boundary, or the `/overview` payload the hub already fetches
- [ ] `findRegionAt` and `offerOrOpen` test point-in-polygon, with the bbox as a cheap pre-filter; keep the current-region-first rule
- [ ] Tests: a point near Fabriano (43.33, 12.90) resolves to Marche from the hub, from `/toscana` and from `/umbria`; La Spezia to Liguria; Perugia to Umbria
- [ ] Place search restricted to served regions uses the same test
