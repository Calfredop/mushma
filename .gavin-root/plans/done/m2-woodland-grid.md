---
order: 4
title: M2 · Woodland grid: 1 km cells with habitat and terrain
status: Done
priority: high
complexity: complex
---
Traces to PRD → Architecture (Grid), Candidate data sources, Milestone 2.
Depends on: M1 Foundations.

The static layer every score sits on: which ~1 km cells in Tuscany are woodland, and what kind of woodland and terrain they have. Write tests first for every transform (AGENTS.md). Source data goes under the gitignored `api/data/`, fetched by a script.

- [x] Region config: Tuscany boundary (ISTAT), bbox, grid CRS EPSG:3035, 1 km cell size. Keep the region swappable.
- [x] Generate the 1 km EPSG:3035 grid clipped to Tuscany, with stable cell ids (EEA reference grid naming)
- [x] Pick the forest source by comparing Regione Toscana forest/land-use maps (Geoscopio), Corine Land Cover and Copernicus HRL Forest Type on detail, license and forest-type classes (castagneti, faggete, cerrete, conifers...)
- [x] Forest mask: define and test the "mostly woodland" threshold per cell
- [x] Forest type per cell: dominant type + fractions, mapped to a small habitat vocabulary the species rules can use
- [x] Terrain per cell from DEM (TINITALY or Copernicus GLO-30): mean elevation, slope, aspect
- [x] Optional: soil pH/type per cell from SoilGrids or the Regione Toscana pedological map (PRD → Known gaps). Only if cheap; otherwise leave a note on how to add it later.
- [x] Place label per cell (comune from ISTAT + nearest named place) for hotspots, area aggregation and search
- [x] Persist the grid to the chosen storage and export a WGS84 version for the map
- [x] Sanity check: cell count, woodland share of Tuscany vs published figures, spot-check known forests (Casentino, Amiata, Garfagnana)
