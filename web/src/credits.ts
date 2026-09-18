/**
 * Data sources and software credited in the app (AGENTS.md → External APIs;
 * PRD → Constraints → Licensing). Names, URLs and licence identifiers are
 * proper nouns; what each one is used for is translated.
 */
import type en from './i18n/locales/en.json'

export interface Credit {
  name: string
  url: string
  use: keyof (typeof en)['credits']['use']
  license: string
}

export const DATA_CREDITS: Credit[] = [
  {
    name: 'Open-Meteo',
    url: 'https://open-meteo.com',
    use: 'weather',
    license: 'CC BY 4.0',
  },
  {
    name: 'GBIF',
    url: 'https://www.gbif.org',
    use: 'sightings',
    license: 'CC0 1.0 / CC BY 4.0 / CC BY-NC 4.0',
  },
  {
    name: 'iNaturalist',
    url: 'https://www.inaturalist.org',
    use: 'inaturalist',
    license: 'CC BY-NC 4.0',
  },
  {
    name: 'Copernicus Land Monitoring Service',
    url: 'https://land.copernicus.eu',
    use: 'landcover',
    license: 'Regulation (EU) 1159/2013',
  },
  {
    name: 'TINITALY (INGV), Mapterhorn',
    url: 'https://mapterhorn.com/attribution',
    use: 'elevation',
    license: 'CC BY 4.0',
  },
  { name: 'ISTAT', url: 'https://www.istat.it', use: 'boundaries', license: 'CC BY 4.0' },
  {
    name: 'ECMWF (EC46, SEAS5) via Open-Meteo',
    url: 'https://open-meteo.com/en/docs/seasonal-forecast-api',
    use: 'seasonal',
    license: 'CC BY 4.0',
  },
]

export const SOFTWARE_CREDITS: Credit[] = [
  {
    name: 'OpenStreetMap',
    url: 'https://www.openstreetmap.org/copyright',
    use: 'basemapData',
    license: 'ODbL 1.0',
  },
  {
    name: 'Protomaps',
    url: 'https://protomaps.com',
    use: 'basemapTiles',
    license: 'BSD-3-Clause',
  },
  {
    name: 'Photon (komoot)',
    url: 'https://photon.komoot.io',
    use: 'geocoding',
    license: 'Apache-2.0',
  },
  {
    name: 'MapLibre GL JS',
    url: 'https://maplibre.org',
    use: 'mapLibrary',
    license: 'BSD-3-Clause',
  },
  {
    name: 'Atkinson Hyperlegible Next, Young Serif',
    url: 'https://fontsource.org',
    use: 'fonts',
    license: 'SIL OFL 1.1',
  },
]
