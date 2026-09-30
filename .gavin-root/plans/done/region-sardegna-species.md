---
kind: task
title: [region] Sardegna — species research and rules
parent: region-sardegna.md
complexity: complex
---
Species research for Sardegna (child of `region-sardegna.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-1`, branch `region/sardegna`). API id
`sardegna`, ISTAT COD_REG 20. The island, from sea level to the Gennargentu (Punta La Marmora,
1,834 m), with its small islands (La Maddalena, Asinara, San Pietro, Sant'Antioco). Its woods are
about a quarter of the land (INFC 2015 bosco 626,140 ha, the third largest in Italy) and it has
as much again of macchia. **Beech is absent from Sardinia**, and so are silver fir and spruce: the
porcini ground is oak (cork, holm, deciduous), chestnut and conifer reforestation. The mountain
blocks (verify, refine and add):

- **Gennargentu and Barbagia** (schist and granite, acid soils): holm oak to about 1,200–1,400 m,
  deciduous oaks (*Quercus pubescens* s.l., *Q. ichnusae*, *Q. congesta*) higher, yew and holly
  relicts, chestnut and hazel orchards at 600–1,100 m (Aritzo, Desulo, Tonara, Belvì, Meana Sardo,
  Sorgono, Atzara), black pine and other conifer reforestation on the massif (Fonni, Desulo,
  Villagrande Strisaili, Arzana, Seulo, Seui's Montarbu). Comuni: Fonni, Desulo, Tonara, Aritzo,
  Belvì, Gadoni, Seulo, Seui, Villagrande Strisaili, Arzana, Talana, Urzulei, Orgosolo, Mamoiada,
  Gavoi, Ollolai, Ovodda, Sorgono.
- **Supramonte and Ogliastra** (limestone): holm oak (Orgosolo, Oliena, Dorgali, Urzulei, Baunei).
- **Montiferru** (volcanic, Monte Urtigu 1,050 m): holm oak, deciduous oak, chestnut (Santu
  Lussurgiu, Seneghe, Cuglieri, Bonarcado, Scano di Montiferro).
- **Marghine and Goceano** (Monte Rasu 1,259 m): deciduous and holm oak, the Burgos and Anela
  forests (Bono, Bolotana, Macomer, Silanus, Burgos, Anela, Bultei, Illorai, Nughedu San Nicolò).
- **Monte Acuto and the Alà plateau** (granite): cork oak and deciduous oak (Alà dei Sardi, Buddusò,
  Pattada with the Foresta di Monte Lerno, Osidda, Bitti, Nule, Benetutti, Monti, Berchidda,
  Oschiri).
- **Gallura and Limbara** (granite, Monte Limbara 1,362 m): cork oak (Tempio Pausania,
  Calangianus, Luras, Aggius, Luogosanto, Bortigiadas), maritime and black pine reforestation on
  the Limbara, holm oak.
- **Sulcis-Iglesiente** (Monte Linas 1,236 m, Marganai, Monte Arcosu, Gutturu Mannu, Pantaleo):
  the island's largest holm oak woods, cork oak, pine and eucalyptus (Iglesias, Domusnovas,
  Fluminimaggiore, Villacidro, Gonnosfanadiga, Arbus, Santadi, Nuxis, Assemini, Uta, Capoterra,
  Siliqua, Teulada, Domus de Maria, Pula).
- **Sarrabus and Sette Fratelli** (granite): holm and cork oak (Burcei, Sinnai, Castiadas, San Vito,
  Villasalto, Muravera). **Sarcidano and Monte Arci**: Laconi, Isili, Nurallao; Morgongiori, Ales,
  Pau, Marrubiu. **Nuorese**: Monte Ortobene (Nuoro), Bitti, Lodè and Monte Albo, Siniscola, Lula.
- Coastal pine (stone and Aleppo pine: Is Arenas at Narbolia, Platamona at Sorso, Porto Pino,
  Buggerru), eucalyptus plantations (Arborea, Terralba, the Sulcis, the Nurra).
- Climate: Mediterranean with a long dry summer (June–September) and rain from October to April,
  about 500 mm on the Campidano and the south coast, 1,000–1,400 mm on the Gennargentu, Limbara and
  Montiferru crests; snow on the Gennargentu in winter; the maestrale dries the west.

Deliver:
- `.gavin-root/docs/species-ecology/sardegna.md`: the regional evidence (season windows, host
  trees and habitat affinities, altitude bands, weather rules where regional literature exists),
  each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Sicilia is the nearest precedent (`species-ecology/sicilia.md` and
  `api/src/api/config/species/sicilia/` on this branch), then Calabria, Campania and Puglia (all
  merged here). Say where Sardinia departs from Sicily and from the central-Italian windows.
  Questions that matter most: **the season** (autumn from October into December or January, when
  the first autumn rains start it; is there a spring flush in April–June in the cork oak and
  holm oak; how late *B. aereus* runs); **which porcini Sardinia actually has** (*B. aereus* is
  likely the leading taxon; is *B. edulis* present without beech, and where: chestnut, deciduous
  oak at height, the pine reforestation? *B. reticulatus* in the deciduous oak and chestnut? *B.
  pinophilus* under the reforestation pines?); **cork oak** as porcini, ovolo and chanterelle ground
  (the Gallura and the Alà plateau); **the reforestation** (maritime, black, Aleppo and stone pine;
  eucalyptus) and **the macchia** (does anything we score fruit under *Arbutus*, *Erica*, *Cistus*?
  the grid files macchia as non-woodland, so this only matters for mixed cells); and whether *A.
  caesarea* and *C. cibarius* are frequent enough to keep. Look for Sardinian checklists and
  mycologists (Marco Contu's papers, the Associazione Micologica Bresadola groups in Sardinia,
  university checklists of Sassari and Cagliari, Sardegna Foreste / Agenzia Forestas, which is
  already in the bibliography), and the regional law on picking epigeous mushrooms and its
  implementing rules (to verify; it belongs in the doc).
- `api/src/api/config/species/sardegna/` started from `tuscany/` (look at `sicilia/`, `calabria/`,
  `campania/`, `puglia/`, `lazio/` for how other regions retuned): per-species YAML with season
  windows, habitat affinities and altitude bands retuned for Sardinia; every factor cited with a
  confidence; groups or keys the region lacks dropped and the doc says so. Altitude bands matter:
  Sardinia's woods run from the coast to about 1,500 m (the Gennargentu tree line is low and
  grazed), the oaks from the coast to about 1,400 m, chestnut at 500–1,100 m. Beech is absent, so a
  key that leans on beech must find its Sardinian hosts or be dropped.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique across the file, prefix new keys `sar_` or infix `_sardegna_`; open every source you
  cite). The only unmerged region branch, `region/basilicata`, appends its block at the end of the
  file; put all of yours in **one block of their own, inserted right after the last Sicilia entry
  and before the Calabria block's comment header** (`# Calabria (region card, 2026-09-28)`), with a
  comment header like Sicilia's, so the branches merge cleanly.
- `sardegna/sanity.yaml`: press or blog contrasts for Sardinia's areas (comuni) and years (La Nuova
  Sardegna, L'Unione Sarda, Sardinia Post, Vistanet, Olbia.it, Gallura Oggi, Cagliaripad,
  Castedduonline, SardegnaLive, Funghi Magazine's national bulletins through Wayback captures, the
  forestry agency, mycological groups), reporting porcini (and ovoli or chanterelle, if any)
  seasons on the Gennargentu and Barbagia, the Montiferru, the Marghine-Goceano, the Alà plateau,
  the Gallura and Limbara, the Sulcis-Iglesiente and the Sette Fratelli, written before any
  Sardinia score exists, in the same format as the other regions'. Contrasts are porcini unless
  the id starts with the group (`ovoli_...`, `gallinacci_...`). Every `comune` must be an ISTAT 2025
  comune name inside Sardinia (check against the ISTAT 2025 boundaries the grid uses; Sardinia's
  provinces were redrawn in 2016 and again in 2025, the comuni were not, but a few names are
  bilingual or changed spelling).
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid's forest source is being
settled in parallel (`api/src/api/config/regions/sardegna.yaml`, the parent session): the
Regione Sardegna's Carta dell'uso del suolo (CLC legend to the 4th–5th level, which splits cork
oak, chestnut and eucalyptus) or CLC 2018 IV level. Expect holm and cork oak → `evergreen_oak`,
downy oak s.l. → `deciduous_oak`, chestnut → `chestnut`, maritime, Aleppo and stone pine →
`mediterranean_pine`, black pine → `mountain_pine`, eucalyptus → `exotic_broadleaf`, poplar,
willow, alder and oleander → `riparian`, macchia → `macchia`, regrowth and sparse woods →
`transitional_woodland_shrub`; no beech, no fir_spruce. The parent session will send the exact
class mapping with its areas, then each habitat's median elevation and dominant cells once the
grid is built. Say in the doc which habitat holds which Sardinian tree.

Do not commit and do not edit any plan card.
