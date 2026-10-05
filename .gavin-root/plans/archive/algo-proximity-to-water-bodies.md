---
order: 2048
kind: task
title: [model] proximity to water bodies
status: Done
---

Are we taking in account proximity to water bodies, like rivers, lakes, sea, streams... Search the web for scientific evidences against influence. For example: does flood season take away sporese and kill mycelium so that very close to streaming bodies is bad enviroment for mushrooms, or does the additional humidity helps?

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->

## Outcome (2026-10-02)

The model has no proximity-to-water factor, and should not get one. Findings and sources:
`.gavin-root/docs/water-proximity.md`; pointer in `species-ecology.md` → Open questions.

- No study measures porcini, ovoli or gallinacci against distance to a stream, lake or the sea.
- Close to water is **negative**: saturated soil suppresses ectomycorrhiza (Lodge 1989, Barnes 2018,
  Thomas 2021), stream-bank holm oaks carry fewer ectomycorrhizal tips (Corcobado 2014), and chestnut
  ink disease follows drainage lines (Vannini 2010). Riparian woods already score 0 in the habitat.
- The humidity benefit is one observation (*B. edulis* on hillslopes beside floodplains,
  Lilleskov 2009); a ridge-vs-valley census found 3× more ectomycorrhizal fruiting on ridges
  (Tsujino 2009). Moisture already enters through rain, water balance and soil moisture.
- Floods washing spores away is not a mechanism: these species fruit from perennial mycelium, and
  spores land within about 1 m.
- Every effect acts at metres to a few hundred metres, below the 1 km cell.

If revisited: a share of each cell in ISPRA high-frequency flood zones as a habitat cut, only if the
backtest shows a residual in wet valley bottoms.
