---
kind: task
title: [region] Valle d'Aosta — species research and rules
parent: region-valle-d-aosta.md
complexity: complex
---
Species research for Valle d'Aosta (child of `region-valle-d-aosta.md`). Work in the region's
checkout (`/Users/coalpila/CloudStation/Coding/mushma-regions-1`, branch `region/valle-d-aosta`).
API id `valle_d_aosta`, ISTAT COD_REG 2, names "Valle d'Aosta" / en "Aosta Valley"; officially
bilingual (Italian and French), so place names come in both forms.

The region is small (3,261 km²) and wholly Alpine: the Dora Baltea valley from Courmayeur and the
Valdigne down through Aosta to the Bassa Valle (Pont-Saint-Martin, Donnas, Bard, Arnad, Verrès),
and its side valleys: Val Ferret and Val Veny, La Thuile, Valgrisenche, Val di Rhêmes,
Valsavarenche and Val di Cogne (Gran Paradiso), Valle di Champorcher and the Mont Avic park
(Champdepraz), Val Clavalité (Fénis), the Gran San Bernardo valley (Étroubles, Saint-Oyen,
Saint-Rhémy-en-Bosses), Valpelline and Ollomont, Saint-Barthélemy (Nus), Valtournenche, Val d'Ayas
(Brusson, Champoluc) and the Col de Joux (Saint-Vincent), the Valle di Gressoney (Lys: Gressoney,
Issime, Gaby, Fontainemore, Lillianes). The central valley is one of the driest in the Alps (Aosta
about 500–600 mm a year, steppe on the south-facing adret); the side valleys toward Monte Rosa and
the Bassa Valle are wetter. Woodland is mostly larch (the region's commonest forest), spruce, Scots
pine on the dry slopes, silver fir in the cooler side valleys, mountain pine (*P. uncinata*, Mont
Avic) and stone pine near the tree line; beech, chestnut, downy and sessile oak only low in the
Bassa Valle and on warm slopes. Much woodland sits at 1,200–2,200 m, above Tuscany's fitted range:
check the altitude bands and the season windows by elevation carefully.

So *B. edulis* (spruce, larch, fir) and *B. pinophilus* (Scots pine, spruce) dominate the porcini
group; *B. aereus* and *B. reticulatus* are marginal (chestnut and oak of the Bassa Valle).
**Ovoli are probably absent**: check the evidence (herbarium and sightings records, regional
mycological literature, press) and, if it agrees, drop the ovoli group (delete
`ovoli_caesarea.yaml` for this region; the rule loader supports a region without a group) and say so
in the doc with the evidence. If ovoli do occur in the Bassa Valle chestnut and oak woods, keep the
group with the narrow bands that evidence supports, as Trentino-Alto Adige did, and say so. Do the
same for any porcini key the region lacks. The region has its own picking law (find and cite the
current one); it does not change the rules, but the local press around it is a source of season
reports.

Deliver:
- `.gavin-root/docs/species-ecology/valle_d_aosta.md`: the regional evidence (season windows, host
  trees and habitat affinities, altitude bands, weather rules where regional literature exists),
  each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Follow the shape of `species-ecology/trentino_alto_adige.md` and
  `species-ecology/piemonte.md` (the neighbour; Valle d'Aosta shares IPLA's forest typology with
  Piemonte). French-language sources count as well as Italian ones: Regione Autonoma Valle
  d'Aosta (Struttura forestazione e sentieristica, Corpo forestale), the Museo regionale di Scienze
  naturali "Efisio Noussan", the Parco Nazionale Gran Paradiso and Parco naturale Mont Avic, the
  region's mycological groups and USL mycological inspectorate, regional press (Aostasera,
  AostaOggi, Gazzetta Matin, La Stampa Aosta, Rai Valle d'Aosta, Bobine.tv, La Vallée Notizie),
  and neighbouring Savoie / Valais sources where the Valdostan ones are thin (say so when you use
  them).
- `api/src/api/config/species/valle_d_aosta/` started from `tuscany/` (look at
  `trentino_alto_adige/` and `piemonte/` first for how the Alpine regions retuned, then `lombardia/`):
  per-species YAML with season windows, habitat affinities and altitude bands retuned for the
  region; every factor cited with a confidence; groups or keys the region lacks dropped and the doc
  says so.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys
  unique; open every source you cite). Put them in their own block for this region, at the end of
  the file, so merges with other region branches stay simple.
- `valle_d_aosta/sanity.yaml`: press or blog contrasts for the region's areas (comuni) and years
  (2016–2025), written before any score exists, in the same format as the other regions'. Aim for
  10–14 contrasts across the region's valleys; name comuni exactly as ISTAT 2025 does (the grid's
  `comune_name`, e.g. "Saint-Vincent", "Gressoney-La-Trinité", "Pré-Saint-Didier",
  "Châtillon"); the province sigla is AO. A gallinacci contrast is welcome if the press has one.
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid will map the regional forest
map's categories to it roughly as Piemonte did (`api/src/api/config/regions/piemonte.yaml`):
spruce and silver fir → `fir_spruce`, larch and stone pine → `other_conifer`, Scots and mountain
pine → `mountain_pine`, beech → `beech`, chestnut → `chestnut`, oaks → `deciduous_oak`,
hop-hornbeam, ash-maple-lime, birch and aspen pioneer woods → `mixed_broadleaf`, robinia →
`exotic_broadleaf`, riparian alder and willow → `riparian`, green alder and rhododendron scrub →
`transitional_woodland_shrub` (not woodland). Check
`api/src/api/config/regions/valle_d_aosta.yaml` once it exists for the final mapping, and say in the
doc which habitat holds which tree of the region. Larch is the region's commonest forest: weigh the
evidence on porcini under larch carefully (Piemonte's doc flags larch at 0.3 as the first knob if
Alpine cells score too high).

Do not commit and do not edit any plan card.
