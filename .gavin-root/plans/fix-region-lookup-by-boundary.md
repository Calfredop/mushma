---
order: 9216
title: [web] Find a point's region by its boundary, not its bbox
status: To Do
priority: medium
complexity: moderate
---
Found by the Liguria and Marche cards (`.gavin-root/docs/regions/liguria.md` and `marche.md` → Known limitations).

`findRegionAt` (web/src/regions/index.ts) and `offerOrOpen` (App.tsx) decide a point's region by bounding box, first match in registry order, current region first. Neighbouring bboxes overlap a lot: Marche's [12.18, 42.68, 13.92, 43.97] shares its whole western half with Umbria's [11.89, 42.36, 13.27, 43.62], which covers Fabriano, Camerino, Cagli, Apecchio and the Sibillini, most of Marche's woodland. So from the hub or from `/toscana`, a GPS fix or a search near Fabriano offers Umbria; inside `/umbria`, a tap there opens Umbria's forecast for a point outside Umbria's grid. Each region added makes it worse (Lazio, Abruzzo and Emilia-Romagna overlap Marche and Umbria too).

Worse in the north (Trentino-Alto Adige card, 2026-09-26): Lombardia's bbox [8.49, 44.67, 11.43, 46.64] takes in most of Trentino, Trento city included (46.07, 11.12), so once both are served a fix in Trento from the hub is offered whichever of the two comes first in the registry. Trentino-Alto Adige's own bbox [10.38, 45.67, 12.48, 47.10] takes in Belluno, Cortina and the Asiago plateau (Veneto) and Val Müstair (Switzerland).

Friuli-Venezia Giulia card (2026-09-27): its bbox [12.32, 45.58, 13.92, 46.65] takes in western Slovenia (Nova Gorica, Tolmin, Kobarid, Bovec), a strip of Carinthia, Veneto's eastern plain (Portogruaro, Caorle) and the Alpago; and Trentino-Alto Adige's bbox reaches 12.48° E, so Erto e Casso (46.27, 12.37) and Cimolais (46.29, 12.44), FVG comuni in the Val Cellina, fall inside both.

Puglia card (2026-09-28): its bbox [14.93, 39.79, 18.53, 42.23] takes in Irpinia (Bagnoli Irpino,
Bisaccia, Andretta), the Vulture and the Materano (Matera, Montescaglioso) and Molise's coast at
Termoli, which belong to Campania, Basilicata and Molise.

Sicilia card (2026-09-28): its bbox [11.92, 35.49, 15.66, 38.82] reaches 15.66° E for the
Strait, so it takes in Reggio Calabria (38.11, 15.65) and Villa San Giovanni (38.22, 15.64), while
Calabria's [15.63, 37.91, 17.21, 40.15] takes in Messina's Capo Peloro, Ganzirri and Torre Faro
(38.26, 15.64): the two regions claim each other's side of the Strait.

Lazio card (2026-09-28): its bbox [11.44, 40.78, 14.03, 42.84] shares its northern strip with
Tuscany's [9.68, 42.23, 12.38, 44.48] and Umbria's [11.89, 42.36, 13.27, 43.62]. Viterbo (42.42,
12.10), the Cimini (Soriano nel Cimino, 42.42, 12.23) and Lake Bolsena fall inside both, so from
the hub or from `/umbria` a fix there is offered Tuscany, first in the registry; Rieti (42.40,
12.86), the Terminillo and Leonessa fall inside Umbria's, so from the hub or `/toscana` they are
offered Umbria. Lazio's bbox in turn takes in Orvieto and Terni (Umbria), Pitigliano and Sorano
(Tuscany), and the Abruzzo side of the Simbruini and the Marsica (Tagliacozzo, Avezzano).

- [ ] Ship each region's simplified boundary (ISTAT 2025 generalised, simplified to ~200–500 m, a few KB per region) where the web can read it: a static GeoJSON per region built from the grid build's boundary, or the `/overview` payload the hub already fetches
- [ ] `findRegionAt` and `offerOrOpen` test point-in-polygon, with the bbox as a cheap pre-filter; keep the current-region-first rule
- [ ] Tests: a point near Fabriano (43.33, 12.90) resolves to Marche from the hub, from `/toscana` and from `/umbria`; La Spezia to Liguria; Perugia to Umbria
- [ ] Place search restricted to served regions uses the same test
