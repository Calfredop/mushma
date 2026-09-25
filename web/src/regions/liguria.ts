import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Liguria: region #2 of the full-Italy rollout. Copy follows Tuscany's pattern with Ligurian
 * areas (Alpi Liguri, Beigua, Val Bormida, Val d'Aveto, Val di Vara); seasons from
 * `.gavin-root/docs/species-ecology/liguria.md`.
 */
export const liguria: RegionDefinition = {
  slug: 'liguria',
  name: { it: 'Liguria', en: 'Liguria' },
  bounds: [
    [7.49, 43.77],
    [10.08, 44.68],
  ],
  maxBounds: [
    [6.2, 43.0],
    [11.4, 45.4],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'liguria',
  wikidata: 'Q1256',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Liguria',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Liguria: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Liguria: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Liguria: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Liguria: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Liguria: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Liguria: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Liguria: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi della Liguria — dalle Alpi Liguri al Beigua e alla Val Bormida, fino alla Val d'Aveto e alla Val di Vara — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi della Liguria in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va soprattutto da fine estate all'autunno, nei faggeti e nei castagneti dell'entroterra, dalla Val d'Aveto alle Alpi Liguri.",
        ovoli:
          "La mappa divide i boschi della Liguria in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dall'estate all'autunno, nei castagneti e nei querceti delle colline più calde.",
        gallinacci:
          "La mappa divide i boschi della Liguria in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla tarda primavera all'autunno, nei castagneti e nei faggeti dell'entroterra.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Liguria',
        porcini: 'Indice delle condizioni per i porcini in Liguria',
        ovoli: 'Indice delle condizioni per gli ovoli in Liguria',
        gallinacci: 'Indice delle condizioni per i gallinacci in Liguria',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Liguria',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Liguria: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Liguria: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Liguria: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Liguria: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Liguria: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Liguria: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Liguria: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides Liguria's woods — from the Ligurian Alps to the Beigua and the Val Bormida, and on to the Val d'Aveto and the Val di Vara — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides Liguria's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs mainly from late summer through autumn, in the beech and chestnut woods inland, from the Val d'Aveto to the Ligurian Alps.",
        ovoli:
          "The map divides Liguria's woods into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from summer into autumn, in chestnut and oak woods on the warmer hills.",
        gallinacci:
          "The map divides Liguria's woods into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from late spring into autumn, in chestnut and beech woods inland.",
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Liguria',
        porcini: 'Conditions index for porcini in Liguria',
        ovoli: 'Conditions index for ovoli in Liguria',
        gallinacci: 'Conditions index for gallinacci in Liguria',
      },
    },
  },
}
