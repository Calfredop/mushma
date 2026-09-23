# Visual direction

M5 frontend core. Traces to PRD → Audience (friends in the field, portfolio), Principles (honest
uncertainty) and Constraints (mobile performance).

## Subject and job

A forager checks mushma on a phone the night before, or in a parked car at the edge of a chestnut wood
at 7 am, often in bright sun and with one hand free. The app has one job: **show where conditions are
good today and over the next week, and why.** Everything else is secondary.

The map is the hero. The chrome borrows from the Italian topographic sheet (IGM tavolette, CAI trail
maps): a quiet paper surface, dark ink, blue for water and interaction, a legend that reads like a map
key. Nothing about it should look like a weather widget or a dashboard.

## Signature: the forecast hatch

Anything that rests on the weather forecast is drawn with a **diagonal hatch**. On a map, hatching is
the convention for an area that is projected or uncertain. Here it marks forecast days on the date
strip and forecast bars in the 7-day outlook, and the same hatch appears in the legend as "forecast".
Observed days are solid. The pattern carries the PRD's "honest uncertainty" principle, so nobody has to
read a footnote to know that Thursday is a forecast. It's the one piece of boldness. Everything around
it stays quiet.

## Palette

Light theme only for v1. People use the app in daylight, and a sequential scale that reads in sun
needs dark-for-high on a light basemap. A dark theme would need a second, reversed scale and is left
for later.

| name | hex | role |
|---|---|---|
| Lichene | `#EDF0EA` | paper: panels, the sheet, and the tint of glass (cool grey-green, not cream) |
| Carta | `#F8FAF6` | raised surface: cards, inputs |
| Humus | `#1C211D` | ink: text, icons, hatch strokes |
| Felce | `#5B675E` | secondary text, rules, inactive controls (5.2:1 on Lichene) |
| Lago | `#1F56A0` | interaction: selection outline, focus ring, links, active control (6.3:1 on Lichene; blue stays distinct from the warm scale for every CVD type) |
| Basemap land | `#E4E8E2` | the basemap is desaturated and cool so the warm score scale is the only warm thing on screen |

### Conditions score scale ("Porcino")

Five stepped classes, not a continuous gradient: in sun, five steps are easier to match against the
legend than a smooth ramp. The panels still show the exact score as a number.

| class | score | hex | OKLCH |
|---|---|---|---|
| 1 | 0.0–0.2 | `#F7F0C6` | 0.95 0.055 100 |
| 2 | 0.2–0.4 | `#F0C967` | 0.85 0.125 88 |
| 3 | 0.4–0.6 | `#E68C2C` | 0.72 0.150 62 |
| 4 | 0.6–0.8 | `#B34F2A` | 0.55 0.140 40 |
| 5 | 0.8–1.0 | `#652D1F` | 0.37 0.085 35 |

It runs from pale straw to porcino-cap brown. Lightness drops strictly from low to high (OKLCH L 0.95 →
0.37), so the order survives any colour-vision deficiency and greyscale. Checked with the Machado et al.
(2009) full-severity simulation:

| view | OKLab L per class | smallest step between adjacent classes (ΔE OK) |
|---|---|---|
| normal | 0.95 0.85 0.72 0.55 0.37 | 0.123 |
| protanopia | 0.95 0.83 0.67 0.49 0.33 | 0.139 |
| deuteranopia | 0.95 0.86 0.73 0.56 0.38 | 0.119 |
| tritanopia | 0.95 0.85 0.73 0.56 0.37 | 0.115 |

Low scores deliberately recede into the basemap (class 1 is 1.08:1 against basemap land), and high
scores stand out (class 5 is 8.7:1). Cells get a thin Humus outline from zoom 11 so the lowest class
still shows where the woodland is.

Text on a score swatch: Humus on classes 1–3 (14.2, 10.3 and 6.4:1), white on classes 4–5 (5.2 and
10.8:1).

## Analysis mode

Card `feat-analysis-mode`. The ◈ "Analisi / Analysis" button in the map's cluster swaps the score
colours for the factors behind them. Each factor of the species' rules is a chip, and each chip that is on draws
its own layer in its own colour. A cell's opacity is the factor's 0–1 value: opaque is favourable,
faint is holding the score back. The measurement behind a value (mm, °C…) stays in the "why" panel.

### Families

Chips come in six families of related hues, so a glance tells rain from cold from terrain. Within a
family each factor has its own colour, mostly a lightness step. A rule id with a window in its name
shares the colour of the concept it names (`water_balance_60d` is the water balance, `drought_14d`
the drought), since no species has both. An unknown factor draws in a neutral grey, `#7A827C`. The
mapping lives in `web/src/score/indicators.ts`.

| family | factor | hex | OKLCH |
|---|---|---|---|
| Rain and moisture (teal) | rain_trigger | `#268C9F` | 0.59 0.093 212 |
| | rain_30d | `#2FA8A3` | 0.67 0.103 191 |
| | rain_frequency | `#60BCD4` | 0.75 0.094 218 |
| | water_balance, water_balance_60d | `#92C8B2` | 0.79 0.064 168 |
| | drought, drought_14d | `#537B6D` | 0.55 0.050 171 |
| | soil_moisture | `#599576` | 0.62 0.080 160 |
| | early_season_wetness | `#72ADB6` | 0.71 0.063 207 |
| | waterlogging | `#55866C` | 0.58 0.067 160 |
| Temperature (orange) | air_temperature | `#EF8332` | 0.72 0.160 53 |
| | soil_temperature | `#DA6210` | 0.64 0.170 47 |
| | heat | `#F8A650` | 0.79 0.140 64 |
| | heat_spike | `#CA3707` | 0.56 0.190 35 |
| Drying (yellow) | drying | `#F4D03D` | 0.86 0.160 95 |
| | evaporative_demand | `#E3B409` | 0.79 0.160 89 |
| Cold (violet) | frost | `#A476E6` | 0.66 0.166 301 |
| | hard_frost | `#764DD6` | 0.54 0.200 292 |
| | cold_nights | `#C593DF` | 0.74 0.119 313 |
| | snow | `#C0BCFD` | 0.82 0.091 287 |
| Terrain and woodland (muted olive) | habitat | `#49553B` | 0.43 0.044 128 |
| | altitude | `#473C25` | 0.36 0.039 84 |
| | slope | `#756A3F` | 0.52 0.062 95 |
| | sun_exposure | `#9DA06C` | 0.69 0.072 111 |
| | lithology | `#645850` | 0.47 0.020 55 |
| | soil_ph | `#6C8970` | 0.60 0.050 148 |
| Season (plum) | season | `#5C0E59` | 0.34 0.140 330 |

Water keeps to teal so it never reads as Lago, which still means selection. Terrain is muted so the
weather families carry the colour. Season is the darkest colour on the map, a plum no other family
comes near.

### Checks

Same method as the score scale: the Machado et al. (2009) full-severity simulation in linear sRGB,
distances in OKLab (ΔE OK). Each figure is the worst over normal vision, protanopia, deuteranopia and
tritanopia. The colours were hill-climbed inside each family's hue and lightness bounds to raise the
worst of these figures.

| check | worst ΔE OK |
|---|---|
| family anchors (rain_trigger, air_temperature, drying, frost, habitat, season), pairwise | 0.104 |
| any enabled factor against Lago `#1F56A0` | 0.083 (drought, habitat) |
| enabled factors within a family | 0.069 (terrain) |
| any two chips one species can show (porcini 13, ovoli 11, gallinacci 16) | 0.060 |
| a full-value cell at the cap against the basemap land | 0.083 (drying) |

Factors no rule enables yet (soil_moisture, early_season_wetness, waterlogging, lithology, soil_ph)
have colours but are held to the family look only. Check them properly when one is switched on.

### Stacking and the opacity cap

Any number of chips can be on, stacked in the order they were turned on (the last on top). With
plain `value × cap` per layer the top layer would hide the rest: three layers at 0.6 leave the
bottom one 10 % of the blend. So each layer instead gets an equal share of the cap. With `n` layers
on, the layer `i` places below the top (0 for the top one) has opacity `value × s / (1 − i·s)`,
where `s = 0.75 / n`. Every indicator then weighs `0.75 / n` in the blend, all of them together
cover at most 0.75 (the cap), and one indicator alone is plain `value × 0.75`.

At full value, the blend of any two family colours differs from either colour alone by at least ΔE
0.065 for normal vision and 0.036 under every simulation. Three differ by at least 0.054 for normal
vision. Under a colour-vision deficiency, 4 of the 20 family triples blend close to one of their own
colours (worst 0.006: air temperature, drying and habitat). Mixing three colours in a dichromat's
two-dimensional colour space can land on any one of them, so no palette avoids this. The chip panel
always says which layers are on.

## Type

Self-hosted with Fontsource (no third-party font requests, and M7 can cache them offline).
`font-display: swap`, Latin subset only.

| role | face | why |
|---|---|---|
| UI and body | **Atkinson Hyperlegible Next** (variable) | Built by the Braille Institute for low-vision legibility, with unambiguous letterforms and a large x-height. That is exactly what glare on a phone screen calls for. |
| Data | **Atkinson Hyperlegible Mono** | Scores, dates and counts in tabular figures that line up in the outlook and breakdown. |
| Display | **Young Serif** | Only for the wordmark and species names. A chunky old-style serif with the feel of a vintage field guide. |

Latin binomials (*Boletus edulis*) are set in italic body type under the species name, following the
naming convention rather than decorating.

Scale (rem, mobile → desktop): 0.8125 caption · 0.9375 body · 1.0625 lead · 1.375 species · 1.75 wordmark.

## Glass

Card `ui-optimizations`. Every control that floats over the map, on a phone and on a desktop,
is one material: **glass**. The species pill, the button cluster, the legend chip, the factor
chips, the time bar, the zoom buttons, the ⓘ menu and the attribution all use it, and the sheet
and the desktop panel use its strong tint. It is CSS only (no SVG refraction) and lives as tokens
in `web/src/styles/tokens.css`, applied through the global `.glass` class
(`composes: glass from global` in a CSS module).

| token | value | role |
|---|---|---|
| `--glass-tint` | Lichene at 66 % | the fill of a control |
| `--glass-tint-strong` | Lichene at 86 % | surfaces that are read: the ⓘ menu, the sheet, the panel |
| `--glass-filter` | `blur(18px) saturate(170%)` | the map behind, blurred and a little richer |
| `--glass-highlight` | 1px white inner line on top, a 9 % Humus hairline all round | the edge that tells glass from paper |
| `--glass-shadow` | the highlight plus a soft two-step shadow | lifts the control off the map |
| `--glass-hover` | Humus at 7 % | hover on anything inside glass |
| `--glass-rule` | Humus at 11 % | the hairline between buttons that share a capsule |

The palette and the score scale don't change: glass is Lichene, and a pressed control is still
solid Humus with Carta text.

**Fallback.** Where `backdrop-filter` is unsupported, or under
`prefers-reduced-transparency: reduce`, the tokens turn opaque (`--glass-tint` is Carta,
`--glass-tint-strong` Lichene, no filter), so text never sits over a busy map through a thin tint.

**Nesting.** A `backdrop-filter`, `filter`, `mask` or `opacity` below 1 on an element makes it
the backdrop root of its descendants: glass inside it blurs only that element, not the map. So
glass never sits inside glass (the ⓘ menu is portalled to the body instead of living in the
cluster), and a container of glass chips never gets a mask or an opacity fade.

## Layout

Mobile first, in the shape of Apple Maps: the map is full-bleed under the safe-area insets,
with no top bar, and everything else floats on it or sits in a sheet over it.

```
┌──────────────────────────────┐
│ (Porcini|Ovoli|Gallin.|Tutte) ◈ │  species pill · glass cluster: ◈ analysis
│                             ◎ │                                ◎ locate
│                             ⓘ │                                ⓘ menu
│            MAP               │
│                              │
│ (▭▭▭▭▭ Legenda ⌃)             │  legend: one chip, opens to the full key
│ [📅][11 12 13 14 ▨15 ▨16 ▨17] │  time bar, forecast days hatched
├──────────────────────────────┤
│            ═══               │  sheet: peek → half → full
│ Mappa Funghi                 │  the wordmark
│ [🔍 Paese, monte, località…] │  the search
└──────────────────────────────┘
```

- **Top.** The species pill sits top-left and stops short of the cluster's column, so at 360px
  the two never overlap (the pill compacts to 14px text below 420px). The cluster is one glass
  capsule of 44px buttons with hairlines between them.
- **◎** only centres the map and draws your dot. The forecast where you stand comes from the
  search: focusing it lists "La mia posizione" first.
- **ⓘ** opens a glass menu: Avvertenze, Dati e crediti, Termini, Privacy, Preferenze cookie,
  GitHub and the IT/EN switch. The footer keeps the same links in one compact row, so crawlers
  still find them.
- **Bottom.** The legend chip, then the time bar. In analysis mode (◈) the legend chip gives way
  to one horizontally scrolling row of glass factor chips, colour-dotted, with the opacity key
  ("frena → favorevole") as a small chip at its start.
- **Sheet.** An overlay on the full-screen map, in the strong glass tint with rounded top
  corners (`--radius-sheet`, 20px) like a mobile app's sheet, with three snap points: peek
  (wordmark and search), half (a chosen spot opens here) and full (a 40px sliver of map stays
  visible; focusing the search goes here). The time bar and the attribution ride on its top edge
  up to half; past half it covers them, and the species pill and cluster fade out under it. Map
  padding keeps a chosen spot visible above it: a tapped place only moves if the sheet would
  hide it.

At 900px and up the map is full-bleed and the panel is a floating inset glass card, 400px wide
and rounded: wordmark, ⓘ and search in its header, then hot places, and the spot forecast and
why once a place is chosen. A toggle collapses it to its header row, and the browser remembers
that. The cluster keeps ◈ and ◎ at the map's top right, the zoom buttons sit on the right edge,
the grouped factor panel replaces the legend at the bottom left, and the date strip runs along
the bottom.

Tap targets are at least 44px (`--tap`) everywhere, and at 360px nothing scrolls the page
sideways and no control sits over another.

## Motion

Little of it, and all of it can be switched off.

- **The sheet** is dragged by its handle and header and snaps to the nearest of its three points,
  with the gesture's velocity deciding ties, on a spring (motion's `motion/react`, loaded through
  `LazyMotion` so first paint keeps its budget). The body only takes the gesture over once it is
  scrolled to the top. The handle is also a button that steps through the snaps, for keyboards
  and screen readers.
- **The map** `flyTo`s a chosen place, with padding for whatever covers it (the sheet, the
  panel).
- **Popovers** (the ⓘ menu) fade and scale in over 160ms from their button's corner.

With `prefers-reduced-motion` the sheet snaps without a spring, popovers appear in place, and the
map `jumpTo`s.

## Copy

Sentence case, plain verbs, Italian first. A score is a "conditions score" (IT *indice delle
condizioni*), never a probability or a chance. No edibility or identification language anywhere.
