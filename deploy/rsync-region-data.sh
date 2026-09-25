#!/usr/bin/env bash
# Rsync one region's pipeline stores to the production data volume, then optionally redeploy.
#
#   deploy/rsync-region-data.sh <region> [--redeploy] [--skip-tests] [--run-job]
#
# Copies grid, weather, scores, sightings, climatology, history and outlook for <region> into
# /srv/mushma-data on the server (same layout as a local $DATA_DIR). Skips bulky raw/ caches.
# With --redeploy, runs deploy/deploy-api.sh afterwards so the API picks up the new region.
#
# DEPLOY_HOST (default root@api.mappafunghi.app) points it somewhere else. The gavin tool
# "Rsync region data" runs this script.
set -euo pipefail

DEPLOY_HOST="${DEPLOY_HOST:-root@api.mappafunghi.app}"
REMOTE_DATA="${REMOTE_DATA:-/srv/mushma-data}"
REDEPLOY=0
DEPLOY_ARGS=()

usage() { sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; }

REGION=""
for arg in "$@"; do
  case "$arg" in
    --redeploy) REDEPLOY=1 ;;
    --skip-tests) DEPLOY_ARGS+=(--skip-tests) ;;
    --run-job) DEPLOY_ARGS+=(--run-job) ;;
    -h | --help) usage; exit 0 ;;
    -*)
      echo "unknown option: $arg" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [ -z "$REGION" ]; then REGION="$arg"
      else echo "unexpected argument: $arg" >&2; usage >&2; exit 2
      fi
      ;;
  esac
done

[ -n "$REGION" ] || { echo "usage: $0 <region> [--redeploy] [--skip-tests] [--run-job]" >&2; exit 2; }

say() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
die() { printf '\033[31mxx  %s\033[0m\n' "$*" >&2; exit 1; }

for cmd in git rsync ssh; do
  command -v "$cmd" >/dev/null 2>&1 || die "'$cmd' is not installed"
done

cd "$(dirname "$0")/.."
DATA_DIR="${DATA_DIR:-api/data}"
case "$DATA_DIR" in /*) ;; *) DATA_DIR="$PWD/$DATA_DIR" ;; esac

[ -d "$DATA_DIR/grid/$REGION" ] || die "no grid for $REGION under $DATA_DIR/grid/$REGION (run onboard first)"

say "Rsync $REGION from $DATA_DIR -> $DEPLOY_HOST:$REMOTE_DATA"
paths=()
for tree in grid weather scores sightings climatology history outlook; do
  if [ -d "$DATA_DIR/$tree/$REGION" ]; then
    paths+=("$tree/$REGION")
  fi
done
[ "${#paths[@]}" -gt 0 ] || die "no store trees for $REGION under $DATA_DIR"
# -L: follow symlinks (worktrees may share a data root). -R with paths relative to $DATA_DIR keeps
# the grid/<region>/… layout. Short flags, --stats and no "/./" anchor: macOS ships openrsync,
# which lacks --info and --relative and ignores the anchor.
(cd "$DATA_DIR" && rsync -azLR --stats "${paths[@]}" "$DEPLOY_HOST:$REMOTE_DATA/")

say "Synced $REGION"
if [ "$REDEPLOY" = 1 ]; then
  say "Redeploying API"
  exec bash deploy/deploy-api.sh ${DEPLOY_ARGS[@]+"${DEPLOY_ARGS[@]}"}
fi
