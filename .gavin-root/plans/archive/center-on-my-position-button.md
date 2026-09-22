---
title: Floating center-on-my-position button
status: Done
complexity: simple
---
A round floating button over the map (bottom-right, above the legend and time bar) that takes a one-shot GPS fix and recenters the map on it, without opening the spot forecast. A "you are here" dot marks the fix. The top-bar "Use my location" button keeps its behavior and also sets the dot.

The position lives only in React state: never in the URL, never sent to the API.

- [x] Failing Vitest test: a fix from the floating button issues a camera request and leaves the selected spot unchanged; an out-of-region fix shows the "outside" message and doesn't move the camera
- [x] i18n strings `locate.center` and `map.userPosition` in it.json and en.json
- [x] `userPosition` prop and marker in `ConditionsMap`
- [x] Floating button, second `useLocate` instance and `userPosition` state in `App.tsx`, style in `App.module.css`
- [x] `pnpm test`, `pnpm run lint`, `pnpm run format:check`, `pnpm run build` all pass
- [x] Real-browser check with a mocked GPS fix on a phone and at 1280 and 1440 px: the tap lands, the map centres at spot zoom, the dot shows, the URL and the sheet don't change

Layout note: on a phone the button shares the legend's row in the bottom grid and keeps its corner when the legend hides. From 900 px it leaves the row (the time bar needs it whole) and sits above the row's end, in the zoom buttons' column.
