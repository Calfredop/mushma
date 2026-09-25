---
order: 19456
title: [model] Rain calibration without steps at region borders
status: To Do
priority: medium
complexity: moderate
---
Found by the Umbria card (`.gavin-root/docs/regions/umbria.md` → Validation → "Known issue: a step at the Tuscan border").

Each region scales the reanalysis rain with its own region-wide gauge fit (`model.precipitation_scale`): Tuscany 1.28 + 0.29/km (SIR gauges, `era5_seamless`), Umbria 0.89 + 0.33/km (Servizio Idrografico gauges, CDS), Liguria 1.04 + 0.20/km (ARPAL, CDS). The reanalysis products agree (CDS vs `era5_seamless` rain pooled 0.995, Tuscany 2024); the gauge networks don't (Tuscany reads the reanalysis at 0.63–0.79 of gauge rain, Umbria about 0.9–1.1). The same raw rain is therefore scaled ×1.41 on the Tuscan side of the border and ×0.99 on the Umbrian side 12 km away. On 2026-09-25 the border band scored 0.86 vs 0.47 (combined) and 0.47 vs 0.07 (porcini), a visible step on the hub map.

- [ ] Decide the shape: one national fit, per climate zone, or a smooth per-node factor from every region's open gauges (SIR Toscana, ARPAL, Umbria's Servizio Idrografico, …)
- [ ] Fit it with the gauge networks in `api.weather.checks` (`GAUGE_NETWORKS`), all gauges rather than woodland-only where a region has few (Umbria has 8 in woodland, 82 overall)
- [ ] Also: Tuscany's local store holds CDS rows for 2024 that outrank `era5_seamless` and are not in the national `precipitation_scale.sources`, so they go unscaled (check whether the server has them)
- [ ] Re-score the affected regions; record before/after at the Tuscany–Umbria and Tuscany–Liguria borders
- [ ] Regions without open daily gauges get their factor from the fit too: Marche (`marche.yaml`) borrows the mean of Umbria's and Emilia-Romagna's CDS fits, 0.76 + 0.57/km, until then (`.gavin-root/docs/regions/marche.md` → Weather)
