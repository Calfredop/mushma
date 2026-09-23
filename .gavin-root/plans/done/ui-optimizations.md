---
complexity: complex
order: 3072
title: [ui] optimizations
status: Done
---
do full optimisations of ui, especially on mobile where is too crammed. Use FABS on map (a la Apple Glass UI), collapsable sidebar, smoothly animated action sheet...

Scope: phone map chrome, phone bottom sheet, desktop sidebar, panel contents density, and the
footer links (plus a GitHub link). Web only (`web/`). Traces to PRD → Audience ("usable on a
phone in the field", portfolio) and M7 polish.

## Decisions (interview, 2026-09-23: don't re-litigate)

- **Phone, Apple Maps shape.** No top bar; the map is full-bleed under the safe-area insets.
  Species pill top-left; a glass button cluster top-right: ◈ analysis, ◎ locate, ⓘ menu. The
  legend is a one-line scale chip that expands to the full key on tap. The wordmark moves to
  the sheet header, the search field to the sheet's peek row.
- **One locate button.** ◎ only centres the map and draws your dot. Focusing the search field
  lists "La mia posizione" first; it runs GPS and opens the spot forecast there (`spot-open`
  method `gps`, like today's top-bar button).
- **Sheet (phone).** An overlay on a full-screen map (no longer a grid row that shrinks it),
  with three snap points: peek (wordmark + search), half (a chosen spot opens here), full (a
  sliver of map stays visible; focusing search goes here). Dragged by its handle and header
  with velocity snapping; the body takes over the gesture only at scrollTop 0. Built with
  **motion** (`motion/react`), loaded through `LazyMotion` so first paint keeps its budget.
  MapLibre padding keeps the chosen spot visible above the sheet, replacing today's "centre on
  the tap" workaround in `onCellClick`/`onPointClick`. Under `prefers-reduced-motion` it snaps
  without a spring. The handle stays a button that steps through the snaps for keyboard and
  screen readers.
- **Glass, CSS only, everywhere.** Every floating control on phone and desktop: Lichene tint at
  low alpha, `backdrop-filter` blur + saturate, a 1px inner highlight, a soft shadow, as
  tokens in `web/src/styles/tokens.css`. Opaque fallback under `prefers-reduced-transparency`
  and where `backdrop-filter` is unsupported. No SVG refraction. Palette and score scale
  unchanged.
- **Analysis on phone.** ◈ toggles it. The factor chips become one horizontally scrolling row
  of glass chips just above the time bar, colour-dotted, no family headings; the opacity key
  ("frena → favorevole") is a small chip at the row's start. Desktop keeps the grouped panel,
  in glass.
- **Desktop (≥900px).** The map goes full-bleed and the panel becomes a floating inset glass
  card (400px, rounded). A toggle collapses it to its header row (wordmark + search); the
  browser remembers it (`usePersistentFlag`); choosing a spot re-expands it. Map padding
  follows the panel.
- **ⓘ menu.** A glass popover (desktop: a button in the panel header) with Avvertenze, Dati e
  crediti, Termini, Privacy, Preferenze cookie, GitHub (https://github.com/Calfredop/mushma)
  and the IT/EN switch. The footer keeps the data status, the one-line disclaimer and one
  compact row of small links with a GitHub icon, so crawlers still find them.
- **Panel density: tighten structure.** Same information, less chrome. It's the nested card below.

## Constraints

- Every new string through i18n, Italian and English complete. "Conditions score" wording; no
  edibility or identification copy.
- Tap targets ≥ `--tap` (44px). At 360px: no horizontal page scroll, no control over another.
- `pnpm run perf` (first map paint) stays under 3 s on fast4g after motion lands.
- Analytics events keep their names and data; nothing sends a location.
- URL state, shared links (`?cell=`, `?at=`), hotspots, keyboard access and the focus ring
  keep working.
- Update `web/e2e/layout.spec.ts` and `smoke.spec.ts` as each item changes the shell: re-aim
  their assertions, don't delete them.
- Out of scope: the API, the model, the score colours, the basemap style, a dark theme, new
  features.

## Checklist

- [x] Glass tokens (tint, blur, saturate, highlight, shadow, fallbacks) in `tokens.css`, applied to every floating control; a "Glass" section in `.gavin-root/docs/visual-direction.md`, and its Layout and Motion sections updated to the new shell
- [x] Phone shell: top bar gone, glass cluster ◈ ◎ ⓘ top-right, species pill beside it without overlap at 360px, legend as an expanding chip, one centre-only locate FAB, safe-area insets respected
- [x] ⓘ glass menu with its seven entries, operable by keyboard and screen reader (menu button, Escape closes, focus returns), also opened from the desktop panel header
- [x] Phone analysis chip row above the time bar, opacity key chip first, playback and calendar still reachable; the 360px analysis test in `layout.spec.ts` asserts the row sits above the strip
- [x] **Review gate:** commit, save 360×640 and 390×844 screenshots (map, analysis, ⓘ menu open) to `web/screenshots/ui-shell/` (add `web/screenshots/` to `.gitignore`), then stop and ask the human to review; tick this only once they approve
- [x] Phone sheet rebuilt on motion: overlay with rounded top corners (human, at the review gate), peek/half/full snaps, drag handed to the body at scrollTop 0, bottom controls riding above it, map padding for the chosen spot, reduced-motion snaps, handle button steps the snaps
- [x] Search in the peek row: focusing it snaps to full and lists "La mia posizione" first, which opens the spot forecast; the intro becomes one line plus a "Come funziona" disclosure
- [x] Desktop floating glass panel with a remembered collapse toggle that a chosen spot re-expands and map padding follows; the desktop checks in `layout.spec.ts` pass at 900–1440px
- [x] Compact footer: data status, one-line disclaimer, one row of small links plus a GitHub icon link; no link wraps onto two lines at 360px
- [x] [Tighter panel contents](./ui-tighter-panel-contents.md)
- [x] Final check: `pnpm test`, `lint`, `format:check`, `build`, `test:e2e` and `perf` pass; screenshots at 360, 390 and 1280px (map, analysis, spot open, each sheet snap, desktop panel open and collapsed) in `web/screenshots/ui-final/`

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
