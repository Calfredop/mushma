import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Trentino-Alto Adige: region #9 of the full-Italy rollout. Copy follows Tuscany's pattern with
 * the region's areas (the Val di Fiemme and Paneveggio forest, the Lagorai, Primiero, the Val di
 * Sole and Val di Non, the Val Pusteria, Val Venosta and Renon plateau in South Tyrol); seasons
 * from `.gavin-root/docs/species-ecology/trentino_alto_adige.md`.
 */
export const trentinoAltoAdige: RegionDefinition = {
  slug: 'trentino-alto-adige',
  name: { it: 'Trentino-Alto Adige', en: 'Trentino-South Tyrol' },
  whole: { it: 'Tutto il Trentino-Alto Adige', en: 'All of Trentino-South Tyrol' },
  bounds: [
    [10.38, 45.67],
    [12.48, 47.1],
  ],
  maxBounds: [
    [9.1, 44.9],
    [13.8, 47.8],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'trentino_alto_adige',
  wikidata: 'Q1237',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Trentino-Alto Adige',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Trentino-Alto Adige: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Trentino-Alto Adige: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Trentino-Alto Adige: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Trentino-Alto Adige: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Trentino-Alto Adige: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title:
            'Gallinacci in Trentino-Alto Adige: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Trentino-Alto Adige: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          'La mappa divide i boschi del Trentino-Alto Adige — dalle abetaie della Val di Fiemme, di Paneveggio e del Lagorai ai boschi della Valsugana, della Val di Non e della Val di Sole, fino alle peccete e alle pinete della Val Pusteria, della Valle Isarco e della Val Venosta — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.',
        porcini:
          'La mappa divide i boschi del Trentino-Alto Adige in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a ottobre: da metà luglio a fine settembre nei boschi di abete rosso e bianco fino a 1900 m, con il culmine in agosto in quota e in settembre più in basso, e da maggio a ottobre nelle pinete di pino silvestre.',
        ovoli:
          "La mappa divide i boschi del Trentino-Alto Adige in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui gli ovoli sono rari: la stagione va da giugno a ottobre, soprattutto da metà luglio a settembre, nei querceti e nelle pinete di pino silvestre dei versanti caldi sotto i 900 m, dall'Oltradige alla Valle dell'Adige e all'Alta Valsugana.",
        gallinacci:
          'La mappa divide i boschi del Trentino-Alto Adige in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre: nelle valli da giugno a ottobre, in montagna da luglio a metà settembre, soprattutto nei boschi di abete rosso fino a 1700 m, dalla Val Pusteria alle valli del Trentino.',
      },
      dataset: {
        region:
          'Indice delle condizioni per porcini, ovoli e gallinacci in Trentino-Alto Adige',
        porcini: 'Indice delle condizioni per i porcini in Trentino-Alto Adige',
        ovoli: 'Indice delle condizioni per gli ovoli in Trentino-Alto Adige',
        gallinacci: 'Indice delle condizioni per i gallinacci in Trentino-Alto Adige',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Trentino-South Tyrol',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Trentino-South Tyrol: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Trentino-South Tyrol: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Trentino-South Tyrol: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Trentino-South Tyrol: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Trentino-South Tyrol: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Trentino-South Tyrol: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Trentino-South Tyrol: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides Trentino-South Tyrol's woods — from the spruce and fir woods of the Val di Fiemme, Paneveggio and the Lagorai to the woods of the Valsugana, the Val di Non and the Val di Sole, and on to the spruce and pine woods of the Val Pusteria, the Valle Isarco and the Val Venosta — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides Trentino-South Tyrol's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to October: from mid-July to the end of September in the spruce and fir woods up to 1900 m, peaking in August up high and in September lower down, and from May to October in the Scots pine woods.",
        ovoli:
          "The map divides Trentino-South Tyrol's woods into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. Ovoli are rare here: the season runs from June to October, mostly from mid-July to September, in the oak and Scots pine woods of the warm slopes below 900 m, from the Oltradige to the Adige valley and the upper Valsugana.",
        gallinacci:
          "The map divides Trentino-South Tyrol's woods into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November: in the valleys from June to October, in the mountains from July to mid-September, mostly in the spruce woods up to 1700 m, from the Val Pusteria to the valleys of Trentino.",
      },
      dataset: {
        region:
          'Conditions index for porcini, ovoli and gallinacci in Trentino-South Tyrol',
        porcini: 'Conditions index for porcini in Trentino-South Tyrol',
        ovoli: 'Conditions index for ovoli in Trentino-South Tyrol',
        gallinacci: 'Conditions index for gallinacci in Trentino-South Tyrol',
      },
    },
  },
}
