---
title: Dev tunnel: reach the local stack from outside
status: Done
priority: medium
complexity: simple
---
## Why

Reach the local dev stack from a phone or a friend's machine — checking the
map and the sidebar on a real device, showing work in progress without
deploying.

## Approach (agreed with the human)

`cd web && pnpm run tunnel` starts the Vite dev server **and** a cloudflared
quick tunnel, prints the public URL, and one Ctrl-C kills both. One tunnel,
one origin: `web/vite.config.ts` already proxies `/api` to
`http://localhost:8000`, so the API rides along and no CORS config changes.

Decisions: cloudflared quick tunnel (no account, random URL per run), web port
only, no auth in front of it.

Three things had to be solved:

- Vite rejects a request whose `Host` is not localhost, so tunnel mode sets
  `server.allowedHosts = ['.trycloudflare.com']` — a subdomain wildcard, so the
  random hostname needs no feeding back in.
- `web/.env` sets `VITE_API_BASE_URL=http://localhost:8000`, which bypasses the
  proxy and is unreachable from outside. The script exports
  `VITE_API_BASE_URL=/api`; real env vars outrank `.env` in Vite, so the file
  stays as it is.
- HMR over the tunnel needs `wss` on 443, otherwise the page loads and live
  reload silently stops.

Not done: named tunnel with a stable hostname, basic auth, exposing the API on
its own URL. All are later upgrades to the same script.

## Checklist

- [x] Tunnel mode in `web/vite.config.ts`, guarded by a `TUNNEL` env var so
      plain `pnpm dev` is untouched: `allowedHosts`, `host`, `hmr`
- [x] `web/scripts/tunnel.sh`: check for `cloudflared`, warn if the API is not
      listening on 8000, start Vite, wait for the port, start cloudflared,
      parse and print the URL, QR code when `qrencode` is present, trap EXIT so
      neither process is orphaned
- [x] `"tunnel"` script in `web/package.json`
- [x] Document it in `README.md` under `## web/`, with the "public while it
      runs" warning
- [x] Note the tunnel override in `web/.env.example`
- [x] Verify end to end: run it, load the printed URL, confirm the map renders
      and `/api` calls succeed through the proxy
- [x] `cd web && pnpm run lint && pnpm run format:check`
