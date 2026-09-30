---
kind: task
title: [region] Friuli-Venezia Giulia — species research and rules
parent: region-friuli-venezia-giulia.md
complexity: complex
---
Species research for Friuli-Venezia Giulia (child of `region-friuli-venezia-giulia.md`). Work in the
region's checkout (`/Users/coalpila/CloudStation/Coding/mushma-regions-2`, branch
`region/friuli-venezia-giulia`). API id `friuli_venezia_giulia`, ISTAT COD_REG 6, names
"Friuli-Venezia Giulia" / en "Friuli-Venezia Giulia".

The region runs from the Adriatic to the Austrian and Slovenian borders in about 100 km:
- **Alps.** Carnic Alps and Carnia (Forni di Sopra, Forni Avoltri, Sauris, Ampezzo, Ovaro, Paluzza,
  Paularo, Arta Terme, Tolmezzo, Monte Zoncolan), the Val Canale and Canal del Ferro with the
  Tarvisio state forest (Tarvisio, Malborghetto Valbruna, Pontebba, Chiusaforte, Dogna) and the
  Julian Alps (Val Raccolana, Sella Nevea, Resia): spruce, silver fir, larch, beech and
  spruce-fir-beech; native black pine (*Pinus nigra*) and Scots pine on the Carnian dolomite.
- **Prealps.** Prealpi Carniche (Val Tramontina, Val Cellina and Val Colvera: Claut, Cimolais,
  Erto e Casso, Barcis, Andreis, Frisanco; Piancavallo above Aviano; the FVG side of the Cansiglio
  at Budoia, Caneva, Polcenigo; Val d'Arzino) and Prealpi Giulie (Valli del Natisone: Pulfero,
  San Pietro al Natisone, Savogna, Stregna, Monte Matajur; Val Torre: Lusevera, Taipana): beech is
  the most extensive forest, with hop-hornbeam and manna ash low down; chestnut and sessile oak on
  the flysch and marl.
- **Hills.** The Collio and Colli Orientali (Cividale, Prepotto, Dolegna del Collio, San Floriano
  del Collio, Bosco Romagno), the moraine hills (Fagagna, Buja, Colloredo di Monte Albano):
  chestnut, sessile oak, robinia.
- **Karst.** The Carso of Trieste and Gorizia (Duino Aurisina, Sgonico, Monrupino, Doberdò del Lago,
  Basovizza): downy oak, Turkey oak and hop-hornbeam scrub, and extensive black-pine
  reforestations from the late 1800s.
- **Plain and coast.** Relict lowland oak-hornbeam woods (Bosco Baredi and Coda di Manin at
  Muzzana del Turgnano, Bosco Bando) and the coastal pinewoods of Lignano (maritime and black
  pine).

So all four groups are plausibly present: *B. edulis* and *B. pinophilus* in the Carnian and Julian
spruce, fir, beech and pine, *B. aereus* and ovoli on the chestnut and oak of the Collio, the
Prealps' lower slopes and the Karst, gallinacci under spruce and beech. Check the evidence for each
(ovoli and *B. aereus* especially), and drop what the region lacks and say so. FVG has its own
collecting law (regional licence and daily limits; find the current law and regolamento and cite
them correctly); it does not change the rules, but the local press around it is a source of season
reports.

Deliver:
- `.gavin-root/docs/species-ecology/friuli_venezia_giulia.md`: the regional evidence (season
  windows, host trees and habitat affinities, altitude bands, weather rules where regional
  literature exists), each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as
  in `species-ecology.md`). Follow the shape of `species-ecology/piemonte.md` on this branch, and
  read the two Alpine regions not yet merged for their method and sources:
  `git show origin/region/trentino-alto-adige:.gavin-root/docs/species-ecology/trentino_alto_adige.md`
  (the nearest analogue for the Carnic and Julian spruce and fir) and
  `git show origin/region/lombardia:.gavin-root/docs/species-ecology/lombardia.md`.
  Slovene, Austrian (Carinthian) and Italian sources all count: Associazione Micologica Bresadola
  and its FVG groups (Gruppo Micologico Friulano, the Trieste and Pordenone groups), Università di
  Udine and Trieste, ERSA and the Direzione centrale risorse agroalimentari forestali (Corpo
  forestale regionale, the state forest of Tarvisio), Museo Friulano di Storia Naturale,
  Slovenian Forestry Institute / Gozdarski inštitut and Mikološka zveza Slovenije for the Julian
  Alps and the Karst; press: Messaggero Veneto, Il Piccolo, Il Gazzettino (Pordenone and Udine
  editions), Telefriuli, Il Friuli, Primorski dnevnik.
- `api/src/api/config/species/friuli_venezia_giulia/` started from `tuscany/` (look at
  `piemonte/` first for how an Alpine region retuned, then the Trentino and Lombardia sets on
  their branches with `git show origin/region/<branch>:api/src/api/config/species/<id>/…`, then
  `emilia_romagna/`, `liguria/`, `marche/`, `umbria/`): per-species YAML with season windows,
  habitat affinities and altitude bands retuned for the region; every factor cited with a
  confidence; groups or keys the region lacks dropped and the doc says so. Woodland spans sea level
  (Karst, Lignano) to about 1,900 m (Carnia, Tarvisio): check the altitude bands and the season
  windows by elevation carefully.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique, also against the keys the Trentino and Lombardia branches add; open every source you
  cite). Put them in their own block for this region at the end of the file so merges with other
  region branches stay simple.
- `friuli_venezia_giulia/sanity.yaml`: press or blog contrasts for the region's areas (comuni) and
  years (2016-2025), written before any score exists, in the same format as the other regions'.
  Aim for 12-16 contrasts across the Alps, Prealps and hills (Karst if the evidence is there);
  name comuni exactly as ISTAT 2025 names them (check against the ISTAT boundaries file cached
  under `/Users/coalpila/CloudStation/Coding/mushma/api/data/raw/`; FVG has bilingual ISTAT names
  for some comuni, e.g. on the Karst).
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid will map the region's forest
map to it roughly as Piemonte and Trentino did: spruce and silver fir → `fir_spruce`, larch →
`other_conifer`, Scots and black pine → `mountain_pine` (the Karst's black-pine reforestations
included), maritime and stone pine at Lignano → `mediterranean_pine`, beech → `beech`, chestnut →
`chestnut`, oaks → `deciduous_oak`, hop-hornbeam, ash-maple, hornbeam, birch → `mixed_broadleaf`,
spruce-fir-beech → `mixed_broadleaf_conifer`, robinia → `exotic_broadleaf`, riparian alder/willow
→ `riparian`, mugo pine and green-alder scrub → transitional (not woodland). Check
`api/src/api/config/regions/friuli_venezia_giulia.yaml` once it exists for the final mapping, and
say in the doc which habitat holds which tree of the region.

Open-Meteo's free quota is shared by every lane on this machine: do not call Open-Meteo (use the
DEM tiles under the data root for elevations if you need them).

Do not commit and do not edit any plan card.
