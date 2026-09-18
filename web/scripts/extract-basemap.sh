#!/usr/bin/env bash
# Extracts the self-hosted basemap for the region (PRD → Architecture → Basemap):
# a Protomaps vector basemap and a Mapterhorn terrain (hillshade) archive.
# Output goes to the gitignored web/data/basemap/. Needs the pmtiles CLI
# (`brew install pmtiles`, or a release from github.com/protomaps/go-pmtiles).
#
#   scripts/extract-basemap.sh [BUILD_DATE]    # BUILD_DATE=YYYYMMDD, default: latest build
#
# Protomaps keeps only about a week of daily builds, so the extract is pinned to
# a date and never read from build.protomaps.com at runtime.
set -euo pipefail

BBOX="9.6,42.2,12.4,44.5" # Tuscany plus a margin, including the archipelago
BASEMAP_MAXZOOM=14        # ~190 MB; MapLibre overzooms beyond
TERRAIN_MAXZOOM=11        # ~33 MB; ~28 m/px, plenty for hillshade

cd "$(dirname "$0")/.."
OUT=data/basemap
mkdir -p "$OUT"

BUILD="${1:-$(curl -fsSL https://build-metadata.protomaps.dev/builds.json |
  python3 -c 'import json, sys; print(json.load(sys.stdin)[-1]["key"].removesuffix(".pmtiles"))')}"

echo "Protomaps build $BUILD → $OUT/tuscany.pmtiles"
pmtiles extract "https://build.protomaps.com/$BUILD.pmtiles" "$OUT/tuscany.pmtiles.tmp" \
  --bbox="$BBOX" --maxzoom="$BASEMAP_MAXZOOM" --download-threads=4
mv "$OUT/tuscany.pmtiles.tmp" "$OUT/tuscany.pmtiles"
echo "$BUILD" > "$OUT/tuscany.build"

echo "Mapterhorn terrain → $OUT/tuscany-terrain.pmtiles"
pmtiles extract https://download.mapterhorn.com/planet.pmtiles "$OUT/tuscany-terrain.pmtiles.tmp" \
  --bbox="$BBOX" --maxzoom="$TERRAIN_MAXZOOM" --download-threads=4
mv "$OUT/tuscany-terrain.pmtiles.tmp" "$OUT/tuscany-terrain.pmtiles"

ls -lh "$OUT"
