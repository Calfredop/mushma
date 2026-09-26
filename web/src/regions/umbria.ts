import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Umbria (region-umbria card). Copy follows Tuscany's pattern; the areas and seasons come from
 * .gavin-root/docs/species-ecology/umbria.md (Places, per-taxon seasons).
 */
export const umbria: RegionDefinition = {
  slug: 'umbria',
  name: { it: 'Umbria', en: 'Umbria' },
  whole: { it: "Tutta l'Umbria", en: 'All of Umbria' },
  bounds: [
    [11.89, 42.36],
    [13.27, 43.62],
  ],
  maxBounds: [
    [10.6, 41.6],
    [14.5, 44.4],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'umbria',
  wikidata: 'Q1280',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Umbria',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Umbria: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Umbria: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Umbria: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Umbria: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Umbria: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Umbria: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Umbria: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi dell'Umbria — dalle faggete del Monte Cucco alla Valnerina, dall'Alta Valle del Tevere all'Orvietano — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi dell'Umbria in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre, soprattutto da fine agosto a ottobre, nei querceti delle colline e nelle faggete dell'Appennino.",
        ovoli:
          "La mappa divide i boschi dell'Umbria in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dall'estate all'autunno, soprattutto a settembre e ottobre, nei boschi di cerro, roverella e castagno sotto i 900 m.",
        gallinacci:
          "La mappa divide i boschi dell'Umbria in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre, con i picchi a fine primavera e in autunno.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Umbria',
        porcini: 'Indice delle condizioni per i porcini in Umbria',
        ovoli: 'Indice delle condizioni per gli ovoli in Umbria',
        gallinacci: 'Indice delle condizioni per i gallinacci in Umbria',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Umbria',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Umbria: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Umbria: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Umbria: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Umbria: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Umbria: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Umbria: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Umbria: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides Umbria's woods — from the beech woods of Monte Cucco to the Valnerina, from the upper Tiber valley to the Orvietano — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides Umbria's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November, mostly from late August to October, in the oak woods of the hills and the beech woods of the Apennines.",
        ovoli:
          "The map divides Umbria's woods into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from summer into autumn, mostly in September and October, in Turkey oak, downy oak and chestnut woods below 900 m.",
        gallinacci:
          "The map divides Umbria's woods into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November, peaking in late spring and autumn.",
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Umbria',
        porcini: 'Conditions index for porcini in Umbria',
        ovoli: 'Conditions index for ovoli in Umbria',
        gallinacci: 'Conditions index for gallinacci in Umbria',
      },
    },
  },
}
