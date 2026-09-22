---
order: 11
title: M7 · PWA, offline and launch polish
status: Done
priority: medium
complexity: moderate
---
Traces to PRD → Features 7 (offline/PWA), Audience (field use + portfolio), Out of scope (no native apps, so the PWA fills that role), Milestone 7.
Depends on: M5 Frontend core. It can run in parallel with M6.

- [x] vite-plugin-pwa: manifest, icons and an install prompt
- [x] Offline caching: app shell, latest scores, spot forecasts for recently viewed places, and basemap tiles for the viewed area (only if the provider's terms allow it)
- [x] "Last updated" timestamp and an offline indicator; stale-data warning when the forecast is old
- [x] Field UX pass: sunlight contrast, one-handed use, low-signal loading states
- [x] Credits page complete: Open-Meteo, GBIF datasets, iNaturalist, Copernicus/Corine or Regione Toscana, DEM source, ISTAT, basemap
- [x] Production hardening: error tracking, uptime and daily-job monitoring, API rate limiting
- [x] Portfolio README: screenshots/GIF, method write-up, validation results from M3 (M3's tuning/hold-out numbers aren't in yet — blocked on the weather backfill; the README links the live validation doc and states that plainly rather than guessing at numbers)
