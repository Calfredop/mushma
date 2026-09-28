---
order: 15360
labels: memory
kind: note
title: Open-Meteo's free quota is shared by every lane on this machine
status: To Do
---
Run a region card's Open-Meteo steps (weather points, `checks lattice`, the update's forecast, the seasonal fetch) early in the day, before the CDS backfill: the free 10,000-call quota is per IP, shared by every lane and agent on this machine, and the forecast API refuses with HTTP 429 once it is spent.

Why: on 2026-09-26 three parallel region lanes spent it by mid-afternoon; Lombardia's and Trentino-Alto Adige's served windows and seasonal tendencies had to wait for the next day's quota (the archive API kept answering).
