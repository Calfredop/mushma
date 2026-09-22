---
order: 4096
kind: plan
title: [feat] Terms and conditions + privacy
status: To Do
complexity: moderate
---
Terms, privacy policy and a cookie banner for the app, formal GDPR/Italian-law-referencing
copy (Italian first, English kept complete). Controller contact: `contact@cosimoalfredopinalari.me`.
The cookie banner gates a self-hosted Umami analytics script (not yet deployed — see the nested
child card) with a real Accept/Decline, not just a notice.

- [ ] Privacy Policy content (`privacy.*` i18n keys): GDPR-referencing (Art. 6/13/15–22), controller
      contact `contact@cosimoalfredopinalari.me`, covers what's actually collected — IP for the
      API's rate limiter, optional browser geolocation (kept in memory only, never persisted),
      localStorage (language, disclaimer flag, cookie-consent flag), self-hosted Umami (describe
      its real IP/cookie handling — check Umami's docs, don't assume), subprocessors (Vercel,
      Cloudflare, Hetzner, self-hosted Umami), retention, international-transfer note, right to
      complain to the Garante, cross-links to the existing Disclaimer for sightings-privacy
      framing (PRD → Sightings privacy: counts only, never coordinates).
- [ ] Terms & Conditions content (`terms.*` i18n keys): GDPR/Italian-consumer-law-referencing,
      service description, "conditions score is an index, not a guarantee" (PRD → Model → Score
      semantics), the clause that responsibility for how the score/data is used and interpreted
      rests with the user, links to (doesn't duplicate) the existing Disclaimer, liability
      limitation, governing law Italy, changes-to-terms clause, link to the Privacy Policy.
- [ ] `web/src/pages/TermsPage.tsx` + `PrivacyPage.tsx`, mirroring `CreditsPage.tsx`'s
      structure/back-link/CSS module.
- [ ] Wire `/terms` and `/privacy` into `App.tsx`'s path switch (next to the existing `/credits`
      branch at `App.tsx:500`) and add both links to the footer's links row (`App.tsx:482-495`).
- [ ] Cookie banner (`web/src/components/CookieBanner.tsx`, new `cookies.*` i18n keys):
      Accept/Decline, shown once until answered, persisted as `mushma.cookieConsent.v1` in
      localStorage (same accepted/declined + try/catch pattern as `disclaimerAccepted()` in
      `DisclaimerDialog.tsx`), links to the Privacy Policy, reopenable later from the footer (like
      the Disclaimer reopen button) so the choice can be changed.
- [ ] Locale parity (`locales.test.ts`/`keys.ts`) passes for the new `terms`/`privacy`/`cookies`
      keys in both `en.json` and `it.json`.
- [ ] Light tests for `CookieBanner` (accept/decline persists across reload, doesn't reappear,
      reopenable from the footer).

Wiring the actual Umami tracking script into the frontend (env vars, consent-gated injection) is
split out into its own card, `feat-umami-integration.md` — it depends on this card's cookie-consent
flag and on the nested `feat-terms-privacy-self-host-umami.md` for a real Umami instance.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
