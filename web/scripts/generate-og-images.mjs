// Generates the 1200×630 link-preview (Open Graph / Twitter card) image for the region page and
// each species page. `/credits` reuses the region page's image (src/seo/prerender.ts). Playwright
// renders real HTML/CSS with the app's own fonts, so the card matches the brand exactly; a plain
// SVG can't do that portably since Young Serif and Atkinson Hyperlegible aren't system fonts.
//
// Run manually when the brand or copy changes, and commit the PNGs:
//
//   node scripts/generate-og-images.mjs
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { chromium } from '@playwright/test'

const ROOT = resolve(import.meta.dirname, '..')
const OUT_DIR = resolve(ROOT, 'public/og')

function fontDataUri(path) {
  return `data:font/woff2;base64,${readFileSync(resolve(ROOT, path)).toString('base64')}`
}

const YOUNG_SERIF = fontDataUri(
  'node_modules/@fontsource/young-serif/files/young-serif-latin-400-normal.woff2',
)
const ATKINSON = fontDataUri(
  'node_modules/@fontsource-variable/atkinson-hyperlegible-next/files/atkinson-hyperlegible-next-latin-wght-normal.woff2',
)
const MARK_SVG = readFileSync(resolve(ROOT, 'public/favicon.svg'), 'utf8')

// Matches region registry SEO titles (Italian: the indexed language) plus the hub.
const CARDS = [
  { name: 'hub', title: 'Condizioni per i funghi in Italia' },
  { name: 'toscana', title: 'Porcini, ovoli e gallinacci in Toscana' },
  { name: 'toscana-porcini', title: 'Porcini in Toscana' },
  { name: 'toscana-ovoli', title: 'Ovoli in Toscana' },
  { name: 'toscana-gallinacci', title: 'Gallinacci in Toscana' },
  { name: 'umbria', title: 'Porcini, ovoli e gallinacci in Umbria' },
  { name: 'umbria-porcini', title: 'Porcini in Umbria' },
  { name: 'umbria-ovoli', title: 'Ovoli in Umbria' },
  { name: 'umbria-gallinacci', title: 'Gallinacci in Umbria' },
  { name: 'emilia-romagna', title: 'Porcini, ovoli e gallinacci in Emilia-Romagna' },
  { name: 'emilia-romagna-porcini', title: 'Porcini in Emilia-Romagna' },
  { name: 'emilia-romagna-ovoli', title: 'Ovoli in Emilia-Romagna' },
  { name: 'emilia-romagna-gallinacci', title: 'Gallinacci in Emilia-Romagna' },
]

function cardHtml(title) {
  return `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
  @font-face {
    font-family: 'Young Serif';
    src: url('${YOUNG_SERIF}') format('woff2');
  }
  @font-face {
    font-family: 'Atkinson Hyperlegible Next Variable';
    src: url('${ATKINSON}') format('woff2');
    font-weight: 100 800;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 1200px; height: 630px; }
  body {
    position: relative;
    overflow: hidden;
    background: #EDF0EA;
    font-family: 'Atkinson Hyperlegible Next Variable', sans-serif;
  }
  .hatch {
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
      -45deg, rgba(28, 33, 29, 0.05) 0 1.5px, transparent 1.5px 9px
    );
  }
  .content {
    position: relative;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 96px;
  }
  .mark { width: 108px; height: 108px; margin-bottom: 36px; }
  .mark svg { display: block; width: 100%; height: 100%; }
  .wordmark {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5B675E;
    margin-bottom: 22px;
  }
  h1 {
    font-family: 'Young Serif', serif;
    font-weight: 400;
    font-size: 64px;
    line-height: 1.18;
    color: #1C211D;
    max-width: 900px;
  }
  .sub {
    margin-top: 26px;
    font-size: 26px;
    color: #5B675E;
  }
</style>
</head>
<body>
  <div class="hatch"></div>
  <div class="content">
    <div class="mark">${MARK_SVG}</div>
    <div class="wordmark">Mappa Funghi</div>
    <h1>${title}</h1>
    <div class="sub">Indice delle condizioni, cella per cella</div>
  </div>
</body>
</html>`
}

mkdirSync(OUT_DIR, { recursive: true })

const browser = await chromium.launch()
try {
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } })
  for (const { name, title } of CARDS) {
    await page.setContent(cardHtml(title), { waitUntil: 'load' })
    await page.evaluate(() => document.fonts.ready)
    const outFile = resolve(OUT_DIR, `${name}.png`)
    await page.screenshot({ path: outFile })
    console.log(`wrote public/og/${name}.png`)
  }
} finally {
  await browser.close()
}
