import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Abruzzo: region #12 of the full-Italy rollout. Copy follows Tuscany's pattern with the Abruzzo
 * mountain areas (Laga, Gran Sasso, Majella, Parco Nazionale d'Abruzzo, Alto Sangro); seasons from
 * `.gavin-root/docs/species-ecology/abruzzo.md`.
 */
export const abruzzo: RegionDefinition = {
  slug: 'abruzzo',
  name: { it: 'Abruzzo', en: 'Abruzzo' },
  whole: { it: "Tutto l'Abruzzo", en: 'All of Abruzzo' },
  bounds: [
    [13.01, 41.68],
    [14.79, 42.9],
  ],
  maxBounds: [
    [11.7, 40.9],
    [16.1, 43.7],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'abruzzo',
  wikidata: 'Q1284',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Abruzzo',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Abruzzo: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Abruzzo: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Abruzzo: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Abruzzo: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Abruzzo: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Abruzzo: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Abruzzo: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi dell'Abruzzo — dai Monti della Laga e dal Gran Sasso alla Majella, fino al Parco Nazionale d'Abruzzo e all'Alto Sangro — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi dell'Abruzzo in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da giugno a ottobre: d'estate il porcino estivo nei querceti, nei castagneti e nelle faggete più basse, da settembre il porcino delle faggete, che qui salgono fin quasi a 1900 metri, dalla Laga alla Majella.",
        ovoli:
          "La mappa divide i boschi dell'Abruzzo in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da agosto a ottobre, nei boschi di castagno, di cerro e di roverella sotto i 900–1200 metri, dai Monti della Laga alla Valle Roveto.",
        gallinacci:
          "La mappa divide i boschi dell'Abruzzo in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla primavera al tardo autunno: in montagna da giugno a ottobre nelle faggete e nei querceti, dalla Laga al Parco Nazionale d'Abruzzo, in collina fino a dicembre.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Abruzzo',
        porcini: 'Indice delle condizioni per i porcini in Abruzzo',
        ovoli: 'Indice delle condizioni per gli ovoli in Abruzzo',
        gallinacci: 'Indice delle condizioni per i gallinacci in Abruzzo',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Abruzzo',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Abruzzo: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Abruzzo: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Abruzzo: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Abruzzo: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Abruzzo: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Abruzzo: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Abruzzo: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides the woods of Abruzzo — from the Monti della Laga and the Gran Sasso to the Majella, the Parco Nazionale d'Abruzzo and the Alto Sangro — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          'The map divides the woods of Abruzzo into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from June to October: in summer the summer porcino in the oak, chestnut and lower beech woods, from September the beech porcino in the beech woods, which here climb to almost 1,900 metres, from the Laga to the Majella.',
        ovoli:
          'The map divides the woods of Abruzzo into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from August to October, in the chestnut, Turkey oak and downy oak woods below 900–1,200 metres, from the Monti della Laga to the Valle Roveto.',
        gallinacci:
          "The map divides the woods of Abruzzo into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from spring to late autumn: in the mountains from June to October in the beech and oak woods, from the Laga to the Parco Nazionale d'Abruzzo, and in the hills until December.",
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Abruzzo',
        porcini: 'Conditions index for porcini in Abruzzo',
        ovoli: 'Conditions index for ovoli in Abruzzo',
        gallinacci: 'Conditions index for gallinacci in Abruzzo',
      },
    },
  },
}
