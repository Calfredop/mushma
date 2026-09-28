---
kind: task
title: [region] Trentino-Alto Adige — species research and rules
parent: region-trentino-alto-adige.md
complexity: complex
---
Species research for Trentino-Alto Adige (child of `region-trentino-alto-adige.md`). Work in the region's
checkout (`/Users/coalpila/CloudStation/Coding/mushma-regions-3`, branch `region/trentino-alto-adige`).
API id `trentino_alto_adige`, ISTAT COD_REG 4, names "Trentino-Alto Adige" / en "Trentino-South Tyrol".
Two autonomous provinces: Trento (Val di Fiemme, Val di Fassa, Primiero, Valsugana, Tesino, Val di
Sole, Val di Non, Giudicarie, Rendena, Altopiano di Piné, Lagorai, Paganella, Monte Bondone, Alto
Garda trentino, Vallagarina) and Bolzano / Südtirol (Val Pusteria/Pustertal, Val Venosta/Vinschgau,
Val Passiria, Val d'Ultimo, Val Sarentino, Renon/Ritten, Val Gardena, Val Badia, Bassa Atesina/
Unterland, Oltradige/Überetsch). Mostly montane and subalpine: spruce, larch, stone pine, silver fir,
Scots pine (dry inner valleys: Venosta, Isarco), beech and mixed beech-fir in southern Trentino,
chestnut and hop-hornbeam/oak only low on the Adige, Sarca and Valsugana slopes. So *B. edulis* and
*B. pinophilus* dominate the porcini group; *B. aereus* and ovoli are marginal or absent (check the
evidence, and drop what the region lacks and say so). Bolzano has a strict collecting law (quantity
limits and odd/even-day rules, L.P. 3/1991 and later) and Trento its own (L.P. 11/2007 and
regolamento); neither changes the rules, but the local press around them is a source of season
reports.

Deliver:
- `.gavin-root/docs/species-ecology/trentino_alto_adige.md`: the regional evidence (season windows,
  host trees and habitat affinities, altitude bands, weather rules where regional literature exists),
  each claim cited, with a confidence (`strong` / `plausible` / `folklore`, as in
  `species-ecology.md`). Follow the shape of `species-ecology/piemonte.md` (the closest Alpine analogue).
  German-language sources for South Tyrol count (Pilzkundliche Arbeitsgemeinschaft, Naturmuseum
  Südtirol, Amt für Forstverwaltung, Dolomiten / Stol.it / Salto press) as well as Italian ones
  (Gruppo Micologico Bresadola — founded in Trento —, Museo delle Scienze MUSE, Servizio Foreste
  Provincia di Trento, l'Adige, Il Dolomiti, Trentino, Alto Adige newspapers).
- `api/src/api/config/species/trentino_alto_adige/` started from `tuscany/` (look at `piemonte/` first
  for how an Alpine region retuned, then `emilia_romagna/`, `liguria/`, `marche/`, `umbria/`):
  per-species YAML with season windows, habitat affinities and altitude bands retuned for the
  region; every factor cited with a confidence; groups or keys the region lacks dropped and the doc
  says so. Much woodland sits at 1,000–2,000 m, above Tuscany's fitted range: check the altitude
  bands and the season windows by elevation carefully.
- Regional references added to the shared `api/src/api/config/species/references.yaml` (keys unique;
  open every source you cite). Put them in their own block for this region so merges with other
  region branches stay simple.
- `trentino_alto_adige/sanity.yaml`: press or blog contrasts for the region's areas (comuni) and years
  (2016-2025), written before any score exists, in the same format as the other regions'. Aim for
  12-16 contrasts across both provinces; name comuni that exist in ISTAT 2025 (Italian names, the
  ISTAT form for bilingual South Tyrolean comuni, e.g. "Brunico", "Malles Venosta").
- `uv run pytest tests/model/test_rules.py tests/model/test_config.py` passes; `uv run ruff check .`
  clean (from `api/`).

The habitat vocabulary is `api/src/api/config/habitats.yaml`. The grid will map the provinces' forest
types to it roughly as Piemonte did: spruce and silver fir → `fir_spruce`, larch and stone pine →
`other_conifer`, Scots, black and mountain pine → `mountain_pine`, beech → `beech`, chestnut →
`chestnut`, oaks → `deciduous_oak`, hop-hornbeam, ash-maple, birch, green alder scrub excluded →
`mixed_broadleaf`, robinia → `exotic_broadleaf`, riparian alder/willow → `riparian`. Check
`api/src/api/config/regions/trentino_alto_adige.yaml` once it exists for the final mapping, and say in
the doc which habitat holds which tree of the region.

Do not commit and do not edit any plan card.
