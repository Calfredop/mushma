import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/** Tuscany: the first served region (live). */
export const toscana: RegionDefinition = {
  slug: 'toscana',
  name: { it: 'Toscana', en: 'Tuscany' },
  whole: { it: 'Tutta la Toscana', en: 'All of Tuscany' },
  bounds: [
    [9.68, 42.23],
    [12.38, 44.48],
  ],
  maxBounds: [
    [8.4, 41.5],
    [13.6, 45.2],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'tuscany',
  wikidata: 'Q1273',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Toscana',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Toscana: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Toscana: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Toscana: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Toscana: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Toscana: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Toscana: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Toscana: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          'La mappa divide i boschi della Toscana in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.',
        porcini:
          "La mappa divide i boschi della Toscana in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va soprattutto da fine estate all'autunno.",
        ovoli:
          'La mappa divide i boschi della Toscana in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da giugno a novembre, soprattutto in autunno.',
        gallinacci:
          "La mappa divide i boschi della Toscana in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione dura quasi tutto l'anno, con i picchi in primavera e in autunno.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Toscana',
        porcini: 'Indice delle condizioni per i porcini in Toscana',
        ovoli: 'Indice delle condizioni per gli ovoli in Toscana',
        gallinacci: 'Indice delle condizioni per i gallinacci in Toscana',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Tuscany',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Tuscany: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Tuscany: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Tuscany: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Tuscany: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Tuscany: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Tuscany: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Tuscany: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides Tuscany's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides Tuscany's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs mainly from late summer through autumn.",
        ovoli:
          "The map divides Tuscany's woods into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from June to November, mostly in autumn.",
        gallinacci:
          "The map divides Tuscany's woods into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs almost all year, peaking in spring and autumn.",
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Tuscany',
        porcini: 'Conditions index for porcini in Tuscany',
        ovoli: 'Conditions index for ovoli in Tuscany',
        gallinacci: 'Conditions index for gallinacci in Tuscany',
      },
    },
  },
}
