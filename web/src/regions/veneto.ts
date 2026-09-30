import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Veneto: region #10 of the full-Italy rollout. Copy follows Tuscany's pattern with the region's
 * areas (the Dolomites of Belluno, the Asiago plateau, the Grappa, the Cansiglio and the Lessinia,
 * the Colli Euganei, the Colli Berici and the Montello); seasons from
 * `.gavin-root/docs/species-ecology/veneto.md`.
 */
export const veneto: RegionDefinition = {
  slug: 'veneto',
  name: { it: 'Veneto', en: 'Veneto' },
  whole: { it: 'Tutto il Veneto', en: 'All of Veneto' },
  bounds: [
    [10.62, 44.79],
    [13.11, 46.68],
  ],
  maxBounds: [
    [9.3, 44.0],
    [14.4, 47.4],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'veneto',
  wikidata: 'Q1243',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Veneto',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Veneto: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Veneto: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Veneto: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Veneto: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Veneto: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Veneto: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Veneto: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi del Veneto — dalle abetaie, dai lariceti e dalle faggete delle Dolomiti bellunesi, dal Cadore e dal Comelico all'Agordino e alla Val di Zoldo, all'Altopiano di Asiago, al Grappa, al Cansiglio e alla Lessinia, fino ai castagneti e ai querceti dei Colli Euganei, dei Colli Berici e del Montello — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi del Veneto in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre: da luglio a ottobre nei boschi di abete rosso, abete bianco e faggio delle Dolomiti, dell'Altopiano di Asiago e del Cansiglio, con il culmine da fine luglio a settembre, e fino a novembre sulle Prealpi basse e sui colli, dove in autunno nascono anche i porcini neri dei castagneti e dei querceti dei Colli Euganei e dei Berici.",
        ovoli:
          'La mappa divide i boschi del Veneto in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui gli ovoli sono rari: la stagione va da giugno a novembre, soprattutto da agosto a ottobre, nei castagneti e nei querceti sotto i 700 m, dai Colli Euganei e dai Berici alla pedemontana vicentina e trevigiana e al fondovalle della Valbelluna.',
        gallinacci:
          "La mappa divide i boschi del Veneto in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre: in montagna da giugno a ottobre, soprattutto nelle abetaie e nelle faggete del Bellunese, dell'Altopiano di Asiago e del Cansiglio, sulle Prealpi basse e sui colli da metà maggio a novembre.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Veneto',
        porcini: 'Indice delle condizioni per i porcini in Veneto',
        ovoli: 'Indice delle condizioni per gli ovoli in Veneto',
        gallinacci: 'Indice delle condizioni per i gallinacci in Veneto',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Veneto',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Veneto: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Veneto: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Veneto: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Veneto: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Veneto: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Veneto: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Veneto: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides Veneto's woods — from the spruce, larch and beech woods of the Belluno Dolomites, from Cadore and the Comelico to the Agordino and the Val di Zoldo, to the Asiago plateau, the Grappa, the Cansiglio and the Lessinia, and on to the chestnut and oak woods of the Colli Euganei, the Colli Berici and the Montello — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides Veneto's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November: from July to October in the spruce, fir and beech woods of the Dolomites, the Asiago plateau and the Cansiglio, peaking from late July to September, and into November on the lower Prealps and the hills, where autumn also brings the dark porcini of the chestnut and oak woods of the Colli Euganei and the Berici.",
        ovoli:
          "The map divides Veneto's woods into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. Ovoli are rare here: the season runs from June to November, mostly from August to October, in the chestnut and oak woods below 700 m, from the Colli Euganei and the Berici to the Vicenza and Treviso foothills and the floor of the Valbelluna.",
        gallinacci:
          "The map divides Veneto's woods into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November: in the mountains from June to October, mostly in the fir and beech woods of the Belluno area, the Asiago plateau and the Cansiglio, and on the lower Prealps and the hills from mid-May to November.",
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Veneto',
        porcini: 'Conditions index for porcini in Veneto',
        ovoli: 'Conditions index for ovoli in Veneto',
        gallinacci: 'Conditions index for gallinacci in Veneto',
      },
    },
  },
}
