---
order: 21504
kind: task
title: [feat] index trend
status: Done
---
When a zone gets selected, or in the region picker, show a trending line of the last 15 days, with the andamento of the index and a colored arrow that shows the direction of the trend

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->

## Plan

Placement (asked 2026-09-29): the Zona picker in Stagioni/Prospettive (the chosen comune, or the
whole region), each row of the hub's region list, and the spot panel (a tapped cell). Not the
top-bar region switcher.

The trend is the mean conditions index over the area's woodland cells, per day, for the 15 days
ending today, read from the score store (so it includes today and matches `/overview`). The arrow
is the least-squares change across the window: up, down, or steady inside a small band.

- [x] API models: `TrendPoint`, `TrendResponse`, `RegionTrend`, `OverviewTrendResponse`, and the
  14 days before today on each `SpeciesForecast` (`past`)
- [x] LiveRepository: area trend (region or comune), region trend, a cell's past days (TDD)
- [x] FixtureRepository: the same, from the deterministic generator
- [x] Routes `GET /trend` and `GET /overview/trend`, cached; openapi.json re-exported
- [x] Web: regenerate `schema.ts`; `useTrend`, `useOverviewTrend`
- [x] Web: `score/trend.ts` (direction, y-domain) with tests
- [x] Web: `TrendLine` sparkline + coloured arrow, i18n it/en
- [x] Web: Zona trend in the Seasons and Outlook panels
- [x] Web: trend on each hub region row
- [x] Web: last 15 days per species in the spot panel
- [x] Checks: pytest, ruff, vitest, eslint, prettier, build; look at it in the browser
