import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Basilicata: region #16 of the full-Italy rollout. Copy follows Tuscany's pattern with the
 * Lucanian woods (Pollino, Sirino, the Sellata and the Maddalena, the Vulture, Gallipoli Cognato);
 * seasons from `.gavin-root/docs/species-ecology/basilicata.md`.
 */
export const basilicata: RegionDefinition = {
  slug: 'basilicata',
  name: { it: 'Basilicata', en: 'Basilicata' },
  whole: { it: 'Tutta la Basilicata', en: 'All of Basilicata' },
  bounds: [
    [15.33, 39.89],
    [16.87, 41.14],
  ],
  maxBounds: [
    [14.03, 39.09],
    [18.17, 41.94],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'basilicata',
  wikidata: 'Q1452',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Basilicata',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Basilicata: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Basilicata: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Basilicata: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Basilicata: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Basilicata: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Basilicata: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Basilicata: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi della Basilicata — dal Pollino e dal Sirino alla Sellata, alla Maddalena e alla Val d'Agri, fino al Vulture e alle cerrete di Gallipoli Cognato — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi della Basilicata in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre, con una pausa nella siccità d'estate: a maggio e giugno il porcino nero nelle cerrete e il porcino estivo, d'estate solo in alta quota sul Sirino e sul Pollino, poi, dopo i temporali di fine agosto, i porcini delle faggete e dei querceti, soprattutto sul versante occidentale, dal Golfo di Maratea e da Lauria e Lagonegro alla Val d'Agri.",
        ovoli:
          "La mappa divide i boschi della Basilicata in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dall'estate all'autunno, soprattutto fra settembre e ottobre, nelle cerrete e nei castagneti di collina e di media montagna, dal Vulture alla Val d'Agri e al Pollino.",
        gallinacci:
          "La mappa divide i boschi della Basilicata in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio all'inverno: fra maggio e giugno nei querceti, in montagna fino a ottobre nelle faggete del Pollino e del Sirino, in collina fino a dicembre, anche sul versante tirrenico.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Basilicata',
        porcini: 'Indice delle condizioni per i porcini in Basilicata',
        ovoli: 'Indice delle condizioni per gli ovoli in Basilicata',
        gallinacci: 'Indice delle condizioni per i gallinacci in Basilicata',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Basilicata',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Basilicata: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Basilicata: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Basilicata: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Basilicata: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Basilicata: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Basilicata: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Basilicata: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides the woods of Basilicata — from the Pollino and the Sirino to the Sellata, the Maddalena and the Val d'Agri, and on to the Vulture and the Turkey-oak forest of Gallipoli Cognato — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides the woods of Basilicata into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November, with a pause in the summer drought: in May and June the black porcino in the Turkey-oak woods and the summer porcino, in summer only high up on the Sirino and the Pollino, then, after the storms of late August, the porcini of the beech and oak woods, above all on the western side, from the Gulf of Maratea, Lauria and Lagonegro to the Val d'Agri.",
        ovoli:
          "The map divides the woods of Basilicata into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from summer into autumn, mostly in September and October, in the Turkey-oak and chestnut woods of the hills and lower mountains, from the Vulture to the Val d'Agri and the Pollino.",
        gallinacci:
          'The map divides the woods of Basilicata into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May into winter: in May and June in the oak woods, until October in the mountains in the beech woods of the Pollino and the Sirino, and into December in the hills, the Tyrrhenian side included.',
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Basilicata',
        porcini: 'Conditions index for porcini in Basilicata',
        ovoli: 'Conditions index for ovoli in Basilicata',
        gallinacci: 'Conditions index for gallinacci in Basilicata',
      },
    },
  },
}
