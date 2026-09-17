---
kind: task
title: Gallinacci (*Cantharellus cibarius*): the same fields, with sources; note the soil-pH dependence we cannot model in v1
parent: m3-species-ecology-research.md
---
You are a research agent for the mushma project. Execute this card end to end.

## Task: gallinacci / finferli (*Cantharellus cibarius*)

Research *Cantharellus cibarius* in Tuscany: a long season (roughly June–November) in
broadleaf and conifer woods on acidic soils. It responds to sustained moisture rather than
single storms and persists longer than porcini. Treat that summary as a hypothesis to confirm
or correct.

Two points need particular care:
- **Taxonomy.** In Mediterranean Italy "gallinaccio" also covers segregates such as
  *C. pallens* (= *C. subpruinosus*), *C. alborufescens*, *C. ferruginascens* and
  *C. amethysteus*, which differ in hosts and altitude. Say which taxa GBIF records under
  *C. cibarius* likely include, and whether the rules should target *C. cibarius* s.l.
- **Soil pH.** Document the acidic-soil dependence (the pH range and the sources). v1 cannot
  model soil chemistry, so write a dedicated "Soil pH: known gap" subsection: how strong the
  dependence is, what the grid could use as a proxy later (acidophilous hosts such as chestnut,
  lithology from a geological map, SoilGrids pH), and how its absence will bias scores
  (over-scoring on calcareous substrates).

Leads to check. These are unverified pointers; confirm them before citing, and find better
ones if you can:
- Pilz et al. 2003, *Ecology and management of commercially harvested chanterelle
  mushrooms* (USDA Forest Service PNW-GTR-576)
- Danell 1994 (Uppsala thesis on *C. cibarius* ecology); Jansen & van Dobben 1987 (*Ambio*,
  decline linked to acidification and nitrogen)
- Egli et al. 2006 (*Biological Conservation*, a long-term Swiss plot study); Straatsma et al.
  2001 (*Mycological Research*, 21 years of fruiting phenology)
- Olariaga et al. 2017 (*Fungal Diversity*, European *Cantharellus* revisited)
- Finnish and Baltic yield-vs-weather studies (e.g. Ohenoja; Salo)
- Italian sources: Università di Siena studies, AMB, and regional groups

**Write your draft to:** `.gavin-root/docs/drafts/species-ecology-gallinacci.md`

> Done 2026-09-17. The draft was merged as the evidence appendix `.gavin-root/docs/species-ecology/gallinacci.md`; its rules are encoded in `.gavin-root/docs/species-rules/`.

## Context

mushma estimates where and when wild mushrooms are likely to fruit in **Tuscany, Italy**.
It turns weather, habitat and terrain into a 0–1 **conditions score** per ~1 km woodland
cell, species and day, using transparent per-species rules. Every rule lives in config with a
cited `source` and a `confidence`. The scores are validated later against GBIF/iNaturalist
sightings. Read `.gavin-root/PRD.md` (sections Species, Model) for the full picture. This card
is research only: no code.

Your output feeds two things: `.gavin-root/docs/species-ecology.md` (the orchestrating
session merges your draft into it) and a YAML rule config that the M3 scoring engine loads.
So every rule must be **quantitative enough to encode** and **traceable to a source**.

## What to research (for each taxon in scope)

1. **Season windows in Tuscany.** When fruiting happens, including separate flushes
   (e.g. a late-spring flush and an autumn one). Give dates as a trapezoid
   `[zero_before, full_from, full_to, zero_after]` in `DD-MM`, and say how the window shifts
   with altitude when sources say so.
2. **Host trees and habitat.** Mycorrhizal hosts, ranked. Express them as an affinity 0–1
   for each term of the draft habitat vocabulary below. Add a term if the vocabulary is
   missing something that matters, and explain why.
3. **Altitude bands in Tuscany.** A trapezoid `[zero_below, full_from, full_to, zero_above]`
   in metres. Note any aspect (north/south slope) effects.
4. **Rain trigger.** How much rain is needed (mm, and over how many days) and the lag from the
   rain to fruiting (min / typical / max days). Give a lag trapezoid in days.
5. **Antecedent / cumulative moisture.** Rain or water balance over the preceding weeks or
   months, soil moisture thresholds, and summer drought legacy.
6. **Temperature.** Soil temperature band (and depth if the source says), air temperature band
   (Tmean / Tmax / Tmin), and whether a temperature drop or "thermal shock" triggers fruiting.
7. **Stoppers.** Drought, frost and cold nights (Tmin thresholds, how many nights), drying wind
   (tramontana, grecale), high evaporative demand (ET0, VPD), heat.
8. **Anything else that matters but cannot be modelled from the data we have** (soil pH, soil
   texture, stand age, canopy, litter, management). Flag it explicitly.

## Data the engine can use

Express rules against these inputs wherever possible (the orchestrator will do the exact
variable mapping):

- **Daily weather (Open-Meteo, local days in Europe/Rome):** precipitation sum; air
  temperature 2 m min/max/mean; soil temperature (a shallow layer ~0–7 cm and a deeper one
  ~7–28 cm); volumetric soil moisture (same layers); max wind speed and gusts at 10 m;
  reference evapotranspiration ET0 (FAO-56); vapour-pressure deficit; relative humidity;
  shortwave radiation; snowfall.
- **Static per cell:** elevation, slope, aspect, habitat class (vocabulary below).
- **Not available in v1:** soil pH/chemistry/texture, stand age, canopy cover, litter depth,
  management history. Rules that depend on these must be flagged, not dropped.

### Draft habitat vocabulary (provisional; the M2 woodland-grid card owns the final one)

Based on the Italian 4th-level Corine Land Cover forest classes and Regione Toscana forest types:

| key | covers |
|---|---|
| `beech` | faggete (*Fagus sylvatica*) |
| `chestnut` | castagneti, coppice and orchards (*Castanea sativa*) |
| `deciduous_oak` | cerrete, querceti di roverella / farnetto / rovere (*Quercus cerris, Q. pubescens, Q. frainetto, Q. petraea*) |
| `evergreen_oak` | leccete, sugherete (*Q. ilex, Q. suber*) |
| `mixed_broadleaf` | ostrieti, carpineti, acero-frassineti and other mesophile broadleaf |
| `riparian` | boschi igrofili (*Populus, Salix, Alnus*) |
| `robinia` | robinieti and other exotic broadleaf |
| `mediterranean_pine` | pinete di pino marittimo, domestico, d'Aleppo |
| `mountain_pine` | pinete di pino nero, pino silvestre (often reforestation) |
| `fir_spruce` | abetine (*Abies alba*), peccete (*Picea abies*), including plantations |
| `other_conifer` | douglasia, cedri, larici, cipressete |
| `mixed_broadleaf_conifer` | mixed conifer + broadleaf stands |
| `macchia` | Mediterranean maquis and shrubland (*Cistus, Arbutus, Erica*); may fall outside the woodland mask |

## Sources and confidence

Prefer, in this order: peer-reviewed phenology/productivity studies (ideally Italian or
Mediterranean), Italian mycological societies and institutions (AMB, the Associazione
Micologica Bresadola and its groups; regional mycological groups; Università di Siena and other
university mycology labs; Regione Toscana / ARSIA; CREA; IGP specifications such as *Fungo di
Borgotaro*), monographs by recognised mycologists, then everything else. Search in **Italian
as well as English** (e.g. "porcini fruttificazione temperatura suolo", "ovolo buono
habitat altitudine", "finferli pH suolo").

Mark each rule's confidence:

- **strong**: peer-reviewed quantitative field data linking fruiting to that factor, ideally
  Mediterranean/Italian, or several consistent peer-reviewed sources.
- **plausible**: qualitative statements from reputable mycological sources (societies,
  university/regional publications, expert monographs), or quantitative data from another
  climate or a close relative that you are extrapolating (say so).
- **folklore**: forager lore, blogs, forums, popular sayings and commercial sites with no
  traceable data. Folklore is still worth recording if it is widespread, because the
  backtest can test it.

**Source hygiene is non-negotiable.** Never invent a citation, DOI, page number or number.
Every reference needs a DOI or URL you actually found. Mark each reference `verified` if you
opened the page, abstract or PDF, or `snippet-only` if you only saw it in search results.
When you turn a qualitative statement into a number (e.g. "about two weeks after rain" into
a lag trapezoid of 8–12–18–25 days), mark the number as **derived** and say what it came from.
Record disagreements between sources instead of silently picking one.

**Safety.** The app forecasts conditions only. Write nothing about edibility, toxicity,
lookalikes-for-eating or how to identify specimens. Taxonomy notes are welcome when they affect
data, e.g. which taxa get lumped under a name in GBIF records, or which Mediterranean
segregates share a common name.

## Output

Write one markdown file at the path given in the task section below, using this structure:

```markdown
# <Common name (IT)>: <taxa> (draft for species-ecology.md)

## Scope and taxonomy notes
(synonyms, segregates, how records get lumped, what the common name covers in Tuscany)

## Rules summary
| id | taxon | factor | rule (plain words) | parameters | confidence | sources | data |
(one row per encodable rule; `parameters` uses trapezoids/thresholds with units;
`sources` are reference ids like [R3]; `data` = available / derived / missing)

## Evidence by factor
### Season windows
### Hosts and habitat affinity
### Altitude and aspect
### Rain trigger (amount, lag)
### Antecedent moisture
### Temperature
### Stoppers
### Not modellable in v1
(for each: what sources say, with [R#] cites, the numbers, the confidence, and derived-number notes)

## Disagreements and open questions

## References
- [R1] Full citation. DOI or URL. `verified` | `snippet-only`. What it supports.
```

Aim for depth over breadth: a few well-read primary sources beat many snippets. Stop once
every factor has either a sourced rule or an explicit "no source found" note.

When you finish, reply with **at most 250 words**: the output path, the 3–5 highest-confidence
rules, the weakest spots, and anything the orchestrator should know. Do not paste the file
back.
