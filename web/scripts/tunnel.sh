#!/usr/bin/env bash
# Serves the local dev stack through a cloudflared quick tunnel, so a phone or
# a friend can reach it from outside. Starts the Vite dev server and the tunnel
# together; Ctrl-C stops both. Needs cloudflared (`brew install cloudflared`).
#
#   pnpm run tunnel                  # or: scripts/tunnel.sh
#   PORT=5174 API_PORT=8001 scripts/tunnel.sh
#
# One tunnel carries the whole stack. Vite proxies /api to the local API
# (vite.config.ts), so the app and the API share the tunnel's single origin:
# no second hostname, no CORS. VITE_API_BASE_URL is forced to /api here because
# a local .env may point it at http://localhost:8000, which is not reachable
# from outside; a real env var outranks .env, so the file is left alone.
#
# The URL is public for as long as the tunnel runs, and is a fresh one every
# run. Anyone holding it reaches this machine's dev API and whatever sits in
# api/data/, so don't leave it up unattended.
set -euo pipefail

PORT="${PORT:-5173}"
API_PORT="${API_PORT:-8000}"
STARTUP_TIMEOUT=60 # seconds to wait for Vite, and again for the tunnel URL

cd "$(dirname "$0")/.."

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "tunnel: cloudflared is not installed. brew install cloudflared" >&2
  exit 1
fi

# A refused connection exits 7; any HTTP reply, 404 included, means something is listening.
port_open() { curl -fsS -o /dev/null -m 2 "http://127.0.0.1:$1" 2>/dev/null || [ $? -ne 7 ]; }

wait_for_port() {
  for _ in $(seq "$STARTUP_TIMEOUT"); do
    port_open "$1" && return 0
    sleep 1
  done
  return 1
}

if ! port_open "$API_PORT"; then
  echo "tunnel: warning — nothing is listening on :$API_PORT, so /api will fail."
  echo "        start it with: cd ../api && uv run fastapi dev src/api/main.py"
fi

LOG="$(mktemp -t mushma-tunnel)"
VITE_PID=""
TUNNEL_PID=""

cleanup() {
  [ -n "$TUNNEL_PID" ] && kill "$TUNNEL_PID" 2>/dev/null || true
  [ -n "$VITE_PID" ] && kill "$VITE_PID" 2>/dev/null || true
  rm -f "$LOG"
}
trap cleanup EXIT INT TERM

echo "tunnel: starting the dev server on :$PORT"
TUNNEL=1 VITE_API_BASE_URL=/api pnpm exec vite --port "$PORT" --strictPort &
VITE_PID=$!

if ! wait_for_port "$PORT"; then
  echo "tunnel: the dev server never came up on :$PORT" >&2
  exit 1
fi

echo "tunnel: opening the cloudflared quick tunnel"
cloudflared tunnel --url "http://localhost:$PORT" >"$LOG" 2>&1 &
TUNNEL_PID=$!

URL=""
for _ in $(seq "$STARTUP_TIMEOUT"); do
  URL="$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$LOG" | head -1 || true)"
  [ -n "$URL" ] && break
  kill -0 "$TUNNEL_PID" 2>/dev/null || break
  sleep 1
done

if [ -z "$URL" ]; then
  echo "tunnel: cloudflared did not report a URL. Its output:" >&2
  cat "$LOG" >&2
  exit 1
fi

RULE="$(printf '%*s' "$((${#URL} + 2))" '' | tr ' ' '-')"
cat <<BANNER

  +$RULE+
  | $URL |
  +$RULE+

  The app and its API are both on that origin. It is public while this runs,
  and a different URL next time. Ctrl-C stops the tunnel and the dev server.

BANNER

command -v qrencode >/dev/null 2>&1 && qrencode -t ANSIUTF8 "$URL"

wait "$VITE_PID"
