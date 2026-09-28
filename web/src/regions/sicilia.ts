import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Sicilia: region #18 of the full-Italy rollout. Copy follows Tuscany's pattern with the Sicilian
 * woods (Nebrodi, Madonie, Etna, Peloritani, Ficuzza and the Sicani); seasons from
 * `.gavin-root/docs/species-ecology/sicilia.md`. The bounds take in the small islands.
 */
export const sicilia: RegionDefinition = {
  slug: 'sicilia',
  name: { it: 'Sicilia', en: 'Sicily' },
  whole: { it: 'Tutta la Sicilia', en: 'All of Sicily' },
  bounds: [
    [11.92, 35.49],
    [15.66, 38.82],
  ],
  maxBounds: [
    [10.7, 34.7],
    [16.9, 39.6],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'sicilia',
  wikidata: 'Q1460',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Sicilia',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Sicilia: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Sicilia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Sicilia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Sicilia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Sicilia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Sicilia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Sicilia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi della Sicilia — dai Nebrodi e dalle Madonie all'Etna, fino ai Peloritani, al Bosco della Ficuzza e ai Sicani — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi della Sicilia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione ha due tempi: a maggio e giugno nei castagneti, nelle cerrete e nelle faggete dei Nebrodi e dell'Etna; poi, dopo l'estate secca, da settembre in quota e da ottobre a dicembre più in basso, dalle faggete del Monte Soro e del versante nord dell'Etna ai querceti e alle sugherete di Caronia, fino al porcino nero delle leccete a dicembre.",
        ovoli:
          "La mappa divide i boschi della Sicilia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da fine maggio a dicembre, soprattutto fra settembre e novembre, nei castagneti e nei querceti di collina: le colline dei Peloritani e dei Nebrodi, le Madonie sopra Gratteri, Cefalù e Pollina, il versante nord dell'Etna a Castiglione di Sicilia.",
        gallinacci:
          "La mappa divide i boschi della Sicilia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla primavera all'inverno, soprattutto da ottobre a dicembre: nelle leccete e nelle pinete dei Peloritani sopra Messina, nei castagneti dell'Etna fra Nicolosi e Pedara, nei boschi dei Nebrodi.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Sicilia',
        porcini: 'Indice delle condizioni per i porcini in Sicilia',
        ovoli: 'Indice delle condizioni per gli ovoli in Sicilia',
        gallinacci: 'Indice delle condizioni per i gallinacci in Sicilia',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Sicily',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Sicily: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Sicily: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Sicily: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Sicily: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Sicily: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Sicily: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Sicily: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          'The map divides the woods of Sicily — from the Nebrodi and the Madonie to Etna, and on to the Peloritani, the Bosco della Ficuzza and the Sicani — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.',
        porcini:
          "The map divides the woods of Sicily into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season comes in two parts: in May and June in the chestnut, Turkey oak and beech woods of the Nebrodi and Etna; then, after the dry summer, from September up high and from October to December lower down, from the beech woods of Monte Soro and Etna's north flank to the oak and cork-oak woods of Caronia, and the black porcino of the holm-oak woods into December.",
        ovoli:
          "The map divides the woods of Sicily into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from late May to December, mostly from September to November, in the chestnut and oak woods of the hills: the Peloritani and Nebrodi hills, the Madonie above Gratteri, Cefalù and Pollina, and Etna's north flank at Castiglione di Sicilia.",
        gallinacci:
          "The map divides the woods of Sicily into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from spring into winter, mostly from October to December: in the holm-oak and pine woods of the Peloritani above Messina, in Etna's chestnut belt between Nicolosi and Pedara, and in the woods of the Nebrodi.",
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Sicily',
        porcini: 'Conditions index for porcini in Sicily',
        ovoli: 'Conditions index for ovoli in Sicily',
        gallinacci: 'Conditions index for gallinacci in Sicily',
      },
    },
  },
}
