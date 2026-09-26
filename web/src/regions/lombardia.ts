import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Lombardia: region #8 of the full-Italy rollout. Copy follows Tuscany's pattern with the Lombard
 * Alps, prealps and Oltrepò; seasons from `.gavin-root/docs/species-ecology/lombardia.md`.
 */
export const lombardia: RegionDefinition = {
  slug: 'lombardia',
  name: { it: 'Lombardia', en: 'Lombardy' },
  bounds: [
    [8.49, 44.67],
    [11.43, 46.64],
  ],
  maxBounds: [
    [7.2, 43.9],
    [12.7, 47.4],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'lombardia',
  wikidata: 'Q1210',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Lombardia',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Lombardia: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Lombardia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Lombardia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Lombardia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Lombardia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Lombardia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Lombardia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi della Lombardia — dalla Valtellina e dalla Val Camonica alle Orobie, ai laghi prealpini e all'Oltrepò Pavese — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi della Lombardia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da luglio a ottobre: sopra i 1300 metri, nelle peccete e nelle faggete della Valtellina, della Val Camonica e delle Orobie, il picco è tra agosto e settembre; più in basso, nei castagneti e nelle faggete dei laghi prealpini e dell'Oltrepò, continua fino a fine ottobre.",
        ovoli:
          "La mappa divide i boschi della Lombardia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da agosto a ottobre, nei castagneti e nei querceti sotto gli 800 metri: sulle sponde del Lario e degli altri laghi prealpini e nell'Oltrepò Pavese.",
        gallinacci:
          'La mappa divide i boschi della Lombardia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da giugno a ottobre: in quota, nelle faggete e nelle peccete delle valli alpine, il picco è tra luglio e agosto; più in basso, nei castagneti e nelle faggete delle Prealpi, continua fino a ottobre.',
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Lombardia',
        porcini: 'Indice delle condizioni per i porcini in Lombardia',
        ovoli: 'Indice delle condizioni per gli ovoli in Lombardia',
        gallinacci: 'Indice delle condizioni per i gallinacci in Lombardia',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Lombardy',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Lombardy: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Lombardy: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Lombardy: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Lombardy: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Lombardy: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Lombardy: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Lombardy: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          'The map divides the woods of Lombardy — from Valtellina and Val Camonica to the Orobie, the prealpine lakes and the Oltrepò Pavese — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.',
        porcini:
          'The map divides the woods of Lombardy into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from July to October: above 1,300 metres, in the spruce and beech woods of Valtellina, Val Camonica and the Orobie, it peaks between August and September; lower down, in the chestnut and beech woods of the prealpine lakes and the Oltrepò, it runs on to late October.',
        ovoli:
          'The map divides the woods of Lombardy into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from August to October, in the chestnut and oak woods below 800 metres: on the shores of Lake Como and the other prealpine lakes and in the Oltrepò Pavese.',
        gallinacci:
          'The map divides the woods of Lombardy into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from June to October: up high, in the beech and spruce woods of the Alpine valleys, it peaks between July and August; lower down, in the chestnut and beech woods of the prealps, it runs on into October.',
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Lombardy',
        porcini: 'Conditions index for porcini in Lombardy',
        ovoli: 'Conditions index for ovoli in Lombardy',
        gallinacci: 'Conditions index for gallinacci in Lombardy',
      },
    },
  },
}
