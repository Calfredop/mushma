---
complexity: complex
order: 9216
kind: plan
title: [feat] analysis mode
status: Done
---
Allow users to go into this mode, to show on the map each of the indicators that contribute to the final index. Give a color to each indicator (rain, humidity, temp…) then allow users to see the evolution of them on the map, using a gradient (opacity) on each tile

## Decided (interview 2026-09-23)

- **What a tile shows.** Each indicator is one enabled factor of the species' rules, drawn with its
  0–1 factor value as opacity: opaque = favourable, faint = holding the score back. The measurement
  behind it (mm, °C…) stays in the existing spot/"why" panel on tap. There is no "humidity" factor.
  Dry air is covered by `drying` ("Wind and dry air") and ovoli's `evaporative_demand`.
- **Several at once, blended.** Any number of indicator chips can be on. Each active chip is its own
  translucent layer in its own colour, stacked.
- **Every factor is a chip; colours come in families.** Chips are the union of enabled factors over the
  species' rule files, named as in "why" (`factor.*` i18n keys), grouped into families of related
  hues: rain & moisture (rain_trigger, rain_30d, rain_frequency, drought_*, water_balance_*…),
  temperature (air/soil_temperature, heat, heat_spike), drying (drying, evaporative_demand), cold
  (frost, hard_frost, cold_nights, snow), terrain & habitat (habitat, altitude, slope, sun_exposure)
  and season. Within a family each factor still gets a distinct colour. Static factors are included
  even though they don't change with the date.
- **Per species, no "Tutti".** Analysis mode works on porcini, ovoli or gallinacci. A cell's values
  come from the rule file that wins that cell on that day (the group row's `source_key`), the same one
  "why" explains. "Tutti" is disabled in the mode, and entering from it switches to porcini.
- **Evolution = the 14-day date strip + play.** Factor values are only stored for today −6 to +7
  (`api.jobs.daily`). A play/pause button steps through those days. Older replay dates and past
  seasons have no factor data, so the mode says so there instead of drawing anything.
- **Entry = a map toggle.** An "Analisi / Analysis" toggle next to the legend. In the mode the score
  colours are hidden and the legend becomes the chip panel. Tapping a cell still opens the spot
  forecast and "why". The sheet (hot places, seasons, outlook) is unchanged.

## Checklist

- [x] **API, tests first.** `GET /factors?species=<porcini|ovoli|gallinacci>&date=` (no `combined`;
      date defaults to today, Europe/Rome) returns, for that species and day, the chip list (factor
      id, `i18n_key`, role, in breakdown order, the union over the group's rule files) and, per
      woodland cell with a score that day, `cell_id`, `lon`, `lat` and each factor's 0–1 value from
      the cell's winning rule file (`null` where that file lacks the factor). 404 with the stored
      range for a day with no factor rows. Cache-Control as `/scores`. Implemented in
      `LiveRepository` and `FixtureRepository` (added to the `ScoresRepository` protocol), with
      pytest covering winner selection, a factor missing from the winner, `combined` rejected and
      the 404. Measure the real payload for one species-day and keep it under the ~1 MB gzipped
      budget (PRD → Constraints). Go columnar if rows don't fit.
      *Measured on the 2026-09-20 stores: 212–239 KB gzipped per species-day (10,777 cells,
      values rounded to 3 decimals in chip order), so rows stay.*
- [x] **Contract.** `openapi.json` re-exported (contract test green) and `web/src/api/schema.ts`
      regenerated with `pnpm generate:api`. A `useFactors(species, date)` query in
      `web/src/api/queries.ts`.
- [x] **URL state.** `mode=analysis` and `f=<comma-separated factor ids>` parse and serialise in
      `web/src/state/urlState.ts` with tests: unknown ids dropped, `species=combined` becomes porcini
      in the mode, entering with no `f` turns on `rain_trigger`, and the mode survives species
      switches, keeping only chips the new species has.
- [x] **Palette.** Family colours designed and written up in `.gavin-root/docs/visual-direction.md`
      (new "Analysis mode" section). Each colour must be distinct from Lago (selection/interaction)
      and from the others under the Machado CVD simulation used for the score scale, and must stay
      readable with two or three stacked at the chosen opacity cap (≤ ~0.75). The factor → family →
      colour mapping lives in one module (e.g. `web/src/score/indicators.ts`), with a test that every
      `factor.*` key in the locales has a colour and an unknown id falls back to a neutral one.
- [x] **Map layers.** In the mode the score layers (`cells-dot`, `cells-fill`) are hidden. Each
      active chip draws its own dot layer (below z11) and square layer (above), like the score's,
      with the chip's colour and opacity = value × cap. `null` is not drawn. Selection, spot and
      sightings layers stay on top. The layer builder is unit-tested (`dataLayers.test.ts` style).
- [x] **Toggle and chip panel.** The toggle sits next to the legend. In the mode the legend becomes
      chips grouped by family (toggle buttons with `aria-pressed`) plus an opacity key ("more
      favourable →", never probability or chance). The species switcher disables "Tutti". It works
      at 360 px wide without covering the date strip (`layout.spec.ts`). Tapping a cell still opens
      spot + "why".
- [x] **Play and limits.** In the mode a play/pause button on the date strip steps through the
      14 days (~1 s a day) and loops. It pauses when the strip is touched and prefetches the next
      days so it doesn't stutter. On a replay date before today −6 or with a season on the map, the
      mode shows "indicators are only kept for the last 7 days and the forecast" and draws nothing.
      Forecast days keep their hatch.
- [x] **i18n and checks.** Every new string is in `it.json` and `en.json` (keys test green).
      `uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`, `pnpm test`,
      `pnpm run lint`, `pnpm run format:check` and `pnpm run build` are green. The e2e smoke test
      (fixtures) toggles the mode, turns on two chips, presses play and sees the date advance.

## Out of scope

- Scoring history with the factor tier so replay and past seasons work (~40 MB per rule file per
  year on the server). Its own card if wanted.
- "Tutti" / combined in analysis mode; raw-weather maps (mm, °C as the colour).
- Any change to the rules, the scoring or the score scale; the hot-places/seasons/outlook sheet.
- Deploying. Commit only.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
