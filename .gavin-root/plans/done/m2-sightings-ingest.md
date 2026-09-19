---
order: 6
title: M2 · Sightings ingest: GBIF + iNaturalist
status: Done
priority: high
complexity: moderate
---
Traces to PRD → Model (Validation, Known data traps), Features 4 (hotspots) and 6 (history), Milestone 2.
Depends on: M1 Foundations. Joining sightings to cells needs M2 Woodland grid.

Sightings serve two purposes: ground truth for the backtest, and the "recent sightings" signal on the hotspots list. Write tests first for parsers and filters.

- [x] Resolve GBIF taxon keys: *Boletus edulis* group (edulis, aereus, aestivalis/reticulatus, pinophilus), *Amanita caesarea*, *Cantharellus cibarius*
- [x] GBIF occurrence client for Tuscany: date, coordinates, coordinate uncertainty, basis of record, dataset key, license
- [x] iNaturalist client for the most recent records (days, not months), deduplicated against GBIF
- [x] Quality filters: drop records whose coordinate uncertainty or geoprivacy obscuring is too coarse for 1 km cells; drop records with missing dates; flag records that sit at a town centroid
- [x] Store sightings with cell id, species key, source/license and an obscured flag. Only counts per cell ever leave the database (PRD → Sightings privacy).
- [x] Profile the data: counts per species, year and month; spatial bias map (near roads/towns); write findings to `.gavin-root/docs/sightings-profile.md`
- [x] Record the attribution each dataset's license requires, for the credits page
