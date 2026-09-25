#!/usr/bin/env bash
# Extracts the self-hosted basemap (PRD → Architecture → Basemap): a Protomaps
# vector basemap and a Mapterhorn terrain (hillshade) archive.
# Output goes to the gitignored web/data/basemap/. Needs the pmtiles CLI
# (`brew install pmtiles`, or a release from github.com/protomaps/go-pmtiles).
#
#   scripts/extract-basemap.sh [BUILD_DATE] [REGION]
#     BUILD_DATE=YYYYMMDD, default: latest Protomaps build
#     REGION=italy (default) | tuscany   — filename prefix and bbox
#
# Protomaps keeps only about a week of daily builds, so the extract is pinned to
# a date and never read from build.protomaps.com at runtime.
#
# Italy (bbox 6.6,35.4,18.6,47.1) is what production serves after the multi-region
# foundation. Record the sizes below after a fresh extract and confirm they fit
# Cloudflare R2's free tier (10 GB storage).
set -euo pipefail

REGION="${2:-italy}"
case "$REGION" in
  italy)
    BBOX="6.6,35.4,18.6,47.1" # all of Italy plus a small margin
    ;;
  tuscany)
    BBOX="9.6,42.2,12.4,44.5" # Tuscany plus a margin, including the archipelago
    ;;
  *)
    echo "unknown region '$REGION' (use italy or tuscany)" >&2
    exit 2
    ;;
esac

BASEMAP_MAXZOOM=14
TERRAIN_MAXZOOM=11

cd "$(dirname "$0")/.."
OUT=data/basemap
mkdir -p "$OUT"

if [ -n "${1:-}" ]; then
  BUILD="$1"
else
  BUILD="$(curl -fsSL https://build-metadata.protomaps.dev/builds.json |
    python3 -c 'import json, sys; print(json.load(sys.stdin)[-1]["key"].removesuffix(".pmtiles"))')"
fi

echo "Protomaps build $BUILD → $OUT/$REGION.pmtiles (bbox $BBOX)"
pmtiles extract "https://build.protomaps.com/$BUILD.pmtiles" "$OUT/$REGION.pmtiles.tmp" \
  --bbox="$BBOX" --maxzoom="$BASEMAP_MAXZOOM" --download-threads=4
mv "$OUT/$REGION.pmtiles.tmp" "$OUT/$REGION.pmtiles"
echo "$BUILD" > "$OUT/$REGION.build"

echo "Mapterhorn terrain → $OUT/$REGION-terrain.pmtiles"
pmtiles extract https://download.mapterhorn.com/planet.pmtiles "$OUT/$REGION-terrain.pmtiles.tmp" \
  --bbox="$BBOX" --maxzoom="$TERRAIN_MAXZOOM" --download-threads=4
mv "$OUT/$REGION-terrain.pmtiles.tmp" "$OUT/$REGION-terrain.pmtiles"

ls -lh "$OUT/$REGION.pmtiles" "$OUT/$REGION-terrain.pmtiles"
echo "Sizes (bytes):"
wc -c "$OUT/$REGION.pmtiles" "$OUT/$REGION-terrain.pmtiles"
