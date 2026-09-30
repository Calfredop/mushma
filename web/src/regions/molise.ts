import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Molise: region #13 of the full-Italy rollout. Copy follows Tuscany's pattern with the Molise
 * woods (Matese, Montagnola di Frosolone, Mainarde, Alto Molise, the Turkey-oak hills); seasons
 * from `.gavin-root/docs/species-ecology/molise.md`.
 */
export const molise: RegionDefinition = {
  slug: 'molise',
  name: { it: 'Molise', en: 'Molise' },
  whole: { it: 'Tutto il Molise', en: 'All of Molise' },
  bounds: [
    [13.94, 41.36],
    [15.17, 42.08],
  ],
  maxBounds: [
    [12.64, 40.56],
    [16.47, 42.88],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'molise',
  wikidata: 'Q1443',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Molise',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Molise: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Molise: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Molise: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Molise: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Molise: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Molise: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Molise: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi del Molise — dal Matese e dalla Montagnola di Frosolone alle Mainarde e all'Alto Molise di Capracotta e Agnone, fino alle cerrete delle colline di Campobasso — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi del Molise in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da giugno a novembre: d'estate il porcino estivo nelle cerrete e nelle faggete del Matese e dell'Alto Molise, poi il porcino nero nei querceti di collina e, da settembre, il porcino delle faggete, dal Matese a Capracotta.",
        ovoli:
          'La mappa divide i boschi del Molise in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da agosto a ottobre, nei boschi di cerro e di roverella sotto i 900–1200 metri, dalle colline di Campobasso alle valli di Isernia.',
        gallinacci:
          "La mappa divide i boschi del Molise in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla primavera al tardo autunno: in montagna da giugno a ottobre nelle faggete del Matese, della Montagnola di Frosolone e dell'Alto Molise, in collina nelle cerrete fino a dicembre.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Molise',
        porcini: 'Indice delle condizioni per i porcini in Molise',
        ovoli: 'Indice delle condizioni per gli ovoli in Molise',
        gallinacci: 'Indice delle condizioni per i gallinacci in Molise',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Molise',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Molise: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Molise: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Molise: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Molise: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Molise: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Molise: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Molise: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          'The map divides the woods of Molise — from the Matese and the Montagnola di Frosolone to the Mainarde and the Alto Molise around Capracotta and Agnone, and on to the Turkey-oak woods of the Campobasso hills — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.',
        porcini:
          'The map divides the woods of Molise into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from June to November: in summer the summer porcino in the Turkey-oak and beech woods of the Matese and the Alto Molise, then the black porcino in the oak woods of the hills and, from September, the beech porcino, from the Matese to Capracotta.',
        ovoli:
          'The map divides the woods of Molise into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from August to October, in the Turkey oak and downy oak woods below 900–1,200 metres, from the Campobasso hills to the valleys around Isernia.',
        gallinacci:
          'The map divides the woods of Molise into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from spring to late autumn: in the mountains from June to October in the beech woods of the Matese, the Montagnola di Frosolone and the Alto Molise, and in the hills, in the Turkey-oak woods, until December.',
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Molise',
        porcini: 'Conditions index for porcini in Molise',
        ovoli: 'Conditions index for ovoli in Molise',
        gallinacci: 'Conditions index for gallinacci in Molise',
      },
    },
  },
}
