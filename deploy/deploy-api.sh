#!/usr/bin/env bash
# Ships api/ and deploy/ to the production server (README.md -> Deploying).
#
#   deploy/deploy-api.sh [--skip-tests] [--run-job]
#
# The server builds from GitHub, not from this checkout, so only a main that is already pushed can
# be deployed. Then: API lint and tests here; on the server, pull, install the daily job's systemd
# units if they changed, rebuild and restart the API behind Caddy, prune old images. It waits for
# /health, smoke-tests the main routes and prints /status. --run-job also runs the daily pipeline
# straight away (about two minutes) instead of waiting for 05:00 Europe/Rome.
#
# DEPLOY_HOST (default root@api.mappafunghi.app) and API_URL (default https://api.mappafunghi.app)
# point it somewhere else. The gavin tool "Deploy API" runs this script.
set -euo pipefail

DEPLOY_HOST="${DEPLOY_HOST:-root@api.mappafunghi.app}"
API_URL="${API_URL:-https://api.mappafunghi.app}"
TESTS=1
RUN_JOB=0

usage() { sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; }
for arg in "$@"; do
  case "$arg" in
    --skip-tests) TESTS=0 ;;
    --run-job) RUN_JOB=1 ;;
    -h | --help) usage; exit 0 ;;
    *) echo "unknown option: $arg" >&2; usage >&2; exit 2 ;;
  esac
done

say() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[33m!!  %s\033[0m\n' "$*" >&2; }
die() { printf '\033[31mxx  %s\033[0m\n' "$*" >&2; exit 1; }

for cmd in git ssh curl uv; do
  command -v "$cmd" >/dev/null 2>&1 || die "'$cmd' is not installed"
done

cd "$(dirname "$0")/.."

# --- 1. What gets deployed: the pushed main ------------------------------------------------------
branch="$(git rev-parse --abbrev-ref HEAD)"
[ "$branch" = main ] || die "on '$branch': deploy from main, the branch the server pulls"
[ -z "$(git status --porcelain -- api deploy)" ] ||
  die "uncommitted changes under api/ or deploy/: commit and push them first"
git fetch -q origin main
sha="$(git rev-parse HEAD)"
[ "$sha" = "$(git rev-parse origin/main)" ] ||
  die "main ($(git rev-parse --short HEAD)) is not origin/main ($(git rev-parse --short origin/main)): push or pull first"
say "Deploying $(git log -1 --format='%h %s')"

# --- 2. Checks on the code the server is about to build ------------------------------------------
if [ "$TESTS" = 1 ]; then
  say "API checks: ruff and pytest"
  (cd api && uv run ruff check . && uv run ruff format --check . && uv run pytest -q) ||
    die "the API checks failed: nothing was deployed"
else
  warn "--skip-tests: deploying without running the API checks"
fi

# --- 3. The server: pull, units, rebuild ---------------------------------------------------------
say "Server $DEPLOY_HOST"
# shellcheck disable=SC2087 # the heredoc is quoted: everything in it runs on the server
ssh -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new "$DEPLOY_HOST" \
  bash -s -- "$sha" "$RUN_JOB" <<'REMOTE'
set -euo pipefail
want="$1"
run_job="$2"

cd /opt/mushma
git fetch -q origin main
git merge -q --ff-only origin/main
[ "$(git rev-parse HEAD)" = "$want" ] || { echo "the server checked out $(git rev-parse --short HEAD), not $want" >&2; exit 1; }

units_changed=0
for unit in mushma-daily.service mushma-daily.timer; do
  if ! cmp -s "deploy/$unit" "/etc/systemd/system/$unit"; then
    cp "deploy/$unit" /etc/systemd/system/
    echo "installed the new $unit"
    units_changed=1
  fi
done
if [ "$units_changed" = 1 ]; then
  systemctl daemon-reload
  systemctl enable mushma-daily.timer >/dev/null 2>&1
  systemctl restart mushma-daily.timer
fi

cd deploy
docker compose up -d --build --remove-orphans
docker image prune -f >/dev/null

if [ "$run_job" = 1 ]; then
  echo "running the daily job now"
  since="$(date '+%F %T')"
  if ! systemctl start mushma-daily.service; then
    journalctl -u mushma-daily --since "$since" -o cat --no-pager | tail -30
    exit 1
  fi
  journalctl -u mushma-daily --since "$since" -o cat --no-pager | grep '"event"' | tail -14
fi

systemctl list-timers mushma-daily.timer --no-pager | sed -n 2p
REMOTE

# --- 4. Is it serving? ---------------------------------------------------------------------------
say "Waiting for $API_URL/health"
tries=30
until curl -fsS -m 5 -o /dev/null "$API_URL/health" 2>/dev/null; do
  tries=$((tries - 1))
  [ "$tries" -gt 0 ] || die "$API_URL/health did not answer after the restart"
  sleep 2
done

say "Smoke test"
today="$(TZ=Europe/Rome date +%F)"
failed=0
for route in "status" "scores?species=combined&date=$today" "spot?lat=43.27&lon=11.12&date=$today" \
  "hotspots?species=porcini&date=$today" "outlook?species=porcini"; do
  code="$(curl -s -o /dev/null -m 30 -w '%{http_code}' "$API_URL/$route")" || code=000
  if [ "$code" = 200 ]; then printf '  ok   %s  /%s\n' "$code" "$route"; else printf '  FAIL %s  /%s\n' "$code" "$route"; failed=1; fi
done

status="$(curl -fsS -m 10 "$API_URL/status")"
printf '\n%s\n' "$status"
stored_rules="$(printf '%s' "$status" | sed -n 's/.*"rules_version":"\([^"]*\)".*/\1/p')"
code_rules="$(cd api && uv run python -c 'from api.model.pipeline import rules_version; print(rules_version())' 2>/dev/null || true)"
if [ -n "$code_rules" ] && [ -n "$stored_rules" ] && [ "$code_rules" != "$stored_rules" ]; then
  warn "the served scores were written with rules $stored_rules, the deployed code has $code_rules: rerun with --run-job to re-score now, or wait for the 05:00 run"
fi

[ "$failed" = 0 ] || die "deployed $(git rev-parse --short HEAD), but some routes failed (see above)"
say "Deployed $(git rev-parse --short HEAD) to $API_URL"
