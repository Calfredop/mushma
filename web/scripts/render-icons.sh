#!/usr/bin/env bash
# Renders the PWA and home-screen icons in public/icons/ from public/favicon.svg, the one
# source of the app icon. Rerun it after editing the SVG and commit the PNGs. Needs
# rsvg-convert and ImageMagick 7 (`brew install librsvg imagemagick`).
#
#   scripts/render-icons.sh
#
# The "any" icons keep the SVG's rounded tile with transparent corners. The full-bleed ones set
# the tile on a square of the same Lichene, so its corners disappear: iOS masks the apple-touch
# icon itself (and would fill transparency with black), and a maskable icon has to keep the
# mushroom inside the central 80% circle that every launcher mask leaves visible.
set -euo pipefail

cd "$(dirname "$0")/.."
SRC=public/favicon.svg
OUT=public/icons
PAPER='#EDF0EA' # Lichene, the manifest's background_color

any() { # size
  rsvg-convert -w "$1" -h "$1" "$SRC" -o "$OUT/icon-$1.png"
}

full_bleed() { # size, tile scale in percent, file name
  local inner=$(($1 * $2 / 100))
  rsvg-convert -w "$inner" -h "$inner" "$SRC" |
    magick -size "$1x$1" "xc:$PAPER" - -gravity center -composite -alpha off -strip \
      -define png:exclude-chunks=date,time "$OUT/$3"
}

any 192
any 512
full_bleed 180 100 apple-touch-icon.png
full_bleed 192 80 icon-maskable-192.png
full_bleed 512 80 icon-maskable-512.png
echo "Rendered $OUT/ from $SRC"
