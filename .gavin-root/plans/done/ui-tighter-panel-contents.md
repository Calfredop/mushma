---
kind: task
title: [ui] tighter panel contents
parent: ui-optimizations.md
complexity: moderate
---
Tighten the panel contents shown in the phone sheet and the desktop panel. Same information,
less chrome. You are one item of the plan `ui-optimizations.md`: read its Decisions and
Constraints first. The shell work (glass tokens, overlay sheet, desktop panel) has already
landed; build on it and don't touch `App.tsx` layout or the map.

- **Spot forecast** (`web/src/panels/SpotPanel.*`, `components/SpeciesBreakdown.*`,
  `components/ScoreChip.*`): each species' name, binomial and score chip share one line, with
  a shorter 8-day bar strip. On a 390×844 phone the three species fit in about the half-open
  sheet (today they take about a full screen).
- **Why breakdown** (`panels/WhyBreakdown.*`, `panels/FactorDetail.tsx`): drop the nested-card
  look inside the sheet. One line per factor: label, favourable bar, value, brake. "frena del
  100%" no longer wraps at 360px. Factors holding nothing back (`impact` 0 from
  `score/impact.ts`) fold into one "Altri N fattori a 1,00" row (plural via i18n) that expands
  in place. Shown factors keep the API's order, never re-sorted. "Mostra tutti i dettagli" and
  each factor's detail disclosure keep working. When the score is blocked or every factor
  brakes, nothing folds.
- **Hot places, Seasons, Outlook, Plausible species**: mobile heading sizes one step down,
  through tokens rather than per-file numbers, and tighter row paddings. No information removed.
- Constraints: new strings in `it.json` and `en.json`; "conditions score" wording; tap targets
  ≥ 44px; no API or score-code changes.
- Tests: update unit tests where markup changes, and add WhyBreakdown tests for the fold:
  full-credit factors hidden until expanded, the count is right, and nothing folds when the
  score is blocked.
- Done: before/after screenshots of an open spot at 360 and 390px in
  `web/screenshots/ui-density/`; `pnpm test`, `lint`, `format:check`, `build` and `test:e2e`
  pass; commit only the files you touched, don't push.
