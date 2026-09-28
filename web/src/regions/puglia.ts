import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Puglia: region #15 of the full-Italy rollout. Copy follows Tuscany's pattern with the Apulian
 * woods (Gargano, Monti Dauni, Murge, the Ionian gravine and the Salento); seasons from
 * `.gavin-root/docs/species-ecology/puglia.md`. The bounds take in the Tremiti.
 */
export const puglia: RegionDefinition = {
  slug: 'puglia',
  name: { it: 'Puglia', en: 'Apulia' },
  whole: { it: 'Tutta la Puglia', en: 'All of Apulia' },
  bounds: [
    [14.93, 39.79],
    [18.53, 42.23],
  ],
  maxBounds: [
    [13.6, 39.0],
    [19.9, 43.0],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'puglia',
  wikidata: 'Q1447',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Puglia',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Puglia: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Puglia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Puglia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Puglia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Puglia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Puglia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Puglia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi della Puglia — dal Gargano e dai Monti Dauni alle Murge e alle gravine dell'arco ionico, fino al Salento — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi della Puglia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da fine aprile a gennaio: il porcino estivo e il porcino nero da maggio e giugno, poi, dopo i temporali d'estate e soprattutto da ottobre a dicembre, nelle cerrete e nella faggeta della Foresta Umbra sul Gargano, sui Monti Dauni e nei boschi di fragno delle Murge, fra Martina Franca, Mottola e Noci.",
        ovoli:
          "La mappa divide i boschi della Puglia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla fine dell'estate all'autunno, soprattutto fra settembre e ottobre, dopo i temporali, nelle cerrete e nei querceti del Gargano, dei Monti Dauni e delle Murge.",
        gallinacci:
          "La mappa divide i boschi della Puglia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla primavera all'inverno: da aprile a dicembre, e fino a gennaio, nei querceti e nelle leccete di collina; da giugno a ottobre nella faggeta e nelle cerrete del Gargano e dei Monti Dauni.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Puglia',
        porcini: 'Indice delle condizioni per i porcini in Puglia',
        ovoli: 'Indice delle condizioni per gli ovoli in Puglia',
        gallinacci: 'Indice delle condizioni per i gallinacci in Puglia',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Apulia',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Apulia: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Apulia: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Apulia: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Apulia: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Apulia: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Apulia: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Apulia: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          'The map divides the woods of Apulia — from the Gargano and the Monti Dauni to the Murge and the gorges of the Ionian arc, and on to the Salento — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.',
        porcini:
          'The map divides the woods of Apulia into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from late April to January: the summer and black porcini from May and June, then, after summer storms and above all from October to December, in the Turkey-oak woods and the Foresta Umbra beech of the Gargano, in the Monti Dauni and in the Macedonian-oak woods of the Murge, around Martina Franca, Mottola and Noci.',
        ovoli:
          'The map divides the woods of Apulia into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from late summer into autumn, mostly in September and October after storms, in the Turkey-oak and oak woods of the Gargano, the Monti Dauni and the Murge.',
        gallinacci:
          'The map divides the woods of Apulia into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from spring into winter: from April to December, and into January, in the oak and holm-oak woods of the hills; from June to October in the beech and Turkey-oak woods of the Gargano and the Monti Dauni.',
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Apulia',
        porcini: 'Conditions index for porcini in Apulia',
        ovoli: 'Conditions index for ovoli in Apulia',
        gallinacci: 'Conditions index for gallinacci in Apulia',
      },
    },
  },
}
