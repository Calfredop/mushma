import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Piemonte: region #6 of the full-Italy rollout. Copy follows Tuscany's pattern with Piedmont's
 * areas (Langhe and Roero, the Cuneo valleys, the Alps from Val di Susa to the Ossola, the Val
 * Borbera Apennine); seasons from `.gavin-root/docs/species-ecology/piemonte.md`.
 */
export const piemonte: RegionDefinition = {
  slug: 'piemonte',
  name: { it: 'Piemonte', en: 'Piedmont' },
  whole: { it: 'Tutto il Piemonte', en: 'All of Piedmont' },
  bounds: [
    [6.62, 44.06],
    [9.22, 46.47],
  ],
  maxBounds: [
    [5.3, 43.3],
    [10.5, 47.2],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'piemonte',
  wikidata: 'Q1216',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Piemonte',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Piemonte: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Piemonte: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Piemonte: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Piemonte: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Piemonte: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Piemonte: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Piemonte: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi del Piemonte — dai castagneti delle Langhe, del Roero e delle valli cuneesi ai faggeti e ai lariceti delle Alpi, dalla Val di Susa all'Ossola, fino all'Appennino della Val Borbera — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          'La mappa divide i boschi del Piemonte in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre: da luglio a settembre nei lariceti, negli abeti e nei faggeti delle Alpi, tra settembre e ottobre nei castagneti e nei faggeti delle valli e delle colline.',
        ovoli:
          "La mappa divide i boschi del Piemonte in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da giugno a novembre, soprattutto in agosto e settembre, nei castagneti e nei querceti delle colline sotto i 1000 m, dalle Langhe e dal Roero al Monferrato e all'Appennino.",
        gallinacci:
          'La mappa divide i boschi del Piemonte in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre: in collina da maggio a ottobre, in montagna da luglio a metà ottobre, nei castagneti, nei faggeti e nei boschi di abete delle valli alpine.',
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Piemonte',
        porcini: 'Indice delle condizioni per i porcini in Piemonte',
        ovoli: 'Indice delle condizioni per gli ovoli in Piemonte',
        gallinacci: 'Indice delle condizioni per i gallinacci in Piemonte',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Piedmont',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Piedmont: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Piedmont: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Piedmont: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Piedmont: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Piedmont: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Piedmont: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Piedmont: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides Piedmont's woods — from the chestnut woods of the Langhe, the Roero and the Cuneo valleys to the beech and larch woods of the Alps, from the Val di Susa to the Ossola, and on to the Val Borbera Apennine — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides Piedmont's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November: from July to September in the larch, spruce and beech woods of the Alps, in September and October in the chestnut and beech woods of the valleys and hills.",
        ovoli:
          "The map divides Piedmont's woods into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from June to November, mostly in August and September, in the chestnut and oak woods of the hills below 1000 m, from the Langhe and the Roero to the Monferrato and the Apennines.",
        gallinacci:
          "The map divides Piedmont's woods into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November: in the hills from May to October, in the mountains from July to mid-October, in the chestnut, beech and fir woods of the Alpine valleys.",
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Piedmont',
        porcini: 'Conditions index for porcini in Piedmont',
        ovoli: 'Conditions index for ovoli in Piedmont',
        gallinacci: 'Conditions index for gallinacci in Piedmont',
      },
    },
  },
}
