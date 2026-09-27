import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Friuli-Venezia Giulia: region #11 of the full-Italy rollout. Copy follows Tuscany's pattern with
 * the region's areas (Carnia and the Tarvisio forest, the Carnic and Julian Prealps from the Val
 * Cellina to the Valli del Natisone, the Collio and the eastern hills, the Karst); seasons from
 * `.gavin-root/docs/species-ecology/friuli_venezia_giulia.md`.
 */
export const friuliVeneziaGiulia: RegionDefinition = {
  slug: 'friuli-venezia-giulia',
  name: { it: 'Friuli-Venezia Giulia', en: 'Friuli-Venezia Giulia' },
  whole: { it: 'Tutto il Friuli-Venezia Giulia', en: 'All of Friuli-Venezia Giulia' },
  bounds: [
    [12.32, 45.58],
    [13.92, 46.65],
  ],
  maxBounds: [
    [11.0, 44.8],
    [15.2, 47.4],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'friuli_venezia_giulia',
  wikidata: 'Q1250',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Friuli-Venezia Giulia',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Friuli-Venezia Giulia: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title:
            'Porcini in Friuli-Venezia Giulia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Friuli-Venezia Giulia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Friuli-Venezia Giulia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Friuli-Venezia Giulia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title:
            'Gallinacci in Friuli-Venezia Giulia: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Friuli-Venezia Giulia: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          'La mappa divide i boschi del Friuli-Venezia Giulia — dalle abetaie e dalle faggete della Carnia e della Foresta di Tarvisio alle Prealpi Carniche e Giulie, dalla Val Cellina alle Valli del Natisone, fino ai castagneti del Collio e dei colli orientali e ai boschi del Carso — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.',
        porcini:
          'La mappa divide i boschi del Friuli-Venezia Giulia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre: da luglio a metà ottobre nei boschi di abete rosso, abete bianco e faggio della Carnia, del Tarvisiano e delle Alpi Giulie, con il culmine in agosto e settembre, e fino a novembre in collina e sul Carso, dove in ottobre nascono soprattutto i porcini neri dei querceti.',
        ovoli:
          'La mappa divide i boschi del Friuli-Venezia Giulia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui gli ovoli sono rari: la stagione va da giugno a novembre, soprattutto da agosto a ottobre, nei querceti e nei castagneti sotto i 650 m, dal Carso triestino ai colli di Cividale, alle colline moreniche e alla pedemontana pordenonese.',
        gallinacci:
          'La mappa divide i boschi del Friuli-Venezia Giulia in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre: in montagna da giugno a ottobre, soprattutto nei boschi di abete e faggio della Carnia e delle Alpi Giulie, in collina e sul Carso da metà giugno a ottobre nei querceti.',
      },
      dataset: {
        region:
          'Indice delle condizioni per porcini, ovoli e gallinacci in Friuli-Venezia Giulia',
        porcini: 'Indice delle condizioni per i porcini in Friuli-Venezia Giulia',
        ovoli: 'Indice delle condizioni per gli ovoli in Friuli-Venezia Giulia',
        gallinacci: 'Indice delle condizioni per i gallinacci in Friuli-Venezia Giulia',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Friuli-Venezia Giulia',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Friuli-Venezia Giulia: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Friuli-Venezia Giulia: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Friuli-Venezia Giulia: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Friuli-Venezia Giulia: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Friuli-Venezia Giulia: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Friuli-Venezia Giulia: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Friuli-Venezia Giulia: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides Friuli-Venezia Giulia's woods — from the spruce, fir and beech woods of Carnia and the Tarvisio forest to the Carnic and Julian Prealps, from the Val Cellina to the Valli del Natisone, and on to the chestnut woods of the Collio and the eastern hills and the woods of the Karst — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides Friuli-Venezia Giulia's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November: from July to mid-October in the spruce, fir and beech woods of Carnia, the Tarvisio area and the Julian Alps, peaking in August and September, and into November in the hills and on the Karst, where October brings mostly the dark porcini of the oak woods.",
        ovoli:
          "The map divides Friuli-Venezia Giulia's woods into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. Ovoli are rare here: the season runs from June to November, mostly from August to October, in the oak and chestnut woods below 650 m, from the Trieste Karst to the hills of Cividale, the moraine hills and the Pordenone foothills.",
        gallinacci:
          "The map divides Friuli-Venezia Giulia's woods into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November: in the mountains from June to October, mostly in the fir and beech woods of Carnia and the Julian Alps, and in the hills and on the Karst from mid-June to October in the oak woods.",
      },
      dataset: {
        region:
          'Conditions index for porcini, ovoli and gallinacci in Friuli-Venezia Giulia',
        porcini: 'Conditions index for porcini in Friuli-Venezia Giulia',
        ovoli: 'Conditions index for ovoli in Friuli-Venezia Giulia',
        gallinacci: 'Conditions index for gallinacci in Friuli-Venezia Giulia',
      },
    },
  },
}
