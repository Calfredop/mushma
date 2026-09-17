---
order: 9
title: M5 · Frontend core: map, spot forecast, why, hotspots
status: To Do
priority: medium
complexity: complex
---
Traces to PRD → Features 1–4 and 8, Audience (friends + portfolio), Principles (honest uncertainty, sightings privacy), Constraints (cost, mobile performance), Open questions (basemap), Milestone 5.
Depends on: M4 API contract + fixtures. Build against fixture mode, in parallel with M2/M3; real data arrives with M4 API.

Mobile-first, portfolio-quality visuals. All strings go through i18n with Italian as the default (AGENTS.md). Call it a "conditions score", never a probability or "% chance".

- [ ] Visual direction with the frontend-design skill: identity, palette, a score color scale that works in sunlight and for colorblind users
- [ ] Decide the basemap provider (MapTiler, self-hosted Protomaps PMTiles, or OSM-based): cost against the ~€10/month ceiling, terms, offline caching allowed? Record it in the PRD.
- [ ] i18n setup (it default, en complete), language switcher, and a check that fails on missing keys
- [ ] Map: MapLibre with the woodland conditions-score layer, species switcher (porcini / ovoli / gallinacci / combined) and legend
- [ ] Date control: past days → today → +7, with forecast days visibly marked as forecast
- [ ] Spot forecast panel: tap a cell, search a place, or use GPS → per-species score plus 7-day outlook
- [ ] "Why this score" breakdown component driven by the API's factor list
- [ ] Hot places now: ranked list linked to the map, plus a per-cell recent-sightings overlay (counts, never points)
- [ ] Disclaimer (conditions only, never edibility or identification) and a data credits page
- [ ] Performance check on a mid-range phone over throttled 4G: first map paint under ~3 s
- [ ] Tests: Vitest for components with logic; one end-to-end smoke test of map → spot → why
