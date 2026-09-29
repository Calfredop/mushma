import type { RegionDefinition } from './types.js'

/**
 * Valle d'Aosta: region #7 of the full-Italy rollout. Copy follows Tuscany's pattern with the
 * region's areas (the larch and spruce woods of the Valdigne, La Thuile and the Gran Paradiso
 * valleys, the Scots pine on the central valley's sunny side, the Val d'Ayas, the Valle di
 * Gressoney and the Bassa Valle's chestnut woods); seasons from
 * `.gavin-root/docs/species-ecology/valle_d_aosta.md`.
 *
 * No ovoli: the region has no record of them, so its rules have no ovoli group and `species`
 * leaves them out (`/valle-d-aosta/ovoli` is not a page). The type still asks for ovoli copy; it
 * is never served, and says why if it ever were.
 */
export const valleDAosta: RegionDefinition = {
  slug: 'valle-d-aosta',
  name: { it: "Valle d'Aosta", en: 'Aosta Valley' },
  locative: { it: "in Valle d'Aosta", en: 'in the Aosta Valley' },
  whole: { it: "Tutta la Valle d'Aosta", en: 'All of the Aosta Valley' },
  bounds: [
    [6.8, 45.46],
    [7.94, 45.99],
  ],
  maxBounds: [
    [5.8, 44.9],
    [8.9, 46.6],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: ['porcini', 'gallinacci'],
  apiRegionId: 'valle_d_aosta',
  wikidata: 'Q1222',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: "Mappa Funghi – porcini e gallinacci in Valle d'Aosta",
          description:
            "L'indice delle condizioni per porcini e gallinacci in Valle d'Aosta: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: "Porcini in Valle d'Aosta: indice delle condizioni | Mappa Funghi",
          description:
            "Dove e quando le condizioni favoriscono i porcini in Valle d'Aosta: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.",
        },
        ovoli: {
          title: "Ovoli in Valle d'Aosta | Mappa Funghi",
          description:
            "In Valle d'Aosta non ci sono segnalazioni di ovoli: la mappa della regione non dà un indice per gli ovoli.",
        },
        gallinacci: {
          title: "Gallinacci in Valle d'Aosta: indice delle condizioni | Mappa Funghi",
          description:
            "Dove e quando le condizioni favoriscono i gallinacci in Valle d'Aosta: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.",
        },
      },
      intro: {
        region:
          "La mappa divide i boschi della Valle d'Aosta — dai lariceti e dalle peccete della Valdigne, di La Thuile e delle valli del Gran Paradiso alle pinete di pino silvestre sul versante al sole della valle centrale, fino ai boschi della Val d'Ayas e della Valle di Gressoney e ai castagneti della Bassa Valle — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi della Valle d'Aosta in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre: da fine luglio a ottobre nelle peccete e nelle abetine fino a 1900 metri, con il culmine tra agosto e settembre, da maggio nelle pinete di pino silvestre e fino a novembre nei boschi della Bassa Valle.",
        ovoli:
          "In Valle d'Aosta non ci sono segnalazioni di ovoli, né nei castagneti e nei querceti della Bassa Valle né altrove: per questo la mappa della regione dà un indice solo per porcini e gallinacci.",
        gallinacci:
          "La mappa divide i boschi della Valle d'Aosta in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da maggio a novembre: in montagna da giugno a ottobre nelle peccete, nelle abetine e nelle faggete fino a 1850 metri, più in basso, nei boschi della Bassa Valle, da metà maggio a novembre.",
      },
      dataset: {
        region: "Indice delle condizioni per porcini e gallinacci in Valle d'Aosta",
        porcini: "Indice delle condizioni per i porcini in Valle d'Aosta",
        ovoli: "Nessun indice per gli ovoli in Valle d'Aosta",
        gallinacci: "Indice delle condizioni per i gallinacci in Valle d'Aosta",
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini and gallinacci in the Aosta Valley',
          description:
            'The conditions index for porcini and gallinacci in the Aosta Valley: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in the Aosta Valley: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in the Aosta Valley: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in the Aosta Valley | Mappa Funghi',
          description:
            'There are no records of ovoli in the Aosta Valley: the map gives no ovoli index for this region.',
        },
        gallinacci: {
          title: 'Gallinacci in the Aosta Valley: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in the Aosta Valley: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          "The map divides the Aosta Valley's woods — from the larch and spruce woods of the Valdigne, La Thuile and the Gran Paradiso valleys to the Scots pine woods on the central valley's sunny side, and on to the woods of the Val d'Ayas and the Valle di Gressoney and the chestnut woods of the Bassa Valle — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.",
        porcini:
          "The map divides the Aosta Valley's woods into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November: from late July to October in the spruce and fir woods up to 1900 m, peaking in August and September, from May in the Scots pine woods, and until November in the woods of the Bassa Valle.",
        ovoli:
          'There are no records of ovoli in the Aosta Valley, neither in the chestnut and oak woods of the Bassa Valle nor elsewhere: so the map gives this region a score for porcini and gallinacci only.',
        gallinacci:
          "The map divides the Aosta Valley's woods into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from May to November: in the mountains from June to October in the spruce, fir and beech woods up to 1850 m, and lower down, in the woods of the Bassa Valle, from mid-May to November.",
      },
      dataset: {
        region: 'Conditions index for porcini and gallinacci in the Aosta Valley',
        porcini: 'Conditions index for porcini in the Aosta Valley',
        ovoli: 'No ovoli index in the Aosta Valley',
        gallinacci: 'Conditions index for gallinacci in the Aosta Valley',
      },
    },
  },
}
