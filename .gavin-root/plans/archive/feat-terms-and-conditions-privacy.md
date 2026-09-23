---
order: 4096
kind: plan
title: [feat] Terms and conditions + privacy
status: Done
complexity: moderate
---
Terms, privacy policy and a cookie banner for the app, formal GDPR/Italian-law-referencing
copy (Italian first, English kept complete). Controller contact: `contact@cosimoalfredopinalari.me`.
The cookie banner gates the self-hosted Umami analytics that `feat-umami-integration.md` builds
and deploys, with a real Accept/Decline, not just a notice.

- [x] Privacy Policy content (`privacy.*` i18n keys): GDPR-referencing (Art. 6/13/15–22), controller
      contact `contact@cosimoalfredopinalari.me`, covers what's actually collected — IP for the
      API's rate limiter, optional browser geolocation (kept in memory only, never persisted),
      localStorage (language, disclaimer flag, cookie-consent flag), self-hosted Umami (describe
      its real IP/cookie handling — check Umami's docs, don't assume; list the tracked events,
      and say that no URL query string or location is ever sent — see
      `feat-umami-integration.md`), subprocessors (Vercel,
      Cloudflare, Hetzner, self-hosted Umami), retention, international-transfer note, right to
      complain to the Garante, cross-links to the existing Disclaimer for sightings-privacy
      framing (PRD → Sightings privacy: counts only, never coordinates).
- [x] Terms & Conditions content (`terms.*` i18n keys): GDPR/Italian-consumer-law-referencing,
      service description, "conditions score is an index, not a guarantee" (PRD → Model → Score
      semantics), the clause that responsibility for how the score/data is used and interpreted
      rests with the user, links to (doesn't duplicate) the existing Disclaimer, liability
      limitation, governing law Italy, changes-to-terms clause, link to the Privacy Policy.
- [x] `web/src/pages/TermsPage.tsx` + `PrivacyPage.tsx`, mirroring `CreditsPage.tsx`'s
      structure/back-link/CSS module.
- [x] Wire `/terms` and `/privacy` into `App.tsx`'s path switch (next to the existing `/credits`
      branch at `App.tsx:500`) and add both links to the footer's links row (`App.tsx:482-495`).
- [x] Cookie banner (`web/src/components/CookieBanner.tsx`, new `cookies.*` i18n keys):
      Accept/Decline, shown once until answered, reopenable later from the footer (like the
      Disclaimer reopen button) so the choice can be changed, links to the Privacy Policy. The
      choice lives in a new `web/src/consent.ts`: `getConsent()` / `setConsent()` /
      `onConsentChange()`, persisted as `mushma.cookieConsent.v1` (`accepted`/`declined`) in
      localStorage with the same try/catch pattern as `disclaimerAccepted()` in
      `DisclaimerDialog.tsx`, plus a same-tab change event. `feat-umami-integration.md` gates its
      loader on this contract.
- [x] Locale parity (`locales.test.ts`/`keys.ts`) passes for the new `terms`/`privacy`/`cookies`
      keys in both `en.json` and `it.json`.
- [x] Light tests for `CookieBanner` (accept/decline persists across reload, doesn't reappear,
      reopenable from the footer) and `consent.ts` (the change event fires on set).

Umami itself is `feat-umami-integration.md`, end to end: the server instance, the consent-gated
loader, its env vars and events. It depends on this card's `web/src/consent.ts`, so the cookie
banner item lands first.

<!-- gavin:auto-commit -->
When the implementation is done, commit it. Commit only the files you touched — never `git add -A`. Do not push.
<!-- /gavin:auto-commit -->
