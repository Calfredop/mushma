import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Lazio: region #4 of the full-Italy rollout. Copy follows Tuscany's pattern with the Lazio woods
 * (Cimini, Sabatini, Tolfa, Castelli Romani, Terminillo, Simbruini, Ernici); seasons and places from
 * `.gavin-root/docs/species-ecology/lazio.md`. Bounds hold the Pontine islands (Ponza, Ventotene).
 */
export const lazio: RegionDefinition = {
  slug: 'lazio',
  name: { it: 'Lazio', en: 'Lazio' },
  locative: { it: 'nel Lazio', en: 'in Lazio' },
  whole: { it: 'Tutto il Lazio', en: 'All of Lazio' },
  bounds: [
    [11.44, 40.78],
    [14.03, 42.84],
  ],
  maxBounds: [
    [10.1, 40.0],
    [15.3, 43.6],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'lazio',
  wikidata: 'Q1282',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci nel Lazio',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci nel Lazio: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini nel Lazio: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini nel Lazio: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli nel Lazio: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli nel Lazio: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci nel Lazio: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci nel Lazio: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          'La mappa divide i boschi del Lazio — dai Monti Cimini e dalla Tolfa ai Castelli Romani, fino al Terminillo, ai Simbruini e agli Ernici — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.',
        porcini:
          'La mappa divide i boschi del Lazio in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da giugno a novembre, soprattutto in autunno: il porcino estivo e quello nero nelle cerrete e nei castagneti dei Monti Cimini, dei Sabatini, della Tolfa e di Monte Rufeno, il porcino nelle faggete del Terminillo, dei Simbruini e degli Ernici.',
        ovoli:
          "La mappa divide i boschi del Lazio in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va soprattutto da fine estate all'autunno, nelle cerrete e nei castagneti di Monte Venere, di Manziana e di Monte Rufeno e sui Monti Lucretili.",
        gallinacci:
          "La mappa divide i boschi del Lazio in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione dura quasi tutto l'anno, con il picco in autunno e sulla costa fino a gennaio, nei castagneti dei Castelli Romani, nei querceti dei Sabatini e nelle faggete di Allumiere.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci nel Lazio',
        porcini: 'Indice delle condizioni per i porcini nel Lazio',
        ovoli: 'Indice delle condizioni per gli ovoli nel Lazio',
        gallinacci: 'Indice delle condizioni per i gallinacci nel Lazio',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Lazio',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Lazio: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Lazio: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Lazio: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Lazio: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Lazio: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Lazio: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Lazio: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          'The map divides the woods of Lazio — from the Monti Cimini and the Tolfa hills to the Castelli Romani, and on to the Terminillo, the Simbruini and the Ernici — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.',
        porcini:
          'The map divides the woods of Lazio into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from June to November, mostly in autumn: the summer and the dark porcino in the Turkey oak and chestnut woods of the Monti Cimini, the Sabatini, the Tolfa hills and Monte Rufeno, the porcino in the beech woods of the Terminillo, the Simbruini and the Ernici.',
        ovoli:
          'The map divides the woods of Lazio into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs mainly from late summer through autumn, in the Turkey oak and chestnut woods of Monte Venere, Manziana and Monte Rufeno and on the Monti Lucretili.',
        gallinacci:
          'The map divides the woods of Lazio into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs almost all year, peaking in autumn and lasting into January on the coast, in the chestnut woods of the Castelli Romani, the oak woods of the Sabatini and the beech woods of Allumiere.',
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Lazio',
        porcini: 'Conditions index for porcini in Lazio',
        ovoli: 'Conditions index for ovoli in Lazio',
        gallinacci: 'Conditions index for gallinacci in Lazio',
      },
    },
  },
}
