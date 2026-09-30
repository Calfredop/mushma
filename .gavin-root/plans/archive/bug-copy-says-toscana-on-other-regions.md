---
kind: task
title: [bug] panels and area picker say Toscana on every region
status: Done
priority: medium
complexity: simple
---
Several i18n strings still hard-code Tuscany, so they read wrong on /piemonte, /marche, etc. (found while fixing the map label, commit 6f1f376):

Visible in the region UI:
- `app.region` ("Toscana" / "Tuscany"), used as the whole-region area name in `web/src/panels/OutlookPanel.tsx` and `web/src/panels/SeasonsPanel.tsx`.
- `area.region` ("Tutta la Toscana" / "All of Tuscany"), the whole-region option in `web/src/components/AreaPicker.tsx`.

Site-wide copy that predates the other regions:
- `terms.sections.service.body` says the service covers "porcini, ovoli e gallinacci in Toscana".
- `seo.credits.description` says conditions "in Toscana".

Make the region strings take the active region's name (the map label now does it with `{{where}}` and `regionLocative`; "Tutta la …" needs the article too, so check Marche → "Tutte le Marche"), reword the site-wide copy for multi-region, keep it/en complete, and add light tests.
