import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Emilia-Romagna: the Apennine side that borders Tuscany (Parma and Borgotaro, Reggio, Modena,
 * Bologna, the Romagna side of the Foreste Casentinesi). Copy follows Tuscany's pattern.
 */
export const emiliaRomagna: RegionDefinition = {
  slug: 'emilia-romagna',
  name: { it: 'Emilia-Romagna', en: 'Emilia-Romagna' },
  bounds: [
    [9.19, 43.73],
    [12.76, 45.14],
  ],
  maxBounds: [
    [7.9, 43.0],
    [14.0, 45.9],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'emilia_romagna',
  wikidata: 'Q1263',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Emilia-Romagna',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Emilia-Romagna: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Emilia-Romagna: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Emilia-Romagna: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Emilia-Romagna: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Emilia-Romagna: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Emilia-Romagna: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Emilia-Romagna: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi dell'Emilia-Romagna — dall'Appennino parmense della Val Taro e della Val Ceno al Frignano, all'Appennino bolognese e alle Foreste Casentinesi sul versante romagnolo — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi dell'Emilia-Romagna in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va soprattutto da fine estate all'autunno, nei castagneti e nelle faggete dell'Appennino, dalla Val Taro di Borgotaro al Frignano e all'Appennino bolognese.",
        ovoli:
          "La mappa divide i boschi dell'Emilia-Romagna in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dall'estate all'autunno, sulle colline a querce e castagni dal Piacentino alla Romagna.",
        gallinacci:
          "La mappa divide i boschi dell'Emilia-Romagna in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dall'inizio dell'estate all'autunno, nelle faggete e nei castagneti dell'Appennino.",
      },
      dataset: {
        region:
          'Indice delle condizioni per porcini, ovoli e gallinacci in Emilia-Romagna',
        porcini: 'Indice delle condizioni per i porcini in Emilia-Romagna',
        ovoli: 'Indice delle condizioni per gli ovoli in Emilia-Romagna',
        gallinacci: 'Indice delle condizioni per i gallinacci in Emilia-Romagna',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Emilia-Romagna',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Emilia-Romagna: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Emilia-Romagna: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Emilia-Romagna: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Emilia-Romagna: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Emilia-Romagna: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Emilia-Romagna: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Emilia-Romagna: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides Emilia-Romagna's woods — from the Parma Apennines of the Taro and Ceno valleys to the Frignano, the Bologna Apennines and the Romagna side of the Casentino Forests — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides Emilia-Romagna's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs mainly from late summer through autumn, in the chestnut and beech woods of the Apennines, from Borgotaro's Taro valley to the Frignano and the Bologna Apennines.",
        ovoli:
          "The map divides Emilia-Romagna's woods into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from summer into autumn, on the oak and chestnut hills from Piacenza to Romagna.",
        gallinacci:
          "The map divides Emilia-Romagna's woods into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from early summer into autumn, in the beech and chestnut woods of the Apennines.",
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Emilia-Romagna',
        porcini: 'Conditions index for porcini in Emilia-Romagna',
        ovoli: 'Conditions index for ovoli in Emilia-Romagna',
        gallinacci: 'Conditions index for gallinacci in Emilia-Romagna',
      },
    },
  },
}
