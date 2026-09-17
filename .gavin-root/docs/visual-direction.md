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
| Lichene | `#EDF0EA` | paper: panels, sheet, top bar (cool grey-green, not cream) |
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

## Layout

Mobile first: the map is full-bleed and everything else is a sheet over it.

```
┌──────────────────────────────┐
│ mushma        🔍  ◎   IT·EN  │  top bar (Lichene, 90% opaque)
│ [Porcini][Ovoli][Gallin.][Tutti]  species switcher
│                              │
│            MAP               │
│                              │
│  ▭▭▭▭▭ legend                │
├──────────────────────────────┤
│ 11 12 13 14 15 16 17 ▨18 ▨19 │  date strip, forecast hatched
├──────────────────────────────┤
│ ═══  Hot places now      ▴   │  bottom sheet (peek → half → full)
└──────────────────────────────┘
```

At 900 px and up the sheet becomes a 400 px left panel (search, hot places, then the spot forecast
and why once a place is chosen). The map fills the rest, with the date strip along its bottom edge.

## Motion

Little of it: the sheet slides and the map `flyTo`s to a chosen place. With `prefers-reduced-motion`,
the sheet appears in place and the map `jumpTo`s.

## Copy

Sentence case, plain verbs, Italian first. A score is a "conditions score" (IT *indice delle
condizioni*), never a probability or a chance. No edibility or identification language anywhere.
