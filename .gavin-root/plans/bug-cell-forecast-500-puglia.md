---
kind: task
title: [bug] Spot and cell forecasts must not 500 when a cell has no factor row
status: To Do
priority: medium
complexity: moderate
---
On 2026-09-29, from the 03:00 UTC daily run until a manual re-score at 12:41-12:54 UTC, some Puglia woodland cells failed every forecast request. Tapping one in the app showed "Non riesco a caricare la previsione per questo punto".

- `GET https://api.mappafunghi.app/cells/1kmE4734N2072?region=puglia` → 500, and `/spot` at that cell's own centre (41.632747, 14.947155) → 500.
- A random 60 of Puglia's 1,104 scored cells: 13 returned 500 on `/cells/{id}` (e.g. `1kmE4747N2063`, `1kmE4736N2066`, `1kmE4746N2062`). Samples in Abruzzo, Calabria and Campania hit the rate limiter (429), so those regions were never checked.
- It was not about points outside the region: `/spot` snaps any point to the region's nearest cell (`_nearest_cell`, plain lat/lon degrees) and returns 200 for far-away points. A far point failed only when it snapped to a failing cell.
- After the re-score (deployed 15039d2, every region re-scored) those cells return 200. It no longer reproduces. It never reproduced on the local stores (scored 2026-09-28) either.

The cause is not known, and the stores that failed were overwritten by the re-score. The candidates, and how to look for them, are in [bug-factors-porcini-500.md](bug-factors-porcini-500.md): porcini `/factors` failed in the same regions and window, and both read the leaf keys' factors tier for the winning `source_key`. Do the two together.

What this card must guarantee, whatever the cause: `get_spot`'s contract is to always succeed (the comment in `_forecast`, and `fix-spot-500-before-daily-job.md` in plans/done). A likely raising point is `_forecast` in `api/src/api/live/repository.py`: `factor_frames[row.source_key].loc[row.date]` raises a KeyError when the winning leaf key has no factor row for that cell and day.

Steps:
1. Test-first (AGENTS.md: TDD for model and data code): a live-repository test where a cell's daily winner names a leaf key with no factor row for that day. Confirm it raises today.
2. Make `_forecast` degrade: serve that species' day without a breakdown, or leave the day out, instead of raising. Check that the web `SpotPanel` handles whichever you choose, and keep the `why` breakdown unchanged where rows exist.
3. Ship with `deploy/deploy-api.sh`. Then check a slow sample of every region's cells (about 1 request a second, so the rate limiter doesn't answer 429).
