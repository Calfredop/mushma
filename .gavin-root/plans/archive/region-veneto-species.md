---
kind: task
title: [region] Veneto — species research and rules
parent: region-veneto.md
complexity: complex
---
Species research for Veneto (child of `region-veneto.md`). Work in the region's checkout
(`/Users/coalpila/CloudStation/Coding/mushma-regions-1`, branch `region/veneto`). API id `veneto`,
ISTAT COD_REG 5, names "Veneto" / en "Veneto"; seven provinces (Belluno BL, Treviso TV, Vicenza VI,
Verona VR, Padova PD, Venezia VE, Rovigo RO).

From the Dolomites and the Prealps down to a forestless plain:
- **Dolomites (Belluno).** Cortina d'Ampezzo and the Val Boite (San Vito, Borca di Cadore), Cadore
  (Pieve di Cadore, Auronzo di Cadore, Lorenzago, Vigo di Cadore), Comelico and the Val Visdende,
  the Agordino (Agordo, Falcade, Canale d'Agordo, Alleghe, Rocca Pietore), the Val di Zoldo, the
  Feltrino (Feltre, Lamon, Sovramonte) and the Valbelluna, the Alpago and the **Cansiglio** forest
  (Tambre, Farra/Alpago, Fregona): spruce, silver fir, larch and stone pine, beech and spruce-fir-beech,
  Scots pine on the dry dolomite; mugo pine and green alder above the tree line.
- **Prealps.** The **Altopiano di Asiago / Sette Comuni** (Asiago, Gallio, Roana, Rotzo, Enego, Foza,
  Lusiana Conco), Tonezza, the Pasubio and Piccole Dolomiti (Recoaro Terme, Valli del Pasubio, Posina),
  **Monte Grappa** (Seren del Grappa, Pieve del Grappa, Borso del Grappa), the **Lessinia** (Bosco
  Chiesanuova, Erbezzo, Roverè Veronese, Selva di Progno, Velo Veronese, Sant'Anna d'Alfaedo) and the
  **Monte Baldo** (Ferrara di Monte Baldo, San Zeno di Montagna, Caprino Veronese, Brenzone sul Garda);
  the Treviso Prealps (Col Visentin, Monte Cesen; Valdobbiadene, Follina, Cison di Valmarino, Revine
  Lago, Vittorio Veneto): beech is the most extensive montane forest, hop-hornbeam and manna ash
  (the region's commonest forest type) and downy oak low down, spruce planted widely.
- **Hills.** The **Colli Euganei** (Teolo, Torreglia, Galzignano Terme, Arquà Petrarca, Rovolon, Vò,
  Baone; chestnut on the volcanic trachyte, downy oak and relict holm oak with Mediterranean
  elements), the **Colli Berici** (Arcugnano, Barbarano Mossano, Nanto, Zovencedo), the **Montello**
  (Volpago del Montello, Giavera del Montello, Nervesa della Battaglia, Montebelluna, Crocetta del
  Montello: robinia, oak-hornbeam, chestnut), the Asolo hills and Valpolicella: chestnut, sessile and
  downy oak, hop-hornbeam, robinia.
- **Plain and coast.** Almost no forest: relict oak-hornbeam woods (Bosco di Carpenedo, Bosco di
  Cessalto, Bosco di Olmè), the coastal pinewoods and holm oak of the Bosco Nordio (Chioggia), Rosolina
  / Porto Caleri, Bibione (San Michele al Tagliamento), Cavallino-Treporti, Eraclea, and the Po delta.

So all four porcini keys are plausible: *B. edulis* and *B. pinophilus* in the Dolomite and Prealpine
spruce, fir, beech and pine (Asiago, Cansiglio, Cadore and Comelico are the region's famous porcini
areas), *B. aereus* and *B. reticulatus* on the chestnut and oak of the Colli Euganei, the Berici, the
Montello and the Prealps' lower slopes; ovoli on the warm chestnut and oak hills (check the evidence:
Colli Euganei, Berici, Montello, Asolo, Valpolicella, Baldo and Lessinia low slopes); gallinacci under
spruce, fir and beech. Check the evidence for each, and drop what the region lacks and say so. Veneto
has its own collecting law (L.R. 19 agosto 1996, n. 23 and its later changes, with provincial and
comunità montana rules: the Sette Comuni and Belluno permits; find the current law and cite it
correctly); it does not change the rules, but the local press around it is a source of season
reports.

The forest map the grid will use is the Region's **Carta regionale delle categorie forestali**
(Regione del Veneto, Del Favero et al. 2000 typology, the same family as Friuli-Venezia Giulia's; about
418,000 ha of polygons with cover over 30 %), whose areas by category are: orno-ostrieti e
ostrio-querceti 81,000 ha, faggete 75,000, formazioni antropogene 52,000 (conifer plantations 29,000,
robinia 18,000), peccete 49,000, lariceti e larici-cembreti 34,000, mughete 28,000, abieteti 23,000,
castagneti e rovereti 20,000, pinete di pino silvestre 13,000, piceo-faggeti 11,000, saliceti e
formazioni riparie 9,000, aceri-frassineti 9,000, querco-carpineti e carpineti 5,000, arbusteti 4,000,
alnete 3,000, formazioni euganee con elementi mediterranei 800, formazioni costiere 500, betuleti 200.
The grid will map it to the habitat vocabulary (`api/src/api/config/habitats.yaml`) roughly as
Friuli-Venezia Giulia did: spruce and silver fir → `fir_spruce`, larch and stone pine →
`other_conifer`, Scots pine and black-pine plantations → `mountain_pine`, coastal stone and maritime
pine → `mediterranean_pine`, beech → `beech`, chestnut → `chestnut`, sessile oak, ostrio-querceti,
querco-carpineti and the Euganean oak woods → `deciduous_oak`, orno-ostrieti, carpineti,
aceri-frassineti, birch → `mixed_broadleaf`, spruce-beech → `mixed_broadleaf_conifer`, robinia →
`exotic_broadleaf`, riparian willow and alder → `riparian`, holm oak → `evergreen_oak`, the Euganean
pseudomacchia and coastal scrub → `macchia`, mugo pine, green alder and arbusteti → transitional (not
woodland). Check `api/src/api/config/regions/veneto.yaml` once it exists for the final mapping, and say
in the doc which habitat holds which tree of the region. Hop-hornbeam is the region's commonest forest:
weigh its affinity for each species carefully.

Deliver:
- `.gavin-root/docs/species-ecology/veneto.md`: the regional evidence (season windows, host trees and
  habitat affinities, altitude bands, weather rules where regional literature exists), each claim
  cited, with a confidence (`strong` / `plausible` / `folklore`, as in `species-ecology.md`). Follow
  the shape of `species-ecology/friuli_venezia_giulia.md` and `species-ecology/trentino_alto_adige.md`
  (the two neighbours with the same kind of Alps and Prealps), and read `lombardia.md` and
  `emilia_romagna.md` for method and sources. Sources: the Associazione Micologica Bresadola (founded
  in Trento; its Veneto groups: Vicenza, Verona, Padova, Treviso, Belluno, Asiago, Schio, Bassano…),
  the Università di Padova (Dipartimento TESAF, forest ecology and mycology) and the Museo di Storia
  Naturale di Verona, Veneto Agricoltura (which manages the Cansiglio and the regional forests), the
  Regione's forest directorate and its forest-type books (Del Favero et al. 2000, the Carta forestale
  documento base), ARPAV, the Carabinieri forestali and the USL mycological inspectorates (ispettorati
  micologici, which publish season notes); press: Il Gazzettino, Corriere delle Alpi, Il Giornale di
  Vicenza, L'Arena, Il Mattino di Padova, La Tribuna di Treviso, La Nuova Venezia, Corriere del Veneto,
  L'Amico del Popolo, BellunoPress, the Asiago and Cadore local sites, and mushroom forums and blogs.
- `api/src/api/config/species/veneto/` started from `tuscany/` (look at `friuli_venezia_giulia/` and
  `trentino_alto_adige/` first for how the neighbouring Alpine regions retuned, then `lombardia/`,
  `piemonte/` and `emilia_romagna/`): per-species YAML with season windows, habitat affinities and
  altitude bands retuned for the region; every factor cited with a confidence; groups or keys the
  region lacks dropped and the doc says so. Woodland spans sea level (the coast and the Colli Euganei)
  to about 2,100 m (Dolomites): check the altitude bands and the season windows by elevation carefully.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys unique;
  open every source you cite). Put them in their own block for this region at the end of the file, so
  merges with other region branches stay simple.
- `veneto/sanity.yaml`: press or blog contrasts for the region's areas (comuni) and years (2016-2025),
  written before any score exists, in the same format as the other regions'. Aim for 12-16 contrasts
  across the Dolomites, the Prealps (Asiago, Grappa, Lessinia, Baldo, Cansiglio) and the hills (Colli
  Euganei, Berici, Montello); a gallinacci and an ovoli contrast are welcome if the press has them.
  Name comuni exactly as ISTAT 2025 names them (check against the ISTAT boundaries file cached under
  `/Users/coalpila/CloudStation/Coding/mushma/api/data/raw/istat/`; several Belluno and Vicenza comuni
  merged recently: Val di Zoldo, Alpago, Borgo Valbelluna, Lusiana Conco, Pieve del Grappa, Valbrenta,
  Barbarano Mossano).
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

Open-Meteo's free quota is shared by every lane on this machine: do not call Open-Meteo (use the DEM
tiles under the data root for elevations if you need them).

Do not commit and do not edit any plan card.
