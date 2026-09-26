import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Marche: region #5 of the full-Italy rollout. Copy follows Tuscany's pattern with the Marche
 * Apennine areas (Montefeltro, Catria and Nerone, Sibillini, Laga); seasons from
 * `.gavin-root/docs/species-ecology/marche.md`.
 */
export const marche: RegionDefinition = {
  slug: 'marche',
  name: { it: 'Marche', en: 'Marche' },
  locative: { it: 'nelle Marche', en: 'in Marche' },
  whole: { it: 'Tutte le Marche', en: 'All of Marche' },
  bounds: [
    [12.18, 42.68],
    [13.92, 43.97],
  ],
  maxBounds: [
    [10.9, 41.9],
    [15.2, 44.75],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'marche',
  wikidata: 'Q1279',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci nelle Marche',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci nelle Marche: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini nelle Marche: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini nelle Marche: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli nelle Marche: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli nelle Marche: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci nelle Marche: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci nelle Marche: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          'La mappa divide i boschi delle Marche — dal Montefeltro al Catria e al Nerone, fino ai Sibillini e ai Monti della Laga — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.',
        porcini:
          'La mappa divide i boschi delle Marche in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da fine maggio a ottobre: qui il porcino più comune è quello estivo, nei querceti, nei boschi di carpino nero e nelle faggete fino a circa 1300 metri, dal Montefeltro ai Sibillini.',
        ovoli:
          "La mappa divide i boschi delle Marche in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dall'estate all'autunno, con il picco a settembre, nei boschi di cerro, di roverella e di castagno sotto gli 800–900 metri.",
        gallinacci:
          "La mappa divide i boschi delle Marche in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla primavera al tardo autunno, con il picco a giugno, nelle faggete e nei querceti dell'Appennino, dal Catria ai Sibillini.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci nelle Marche',
        porcini: 'Indice delle condizioni per i porcini nelle Marche',
        ovoli: 'Indice delle condizioni per gli ovoli nelle Marche',
        gallinacci: 'Indice delle condizioni per i gallinacci nelle Marche',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Marche',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Marche: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Marche: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Marche: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Marche: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Marche: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Marche: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Marche: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          'The map divides the woods of Marche — from the Montefeltro to Monte Catria and Monte Nerone, and on to the Sibillini and the Monti della Laga — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.',
        porcini:
          'The map divides the woods of Marche into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from late May to October: the commonest porcino here is the summer one, in the oak, hop-hornbeam and beech woods up to about 1,300 metres, from the Montefeltro to the Sibillini.',
        ovoli:
          'The map divides the woods of Marche into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from summer into autumn, peaking in September, in the Turkey oak, downy oak and chestnut woods below 800–900 metres.',
        gallinacci:
          'The map divides the woods of Marche into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from spring to late autumn, peaking in June, in the beech and oak woods of the Apennines, from Monte Catria to the Sibillini.',
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Marche',
        porcini: 'Conditions index for porcini in Marche',
        ovoli: 'Conditions index for ovoli in Marche',
        gallinacci: 'Conditions index for gallinacci in Marche',
      },
    },
  },
}
