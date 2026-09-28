import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Calabria: region #17 of the full-Italy rollout. Copy follows Tuscany's pattern with the
 * Calabrian woods (Pollino, Catena Costiera, Sila, Serre, Aspromonte); seasons from
 * `.gavin-root/docs/species-ecology/calabria.md`.
 */
export const calabria: RegionDefinition = {
  slug: 'calabria',
  name: { it: 'Calabria', en: 'Calabria' },
  whole: { it: 'Tutta la Calabria', en: 'All of Calabria' },
  bounds: [
    [15.63, 37.91],
    [17.21, 40.15],
  ],
  maxBounds: [
    [14.4, 37.1],
    [18.5, 40.95],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'calabria',
  wikidata: 'Q1458',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Calabria',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Calabria: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Calabria: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Calabria: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Calabria: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Calabria: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Calabria: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Calabria: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi della Calabria — dal Pollino e dalla Catena Costiera alla Sila, fino alle Serre e all'Aspromonte — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi della Calabria in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a dicembre: il porcino dei pini nelle pinete di laricio della Sila e del Pollino già a maggio e giugno, poi, dopo i temporali d'estate e soprattutto da settembre a novembre, i porcini delle faggete e dei castagneti dalla Sila e dalla Catena Costiera alle Serre e all'Aspromonte, e il porcino nero nei querceti più bassi fino a dicembre.",
        ovoli:
          "La mappa divide i boschi della Calabria in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dall'estate all'autunno, soprattutto fra settembre e ottobre, nei castagneti e nei querceti di collina e di media montagna: la Catena Costiera sopra Cerisano e Mendicino, la Presila fra la Sila Piccola e la Sila Greca, le colline di Rossano.",
        gallinacci:
          "La mappa divide i boschi della Calabria in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio all'inverno: in montagna da giugno a ottobre, nelle faggete; in collina fino a gennaio, nei castagneti, nei querceti e nelle sugherete, soprattutto nel Cosentino.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Calabria',
        porcini: 'Indice delle condizioni per i porcini in Calabria',
        ovoli: 'Indice delle condizioni per gli ovoli in Calabria',
        gallinacci: 'Indice delle condizioni per i gallinacci in Calabria',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Calabria',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Calabria: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Calabria: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Calabria: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Calabria: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Calabria: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Calabria: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Calabria: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          'The map divides the woods of Calabria — from the Pollino and the Catena Costiera to the Sila, and on to the Serre and the Aspromonte — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.',
        porcini:
          'The map divides the woods of Calabria into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to December: the pine porcino in the laricio pinewoods of the Sila and the Pollino as early as May and June, then, after summer storms and above all from September to November, the porcini of the beech and chestnut woods from the Sila and the Catena Costiera to the Serre and the Aspromonte, and the black porcino in the lower oak woods into December.',
        ovoli:
          'The map divides the woods of Calabria into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from summer into autumn, mostly in September and October, in the chestnut and oak woods of the hills and lower mountains: the Catena Costiera above Cerisano and Mendicino, the pre-Sila between the Sila Piccola and the Sila Greca, the hills around Rossano.',
        gallinacci:
          'The map divides the woods of Calabria into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May into winter: from June to October in the mountains, in the beech woods; into January in the hills, in the chestnut, oak and cork-oak woods, above all around Cosenza.',
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Calabria',
        porcini: 'Conditions index for porcini in Calabria',
        ovoli: 'Conditions index for ovoli in Calabria',
        gallinacci: 'Conditions index for gallinacci in Calabria',
      },
    },
  },
}
