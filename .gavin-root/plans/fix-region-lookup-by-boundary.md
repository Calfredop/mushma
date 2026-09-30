---
order: 4096
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

Veneto card (2026-09-29): the worst case yet. Veneto's bbox [10.62, 44.79, 13.11, 46.68] and its
neighbours' overlap so much that no registry order works: 3,896 of Veneto's 4,025 woodland cells
(97 %) lie inside Trentino-Alto Adige's (3,263), Lombardia's (943: the Lessinia and Monte Baldo) or
Friuli-Venezia Giulia's (639: the Cansiglio, Alpago, Cadore) bboxes, and Veneto's own bbox holds
5,625 of Trentino-Alto Adige's 7,698 woodland cells (Trento, Rovereto, the Garda shore), 1,767 of
Friuli-Venezia Giulia's 3,304 (Pordenone, the Val Cellina, Piancavallo) and 145 of Lombardia's. So
Veneto is registered last (no served region regresses), and from the hub a fix or a search in
Belluno, Cortina, Asiago, Bassano, the Grappa or the Lessinia is offered Trentino-Alto Adige or
Lombardia; inside `/veneto` the current-region-first rule serves it. The simplified boundaries this
card needs already exist: `web/src/regions/boundaries.json` (every region, ISTAT 2025 simplified to
~500 m, from `api.grid.web_boundaries`), loaded lazily by the hub map.

Molise card (2026-09-30): Molise's bbox [13.94, 41.36, 15.17, 42.08] is small but sits among four
neighbours. 857 of its 1,455 woodland cells (59 %) lie inside Abruzzo's bbox (507: Agnone,
Vastogirardi, San Pietro Avellana, the whole Alto Molise), Campania's (300: the Matese side, Bojano,
Guardiaregia, Sepino), Lazio's (76: the Mainarde, Pizzone, Venafro) or Puglia's (4); and Molise's own
bbox holds 796 of Abruzzo's woodland cells (Castel di Sangro, Alfedena, Barrea, Palena), 349 of
Campania's (the Campanian Matese, Piedimonte Matese), 85 of Puglia's (the Monti Dauni north of
Celenza Valfortore) and 74 of Lazio's (Vallerotonda, San Biagio Saracinisco). So Molise is registered
last, as Veneto is: from the hub a fix or a search in Agnone or Capracotta is offered Abruzzo, on the
Molise Matese Campania; inside `/molise` the current-region-first rule serves it.

Basilicata card (2026-09-30): Basilicata's bbox [15.33, 39.89, 16.87, 41.14] lies wholly inside
Puglia's [14.93, 39.79, 18.53, 42.23], so registered last it would never be found from the hub. 800 of
its 2,545 woodland cells also lie inside Campania's bbox (lon ≤ 15.81: Potenza itself, the Vulture,
the Sellata, Muro Lucano) and 707 inside Calabria's (lat ≤ 40.15: the Lucanian Pollino, the Sirino,
Lauria, Maratea); its own bbox holds 1,004 of Campania's woodland cells (Vallo di Diano, eastern
Irpinia), 361 of Calabria's (the Calabrian Pollino, Rocca Imperiale) and 114 of Puglia's (the Murge
round Altamura and Gravina in Puglia). Registered after Calabria and before Puglia, the hub finds
Basilicata for 1,134 of its woodland cells (Matera, the Val d'Agri, Gallipoli Cognato, the Ionian
coast) and Campania and Calabria keep all theirs; Puglia's Altamura and Gravina go to Basilicata. From
the hub a fix in Potenza is offered Campania and one on the Lucanian Pollino Calabria; inside
`/basilicata` the current-region-first rule serves all of it.

- [ ] Ship each region's simplified boundary (ISTAT 2025 generalised, simplified to ~200–500 m, a few KB per region) where the web can read it: a static GeoJSON per region built from the grid build's boundary, or the `/overview` payload the hub already fetches
- [ ] `findRegionAt` and `offerOrOpen` test point-in-polygon, with the bbox as a cheap pre-filter; keep the current-region-first rule
- [ ] Tests: a point near Fabriano (43.33, 12.90) resolves to Marche from the hub, from `/toscana` and from `/umbria`; La Spezia to Liguria; Perugia to Umbria
- [ ] Place search restricted to served regions uses the same test
