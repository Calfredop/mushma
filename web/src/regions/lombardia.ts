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
          "La mappa divide i boschi della Lombardia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla tarda primavera all'autunno, nei castagneti e nelle faggete delle Prealpi e nelle peccete e nei lariceti delle valli alpine, dalla Valtellina all'Oltrepò.",
        ovoli:
          "La mappa divide i boschi della Lombardia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dall'estate all'inizio dell'autunno, nei castagneti e nei querceti delle sponde dei laghi prealpini e dell'Oltrepò Pavese.",
        gallinacci:
          "La mappa divide i boschi della Lombardia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da giugno all'autunno, nelle faggete, nelle peccete e nei boschi misti di abete e faggio delle Prealpi e delle valli alpine.",
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
          'The map divides the woods of Lombardy into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from late spring into autumn, in the chestnut and beech woods of the prealps and the spruce and larch woods of the Alpine valleys, from Valtellina to the Oltrepò.',
        ovoli:
          'The map divides the woods of Lombardy into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from summer into early autumn, in the chestnut and oak woods on the shores of the prealpine lakes and in the Oltrepò Pavese.',
        gallinacci:
          'The map divides the woods of Lombardy into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from June into autumn, in the beech, spruce and fir-beech woods of the prealps and the Alpine valleys.',
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
