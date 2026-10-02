# Proximity to water: not a model factor

Researched 2026-10-02. Card: `[model] proximity to water bodies`
(`plans/algo-proximity-to-water-bodies.md`). Traces to PRD → Model (transparent per-species rules
over weather, habitat and terrain) and to `species-ecology.md`.

**Question.** Should distance to rivers, streams, lakes or the sea change the conditions score? Does
flooding wash spores away and kill mycelium near water, or does the extra humidity help?

**Answer: no new factor.** No study measures porcini, ovolo or chanterelle yield or occurrence
against distance to a stream, lake or the sea. Every effect with evidence acts at metres to a few
hundred metres, well below the 1 km cell:

- **On stream banks and in floodplains (about 0–50 m, a few hundred metres on big rivers): negative.**
  Saturated soil suppresses ectomycorrhiza, the riparian trees host other fungi, and *Phytophthora*
  follows drainage lines.
- **On the lower slope beside a floodplain (metres to tens of metres): weakly positive in drought
  years.** This rests on one observation of *B. edulis*, and the one census of fruiting by
  topography found the opposite.
- **Coast:** salt spray falls to background within about 1 km. No positive maritime effect is
  documented for these species.
- **Lakes:** nothing found.
- **Spores washed away by floods:** irrelevant. These species fruit from perennial mycelium on living
  hosts, not from spores.

The model already covers the parts of this that a 1 km cell can see. Riparian woods score 0 (or
0.05–0.1) for every Tuscan species, and moisture enters through rain, water balance, soil moisture,
slope and sun exposure.

## What the model has today

- **Habitat.** `riparian` (CLC IV 3116: pioppeti, saliceti, ontanete) is a non-host in every Tuscan
  rule: 0 for *B. edulis*, *B. aereus*, *B. pinophilus* and *A. caesarea*, 0.05 for
  *B. reticulatus*, 0.1 for gallinacci (`api/src/api/config/species/tuscany/*.yaml`). The habitat
  score is a host-weighted share of the cell, so a cell that is mostly riverside wood already scores
  low.
- **Moisture.** Rain trigger and 30-day rain for porcini, and water balance and drought stoppers
  for gallinacci. The `soil_moisture` percentile (porcini) and the `waterlogging` stopper (ovoli,
  ≥ 0.40 m³/m³ → ×0.8) exist but are disabled.
- **Terrain.** Slope (steep ground drains fast; Beven & Kirkby 1979 is already cited there) and
  sun exposure from aspect.
- **No hydrography.** No river, lake or coastline layer, no distance to water and no topographic
  wetness index (TWI).

## Evidence

Each source below was read in full or in abstract unless it says *via citing source*. Kinds: primary
field study, lab or pot experiment, review, guide or folklore.

### Flooding and waterlogging: negative

| source | what and where | finding | kind / confidence |
|---|---|---|---|
| Lodge 1989, *Plant and Soil* 117:243, [doi](https://doi.org/10.1007/BF02220718) | *Populus*, *Salix*; moisture and flooding treatments and field drainage transects | Ectomycorrhiza formed only in "very moist but well-drained" soil (0 to −0.2 MPa). Arbuscular mycorrhiza spanned flooded soil to −3.4 MPa. Three months of flooding replaced ectomycorrhiza with arbuscular mycorrhiza. | experiment + field / high for the direction |
| Stenström 1991, *Plant and Soil* 131:247, [doi](https://doi.org/10.1007/BF00009455) | *Pinus sylvestris* seedlings, periodic root flooding | *Thelephora*, *Laccaria* and *Hebeloma* tolerated it. *Suillus bovinus* and *S. flavidus* (Boletales) failed to colonise even at 2 min of flooding a day. | lab / medium |
| Barnes et al. 2018, *New Phytologist* 220:1172, [doi](https://doi.org/10.1111/nph.14990) | UK willow coppice, 3 years either side of a 1-in-100-year rain | Ectomycorrhizal richness and relative abundance fell by more than half, while saprotrophs and pathogens rose. | field / high, other host |
| Thomas 2021, *Mycorrhiza* 31:511, [doi](https://doi.org/10.1007/s00572-021-01035-4) | *Tuber aestivum* on *Quercus robur*, root submersion 7–65 days | 7 days cut ectomycorrhizal tips from 26.5 to 14.75 per zone. Longer floods cut no further, and colonisation recovered. Floods injure the mycelium but do not kill it. | pot / medium |
| Corcobado et al. 2013, [doi](https://doi.org/10.1016/j.agrformet.2012.09.017); 2014, [doi](https://doi.org/10.1016/j.foreco.2014.03.040); 2015, [doi](https://doi.org/10.1093/forestry/cpu056) | *Quercus ilex* dehesas, western Spain, stream banks against slopes | Trees on stream banks (waterlogged 1–2 months a year) had fewer fine roots and fewer vital ectomycorrhizal tips, and higher *Phytophthora cinnamomi* mortality. Topography did not change the seasonal dynamics of ectomycorrhizal abundance. | field / medium-high; the closest Mediterranean analogue |
| Tedersoo et al. 2009, [doi](https://doi.org/10.1111/j.1469-8137.2009.02792.x); Roy et al. 2013, [doi](https://doi.org/10.1111/nph.12212); Põlme et al. 2013, [doi](https://doi.org/10.1111/nph.12170) | *Alnus* ectomycorrhizal communities, global | Species-poor (86 taxa over 5 alder hosts) and dominated by *Alnicola*, *Alpova* and *Tomentella*. No *Boletus*, *A. caesarea* or *Cantharellus*. | field surveys / high; supports riparian = non-host |
| Jurgensen et al. 1997, *Wetlands Ecology and Management*, [link](https://research.fs.usda.gov/treesearch/59695) | US bottomland hardwoods | Ectomycorrhiza is more flood-sensitive than arbuscular mycorrhiza, which persists in permanently flooded soil. | review / medium |

### Humidity near water and topographic wetness: weak and mixed

| source | what and where | finding | kind / confidence |
|---|---|---|---|
| Lilleskov et al. 2009, *New Phytologist* 182:483, [doi](https://doi.org/10.1111/j.1469-8137.2009.02775.x) | Sierra Nevada pine, summer drought | Stated as background: *B. edulis* was seen "fruiting heavily along hillslopes adjacent to floodplains". In dry soil, sporocarps took 25–80 % of their water from deep (> 30 cm) or hydraulically lifted water. | observation, not a tested predictor / low-medium for the pattern |
| Tsujino et al. 2009, *Mycoscience* 50:388, [doi](https://doi.org/10.1007/s10267-009-0494-0) | Yakushima warm-temperate broadleaf forest, line census of ridges against valleys | Ectomycorrhizal fruitbodies: 26.7 per km on ridges against 8.7 per km in valleys. Saprotrophs: 12.5 against 25.0. Boletaceae and Amanitaceae were among the families recorded. | field / medium (other biome); points **away** from valley bottoms |
| Bonet et al. 2008, [doi](https://doi.org/10.1051/forest:2007089); 2010, [doi](https://doi.org/10.1139/X09-198) | Pyrenean pine yield models | Predictors: basal area, slope, elevation, aspect, autumn rain. No distance to water and no TWI term. | field / high that hydrography is absent |
| Martínez-Peña et al. 2012 (Soria *B. edulis* yield model) | *P. sylvestris*, 18 plots over 15 years | Rain, temperature, basal area, slope, aspect and elevation. No hydrography. | field / high (*via citing source*) |
| Karavani et al. 2018, [doi](https://doi.org/10.1016/j.agrformet.2017.10.024); Ágreda et al. 2015, [doi](https://doi.org/10.1111/gcb.12960) | Mediterranean pine yield | Soil moisture and water balance drive yield, and water deficit limits it. A wet site helps only by easing that deficit, and these models get it from weather and soil, not hydrography. | field / high for the mechanism |
| Fink et al. 2021, *Fungal Ecology* 49:100981, [doi](https://doi.org/10.1016/j.funeco.2020.100981) | 990 Swiss macrofungi from citizen science | Only 15 % showed riparian affinity, mostly wood-decay and soil saprobes. | field / medium |
| Fire 2025, 8:438, [doi](https://doi.org/10.3390/fire8110438) | Mediterranean relict forest after fire | TWI had a weak positive effect on mycorrhizal *richness*, not yield. | field / low |

**Gallinacci and ovoli.** Neither has a field study of moisture position. Gallinacci are described on
well-drained, acid, nutrient-poor soils, with yield following rain in the weeks before. Ovoli are
thermophilic and "absent from overly wet areas", which is guide literature, the same basis as the
disabled `waterlogging` stopper.

### Coast: salt spray within a few hundred metres

- Ectomycorrhizal salt tolerance varies widely by species. The evidence is in vitro or on seedlings
  (*Cenococcum* inhibited above 200 mM NaCl, *Suillus granulatus* tolerant; *Laccaria* and
  *Pisolithus* colonisation cut by 80 mM, [doi](https://doi.org/10.1007/BF00210694)). In a Yellow
  Sea *Pinus thunbergii* survey ([PMC8105453](https://pmc.ncbi.nlm.nih.gov/articles/PMC8105453/))
  most ectomycorrhizal species sat where soil Na⁺ was low. None of this concerns our species in the
  field.
- Chloride deposition falls off exponentially inland, mostly within 100–400 m of the shore and near
  background by about 1 km (Guan et al. 2010, *HESS* 14:801; *Hydrological Processes* 2023,
  [doi](https://doi.org/10.1002/hyp.15052)).
- Coastal fog wets soil in Californian pine and redwood (Fischer et al. 2016,
  [doi](https://doi.org/10.1002/ecs2.1364)). No study links it to ectomycorrhizal fruiting.
- No macrofungal yield study or checklist for porcini, ovoli or gallinacci in the Tuscan coastal
  pinewoods (San Rossore, Migliarino) turned up. What literature there is names *Suillus*
  (*S. bellinii*, *S. mediterraneensis*, *S. collinitus*), not *Boletus edulis* s.l. The coastal
  *B. aereus* in holm oak recorded for Abruzzo (`regions/abruzzo.md`, Torino di Sangro) is a habitat
  signal (holm oak), not a sea signal.

### Lakes: nothing found

No study links lake microclimate (fog, humidity, milder frost) to ectomycorrhizal or edible-mushroom
fruiting. Any temperature or humidity buffering would reach the model through the weather inputs.

### Spores and flooding: not a mechanism for fruiting

- 95 % of basidiospores land within about 1 m of the cap (Galante et al. 2011, *Mycologia* 103:1175,
  [doi](https://doi.org/10.3852/10-388)).
- Ectomycorrhizal spore banks are made up of *Rhizopogon*, *Wilcoxina*, *Cenococcum*, *Suillus*,
  *Tuber* and *Laccaria*, and overlap little with the mature-forest community (Glassman et al. 2015,
  [doi](https://doi.org/10.1111/nph.13240)). They hold no *Boletus*, *Amanita* or *Cantharellus*.
- Porcini, ovoli and gallinacci fruit from established perennial mycelium on living hosts. A flood
  carrying spores away does not change whether a stand fruits. The real flood effect is the
  waterlogging of the mycelium above.

### Phytophthora along drainage lines: negative, local

- Chestnut ink disease (*P. cambivora*) in central Italy "occurred preferentially along natural
  drainage routes". Incidence, severity and mortality fall with distance from them, at stand scale
  (Vannini et al. 2010, *Forest Pathology* 40:73,
  [doi](https://doi.org/10.1111/j.1439-0329.2009.00609.x); Vannini et al. 2021,
  [doi](https://doi.org/10.1111/efp.12722)). Rain above 1,000 mm a year with a short summer drought
  raises the risk (Vettraino et al. 2001, [doi](https://doi.org/10.1046/j.1365-3059.2001.00528.x); 2005, [doi](https://doi.org/10.1007/s10658-004-1882-0); *via citing source*).
- Holm-oak mortality from *P. cinnamomi* is higher on stream banks (Corcobado, above).
- This lowers chestnut and oak hosts (porcini, ovoli) in drainage lines over tens of metres. Where
  stands have died or changed type, the forest map already sees it.

## Why not a factor at 1 km

1. **Scale.** Every mechanism acts at metres to a few hundred metres. In hilly Tuscany most woodland
   cells should hold a stream channel or sit next to one (not measured: there is no hydrography
   layer in the grid), so a cell's distance to the nearest stream would be near zero almost
   everywhere and carry little signal.
2. **Both signs.** Close to water is negative (saturation, non-host trees, *Phytophthora*). Lower
   slopes beside a floodplain might be positive in drought years, but only one source says so.
   Netting the two inside a cell has no source to cite.
3. **Already counted.** The strongest negative, riparian wood, is in the habitat score. The moisture
   benefit is what rain, water balance and the soil-moisture factors model directly. A second
   moisture proxy would count the same water twice, the same reason `slope` acts on the score and
   never on the rain.
4. **Confounded.** Valleys and coasts are where the farmland, towns, roads and paths are. A sightings
   test would find an access-bias "near water" effect that is not ecology.
5. **No rule to cite.** "Rules are data" needs a source and a confidence. The only one available
   would be folklore, against high-confidence studies saying the wet end is bad for
   ectomycorrhiza.

## If it is ever revisited

These are possible later steps, none on the board, and none worth doing before the backtest shows a
residual in wet valley bottoms:

- **A floodplain share (negative).** Share of each cell inside mapped flood-hazard zones (ISPRA
  *Mosaicatura pericolosità idraulica*, P3 high-frequency areas) as a habitat-weight cut, at
  `plausible` confidence. It reads the mapped saturated ground directly, not a distance.
- **A coastal strip.** Forest within about 300 m of the shoreline as a small habitat-weight cut.
  Low priority: Tuscany's coastal woods are mostly stone and maritime pine, already a weak habitat
  for these species.
- **The existing switches.** Enabling the `waterlogging` stopper (ovoli) or the `soil_moisture`
  percentile (porcini) tests the wet-soil hypothesis with data the model already has.

## Not found

- Any study of porcini, ovolo or chanterelle yield or occurrence against distance to a stream,
  river, lake or coast.
- Any mushroom yield model (Spanish, Catalan, Finnish, Swedish, Italian) with TWI or a distance to
  water among its predictors.
- Any field study of *A. caesarea* habitat moisture.
- Full texts of Cho et al. 2021 (*Pinus densiflora* seedlings under flooding,
  [doi](https://doi.org/10.3390/su13084367)) and Lilleskov 2009 were paywalled. The Lilleskov
  floodplain observation is from the abstract and introduction.
