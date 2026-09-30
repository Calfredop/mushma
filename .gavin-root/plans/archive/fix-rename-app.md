---
status: Done
complexity: simple
kind: task
title: [fix] rename app
parent: eat-seo.md
---
Rename app in frontend, from mushma to Mappa Funghi (same as domain)

Change every user-visible brand string to **Mappa Funghi**:
- `web/src/i18n/locales/it.json` and `en.json`: `app.name`, `app.documentTitle`, and
  every other string that says "mushma" (install banner, outside-region message,
  disclaimer, credits intro — `grep -n mushma` finds them all);
- `<title>` in `web/index.html`;
- the PWA manifest `name` and `short_name` in `web/vite.config.ts`.

Do NOT rename internal identifiers: localStorage keys (`mushma.*`; renaming them resets
every visitor's language, accepted disclaimer and dismissed banners), Workbox cache
names, `performance.mark` names, Vite plugin names, the repo, packages or the API.

Update any unit or e2e test that asserts the old name. Run `pnpm test`, `lint`,
`format:check` and `build` in `web/`.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
