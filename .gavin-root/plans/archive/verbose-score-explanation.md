---
title: Verbose "why this score" justification in the sidebar
status: Done
priority: high
complexity: moderate
---
## Why

Many cells are scoring high when the only recent rain was a short event a few
days ago. The scores may be right or the rules may be too generous — there is
no way to tell from the UI, because the "why this score" panel shows each
factor's 0–1 value and its share of the shortfall, but never the **measurement
behind it**. This card makes the panel state the evidence, so a suspicious
score can be checked without querying Parquet by hand.

Traces to PRD → Features (v1) #3 ("show the factors that contributed — rain N
days ago, cumulative rain, soil/air temperature, drying, habitat, altitude,
season window — and how much each one weighed"). The panel today satisfies
"how much each one weighed" but not "rain N days ago".

This card is the **instrument**, not the tuning. If the numbers it surfaces
show the rules really are optimistic, open a separate card against the species
rules / `model-v1-validation.md`; do not retune here.

## What exists today

- `api/src/api/model/factors.py` already computes, per factor, the measured
  `input` (the aggregate, the day count, the attribute) and, for rain events,
  `days_ago` — the lag of the rain it actually scored.
- `api/src/api/model/pipeline.py:90` already persists them to the factors tier
  as `<factor>__input` and `<factor>__days_ago`.
- The read path drops them: `reconstruct_breakdown`
  (`api/src/api/live/breakdown.py`) rebuilds only `value` + `contribution`, and
  the API model `FactorBreakdown` (`api/src/api/models.py:17`) has no field for
  them. So the frontend has never seen a measurement.
- UI: `web/src/panels/WhyBreakdown.tsx` + `web/src/score/impact.ts`, strings
  under `why.*` and `factor.*` in `web/src/i18n/locales/{it,en}.json`.

## Target

Each factor row can be expanded (or reads, on one extra line) as a sentence in
the user's language naming the measurement, its unit, when it happened, and
what the rule wanted. For example, for `rain_trigger`:

> Pioggia scatenante — 42 mm in 3 giorni, caduti 6 giorni fa. La regola dà
> credito pieno da 30 mm e da 6 a 16 giorni di distanza.

and for a gate:

> Quota — 640 m. Piena fino a 800 m, nulla oltre 1250 m.

Copy rule: it stays a **conditions index**, never a probability, and never an
edibility or identification claim.

## Open question for whoever picks this up

How verbose, and always-on or behind a disclosure? A sentence per factor is
5–20 lines on a phone. Suggested default: keep the current compact rows, add a
per-row expander plus one "show all details" toggle that remembers its state.
Confirm with the human before building the alternative.

## Decisions (2026-09-19)

- **Disclosure: the suggested default.** Compact rows stay; each row gets an
  expander and one "show all details" toggle whose state is remembered
  (localStorage, wrapped in try/catch). The alternative (always-on sentences)
  is not built, so there is nothing to confirm.
- **Thresholds are inlined per factor, as a `rule` object, not served by a
  rules endpoint.** (1) A group or combined breakdown is the *winning species
  key's*, and the response does not name that key, so a rules endpoint has
  nothing to be keyed by; the four porcini keys have different thresholds.
  (2) The inlined rule is the same config object `reconstruct_breakdown`
  replays the contribution from, so the band the copy quotes cannot drift from
  the value beside it. (3) The PWA already caches the spot response; a second
  cached endpoint is a second thing to keep in step for offline. Cost: the rule
  repeats across 8 days x 3 species, which gzip removes.
- **Units live next to the attribute vocabulary, not in `model.yaml`.** Weather
  variables read `weather.yaml`; the derived series and grid attributes get
  constants beside `DERIVED_SERIES` / `GRID_ATTRIBUTES` in `model/rules.py`.
  `model.yaml` is hashed into `rules_version`, and a display unit is not a
  scoring rule.
- **The rain a factor quotes is the model's rain, after
  `precipitation_scale`** (x1.28 + 0.29/km on reanalysis days, forecast days
  unscaled). The panel says so in one note, because that rescale is a
  candidate cause of the suspicion this card investigates.
- **Season and habitat get a plain sentence with no numbers.** The habitat
  affinity is not persisted and a season window shifts with altitude, so a
  single set of dates would mislead.
- The example in "Target" says full credit "from 6 to 16 days"; for
  `porcini_edulis` the lag plateau is 10-16 days (`[6, 10, 16, 24]`, zero
  outside 6-24). The copy quotes the plateau and the zero edges from the rule.

## Checklist

### API (TDD — failing test first, per AGENTS.md)

- [x] Extend `FactorBreakdown` (`api/src/api/models.py`) with optional
      `input`, `unit`, `days_ago`, `role` and `weight`, documented as "the
      measurement this factor read", and keep every existing field
- [x] Carry the rule's response thresholds (trapezoid edges, rain lag window)
      into the breakdown so the copy can say what the rule wanted; decide
      between inlining them per factor and a separate cached rules endpoint,
      and write the reason into the card before coding
- [x] Resolve each factor's unit from config, not from the UI: weather
      variables have units in `api/src/api/config/weather.yaml`, grid
      attributes (`elevation_m`, `slope_deg`, `soil_ph`) need a unit map
- [x] Read `<factor>__input` / `<factor>__days_ago` in the live repository and
      thread them through `reconstruct_breakdown`
      (`api/src/api/live/breakdown.py`, `api/src/api/live/repository.py`);
      tolerate the columns being absent for days scored without the factors
      tier
- [x] Fill the new fields in the fixtures repository
      (`api/src/api/fixtures/repository.py`) so contract tests and the offline
      frontend stay honest
- [x] Tests: `api/tests/live/test_breakdown.py` (inputs survive the round
      trip, missing columns degrade to `None`), plus the fixtures contract test
- [x] Re-export the contract: `cd api && uv run python scripts/export_openapi.py`

### Frontend

- [x] `cd web && pnpm run generate:api` to regenerate `src/api/schema.ts`
- [x] Extend `explainScore` (`web/src/score/impact.ts`) only if the rendering
      needs derived values; keep the impact maths unchanged (not needed: the
      new `FactorDetail` reads the API fields directly, `impact.ts` is untouched)
- [x] Render the justification in `WhyBreakdown.tsx` with the disclosure agreed
      above; a factor with no measurement (season, habitat) still gets its
      plain-language line
- [x] Format numbers and dates through the existing `Intl` helpers and
      `formatDayLong`; metric units only
- [x] i18n: one phrasing key per factor kind in `it.json` **and** `en.json`,
      both complete, no hardcoded strings; Italian is the default locale
- [x] Tests: `WhyBreakdown.test.tsx` — a rain factor shows amount + lag, a gate
      shows its attribute and band, a missing input renders without crashing
- [x] Check the panel at phone width (390 px, headless Chromium on the live API and
      real 2026-09-19 scores: no horizontal overflow, rows keep their compact
      40 px pitch with a 44 px hit area, in it and en; the Chrome extension tab
      stayed in a hidden window and never finished loading the map)

### Verify the original suspicion

- [x] With the panel live, open two or three of the high-scoring cells that
      prompted this card and record, in `.gavin-root/docs/model-v1-validation.md`,
      what `rain_trigger` / `rain_30d` / `soil_moisture` actually measured
- [x] If the rules look too generous, file a separate tuning card — do not
      change thresholds in this one
      (filed: `tune-rain-drivers-saturate.md`)

### Done when

- [x] `cd api && uv run pytest && uv run ruff check . && uv run ruff format --check .`
- [x] `cd web && pnpm test && pnpm run lint && pnpm run format:check && pnpm run build`

## Outcome (2026-09-19)

- API: `FactorBreakdown` now carries `role`, `weight`, `input`, `unit`,
  `days_ago` and a `rule` (`FactorRule`: kind, variable and its unit,
  aggregate, window, offset, op, threshold, and the `trapezoid` / `lag_days`
  bands). The bands are lists, not tuples: `openapi-fetch` turns a generated
  tuple type into an array, which broke `queries.ts` type-checking.
- Web: each row has a disclosure, plus one "show all details" switch kept in
  `localStorage` (`mushma.whyDetails`). `FactorDetail.tsx` phrases the numbers;
  `score/detail.ts` reads a trapezoid as a full band and its zero edges;
  `impact.ts` is untouched.
- The real numbers are in `.gavin-root/docs/model-v1-validation.md`. They show
  the rain drivers saturate in an ordinary September; the tuning is a separate
  card and no threshold changed here.
- `why.detail.rainNote` states that the panel's rain is scaled up. It is tied
  to `precipitation_scale.enabled` in `model.yaml`: reword or drop it if that
  is turned off (also listed on the tuning card).
- To repeat the check: the API allows CORS only from `:5173` and `:4173`, so run
  the dev server on `:5173`.
