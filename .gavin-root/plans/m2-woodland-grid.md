---
order: 4
title: M2 · Woodland grid: 1 km cells with habitat and terrain
status: To Do
priority: high
complexity: complex
---
Traces to PRD → Architecture (Grid), Candidate data sources, Milestone 2.
Depends on: M1 Foundations.

The static layer every score sits on: which ~1 km cells in Tuscany are woodland, and what kind of woodland and terrain they have. Write tests first for every transform (AGENTS.md). Source data goes under the gitignored `api/data/`, fetched by a script.

- [ ] Region config: Tuscany boundary (ISTAT), bbox, grid CRS EPSG:3035, 1 km cell size. Keep the region swappable.
- [ ] Generate the 1 km EPSG:3035 grid clipped to Tuscany, with stable cell ids (EEA reference grid naming)
- [ ] Pick the forest source by comparing Regione Toscana forest/land-use maps (Geoscopio), Corine Land Cover and Copernicus HRL Forest Type on detail, license and forest-type classes (castagneti, faggete, cerrete, conifers...)
- [ ] Forest mask: define and test the "mostly woodland" threshold per cell
- [ ] Forest type per cell: dominant type + fractions, mapped to a small habitat vocabulary the species rules can use
- [ ] Terrain per cell from DEM (TINITALY or Copernicus GLO-30): mean elevation, slope, aspect
- [ ] Optional: soil pH/type per cell from SoilGrids or the Regione Toscana pedological map (PRD → Known gaps). Only if cheap; otherwise leave a note on how to add it later.
- [ ] Place label per cell (comune from ISTAT + nearest named place) for hotspots, area aggregation and search
- [ ] Persist the grid to the chosen storage and export a WGS84 version for the map
- [ ] Sanity check: cell count, woodland share of Tuscany vs published figures, spot-check known forests (Casentino, Amiata, Garfagnana)
