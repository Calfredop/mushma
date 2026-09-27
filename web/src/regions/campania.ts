import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Campania: region #14 of the full-Italy rollout. Copy follows Tuscany's pattern with the
 * Campanian woods (Matese, Taburno, Partenio, Picentini, Alburni, Cilento, Roccamonfina); seasons
 * from `.gavin-root/docs/species-ecology/campania.md`. Bounds hold Ischia, Procida and Capri.
 */
export const campania: RegionDefinition = {
  slug: 'campania',
  name: { it: 'Campania', en: 'Campania' },
  whole: { it: 'Tutta la Campania', en: 'All of Campania' },
  bounds: [
    [13.76, 39.99],
    [15.81, 41.51],
  ],
  maxBounds: [
    [12.5, 39.2],
    [17.1, 42.3],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'campania',
  wikidata: 'Q1438',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Campania',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Campania: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Campania: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Campania: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Campania: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Campania: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Campania: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Campania: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          'La mappa divide i boschi della Campania — dal Matese e dal Taburno al Partenio, ai Picentini e agli Alburni, fino al Cilento — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.',
        porcini:
          "La mappa divide i boschi della Campania in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla tarda primavera a novembre, con una pausa nella siccità d'estate: il porcino estivo nelle faggete dei Picentini, del Laceno e del Matese fra 1100 e 1600 metri, il porcino nero più in basso, nei castagneti e nei querceti dall'Irpinia al Roccamonfina e al Cilento.",
        ovoli:
          "La mappa divide i boschi della Campania in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dall'estate all'autunno, con il picco a settembre, nei castagneti e nei boschi di cerro e di roverella di collina, dai dintorni di Bagnoli Irpino al Sannio e al Cilento.",
        gallinacci:
          "La mappa divide i boschi della Campania in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio all'inverno: in montagna da fine primavera, nelle faggete del Laceno e del Matese; in collina fino a dicembre, nei castagneti e nei querceti.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Campania',
        porcini: 'Indice delle condizioni per i porcini in Campania',
        ovoli: 'Indice delle condizioni per gli ovoli in Campania',
        gallinacci: 'Indice delle condizioni per i gallinacci in Campania',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Campania',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Campania: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Campania: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Campania: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Campania: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Campania: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Campania: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Campania: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          'The map divides the woods of Campania — from the Matese and the Taburno to the Partenio, the Picentini and the Alburni, and on to the Cilento — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.',
        porcini:
          'The map divides the woods of Campania into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from late spring to November, with a pause in the summer drought: the summer porcino in the beech woods of the Picentini, the Laceno and the Matese between 1,100 and 1,600 metres, the black porcino lower down, in the chestnut and oak woods from Irpinia to Roccamonfina and the Cilento.',
        ovoli:
          'The map divides the woods of Campania into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from summer into autumn, peaking in September, in the chestnut, Turkey oak and downy oak woods of the hills, from around Bagnoli Irpino to the Sannio and the Cilento.',
        gallinacci:
          'The map divides the woods of Campania into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May into winter: from late spring in the mountains, in the beech woods of the Laceno and the Matese; into December in the hills, in the chestnut and oak woods.',
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Campania',
        porcini: 'Conditions index for porcini in Campania',
        ovoli: 'Conditions index for ovoli in Campania',
        gallinacci: 'Conditions index for gallinacci in Campania',
      },
    },
  },
}
