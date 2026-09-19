/**
 * Data sources and software credited in the app (AGENTS.md → External APIs;
 * PRD → Constraints → Licensing). Kept in step with the grid and weather
 * pipelines' own source list, api/src/api/config/sources.yaml — that file is
 * the source of truth for names, homepages and licences. Names, URLs and
 * licence identifiers are proper nouns; what each one is used for is translated.
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
    name: 'Copernicus Climate Change Service — ERA5-Land, ERA5',
    url: 'https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land',
    use: 'weather',
    license: 'CC BY 4.0',
  },
  {
    name: 'ECMWF — IFS HRES open data forecasts',
    url: 'https://www.ecmwf.int/en/forecasts/datasets/open-data',
    use: 'weather',
    license: 'CC BY 4.0',
  },
  {
    name: 'ECMWF — EC46, SEAS5 seasonal forecasts (via Open-Meteo)',
    url: 'https://open-meteo.com/en/docs/seasonal-forecast-api',
    use: 'seasonal',
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
    name: 'Regione Toscana — Uso e copertura del suolo',
    url: 'https://www502.regione.toscana.it/geonetwork/srv/api/records/r_toscan:0d4d6640-9a1c-47a4-9a5d-a85cdb36927c',
    use: 'landcover',
    license: 'CC BY 4.0',
  },
  {
    name: 'ISPRA — Corine Land Cover 2018',
    url: 'https://groupware.sinanet.isprambiente.it/uso-copertura-e-consumo-di-suolo/library/copertura-del-suolo/corine-land-cover/corine-land-cover-2018-iv-livello',
    use: 'landcover',
    license: 'CC BY 4.0',
  },
  {
    name: 'Copernicus DEM GLO-30',
    url: 'https://registry.opendata.aws/copernicus-dem/',
    use: 'elevation',
    license: 'Copernicus DEM licence',
  },
  {
    name: 'SoilGrids (ISRIC)',
    url: 'https://soilgrids.org',
    use: 'soil',
    license: 'CC BY 4.0',
  },
  { name: 'ISTAT', url: 'https://www.istat.it', use: 'boundaries', license: 'CC BY 4.0' },
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
    name: 'Mapterhorn',
    url: 'https://mapterhorn.com/attribution',
    use: 'terrain',
    license: 'CC BY 4.0',
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
