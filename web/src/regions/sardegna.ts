import { SPECIES } from '../state/urlState.js'
import type { RegionDefinition } from './types.js'

/**
 * Sardegna: region #19 of the full-Italy rollout. Copy follows Tuscany's pattern with the
 * Sardinian woods (the Gallura and the Limbara, the Alà plateau, the Barbagia and the
 * Gennargentu, the Marghine and the Montiferru, the Sulcis-Iglesiente and the Sette Fratelli);
 * seasons from `.gavin-root/docs/species-ecology/sardegna.md`. The bounds take in the small
 * islands (La Maddalena, the Asinara, San Pietro and Sant'Antioco).
 */
export const sardegna: RegionDefinition = {
  slug: 'sardegna',
  name: { it: 'Sardegna', en: 'Sardinia' },
  whole: { it: 'Tutta la Sardegna', en: 'All of Sardinia' },
  bounds: [
    [8.13, 38.85],
    [9.83, 41.32],
  ],
  maxBounds: [
    [6.9, 38.05],
    [11.05, 42.1],
  ],
  minZoom: 6,
  maxZoom: 15,
  species: [...SPECIES],
  apiRegionId: 'sardegna',
  wikidata: 'Q1462',
  historyStart: '2016-01-01',
  copy: {
    it: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli e gallinacci in Sardegna',
          description:
            "L'indice delle condizioni per porcini, ovoli e gallinacci in Sardegna: meteo, bosco e quota aggiornati ogni giorno, cella per cella da 1 km.",
        },
        porcini: {
          title: 'Porcini in Sardegna: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i porcini in Sardegna: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        ovoli: {
          title: 'Ovoli in Sardegna: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono gli ovoli in Sardegna: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
        gallinacci: {
          title: 'Gallinacci in Sardegna: indice delle condizioni | Mappa Funghi',
          description:
            'Dove e quando le condizioni favoriscono i gallinacci in Sardegna: pioggia, temperatura e tipo di bosco aggiornati ogni giorno su una mappa a celle da 1 km.',
        },
      },
      intro: {
        region:
          "La mappa divide i boschi della Sardegna — dalle sugherete della Gallura e dell'altopiano di Alà ai boschi della Barbagia e del Gennargentu, fino al Montiferru, al Sulcis-Iglesiente e ai Sette Fratelli — in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per porcini, ovoli e gallinacci: più è alto, più meteo e bosco sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. Qui ogni cella mostra la specie con le condizioni migliori; scegli una specie per vedere la sua stagione e cosa pesa sul suo indice.",
        porcini:
          "La mappa divide i boschi della Sardegna in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i porcini: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione ha due tempi: da aprile a giugno nella macchia e nei querceti di collina; poi, dopo l'estate secca, dalla prima buona pioggia d'autunno fino a dicembre, con il culmine a novembre, nelle sugherete della Gallura e del Limbara, nei boschi della Barbagia e del Gennargentu fra Desulo, Tonara e Fonni, sul Montiferru, nel Marghine e sui Sette Fratelli.",
        ovoli:
          "La mappa divide i boschi della Sardegna in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per gli ovoli: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va da fine maggio a dicembre, soprattutto in autunno, nelle sugherete e nei querceti della Gallura fra Tempio Pausania, Aggius e Calangianus, sull'altopiano di Alà e nelle leccete dei Sette Fratelli e di Castiadas.",
        gallinacci:
          "La mappa divide i boschi della Sardegna in celle di 1 km e dà a ognuna un indice delle condizioni da 0 a 1 per i gallinacci: più è alto, più meteo, bosco e quota sono adatti in quel giorno. Mostra dove le condizioni sono buone, non dove si trovano i funghi. La stagione va dalla primavera all'inverno, soprattutto da ottobre a dicembre e, negli inverni miti, fino a febbraio: nelle sugherete e nelle leccete della Gallura fra Tempio Pausania, Aggius e Padru, sul Montiferru e sul Monte Arci.",
      },
      dataset: {
        region: 'Indice delle condizioni per porcini, ovoli e gallinacci in Sardegna',
        porcini: 'Indice delle condizioni per i porcini in Sardegna',
        ovoli: 'Indice delle condizioni per gli ovoli in Sardegna',
        gallinacci: 'Indice delle condizioni per i gallinacci in Sardegna',
      },
    },
    en: {
      seo: {
        region: {
          title: 'Mappa Funghi – porcini, ovoli and gallinacci in Sardinia',
          description:
            'The conditions index for porcini, ovoli and gallinacci in Sardinia: weather, woodland and elevation, updated daily, cell by cell.',
        },
        porcini: {
          title: 'Porcini in Sardinia: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour porcini in Sardinia: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        ovoli: {
          title: 'Ovoli in Sardinia: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour ovoli in Sardinia: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
        gallinacci: {
          title: 'Gallinacci in Sardinia: conditions index | Mappa Funghi',
          description:
            'Where and when conditions favour gallinacci in Sardinia: rain, temperature and woodland type, updated daily on a 1 km grid.',
        },
      },
      intro: {
        region:
          'The map divides the woods of Sardinia — from the cork-oak woods of the Gallura and the Alà plateau to the woods of the Barbagia and the Gennargentu, and on to the Montiferru, the Sulcis-Iglesiente and the Sette Fratelli — into 1 km cells and gives each one a conditions score from 0 to 1 for porcini, ovoli and gallinacci: the higher it is, the better the weather and woods suit them on that day. It shows where conditions are good, not where the mushrooms are. Here each cell shows the species with the best conditions; pick a species to see its season and what weighs on its score.',
        porcini:
          'The map divides the woods of Sardinia into 1 km cells and gives each one a conditions score from 0 to 1 for porcini: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season comes in two parts: from April to June in the macchia and the oak woods of the hills; then, after the dry summer, from the first good autumn rain into December, peaking in November, in the cork-oak woods of the Gallura and the Limbara, the woods of the Barbagia and the Gennargentu around Desulo, Tonara and Fonni, on the Montiferru, in the Marghine and on the Sette Fratelli.',
        ovoli:
          'The map divides the woods of Sardinia into 1 km cells and gives each one a conditions score from 0 to 1 for ovoli: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from late May to December, mostly in autumn, in the cork-oak and oak woods of the Gallura around Tempio Pausania, Aggius and Calangianus, on the Alà plateau and in the holm-oak woods of the Sette Fratelli and Castiadas.',
        gallinacci:
          'The map divides the woods of Sardinia into 1 km cells and gives each one a conditions score from 0 to 1 for gallinacci: the higher it is, the better the weather, woods and altitude suit them on that day. It shows where conditions are good, not where the mushrooms are. The season runs from spring into winter, mostly from October to December and, in mild winters, into February: in the cork-oak and holm-oak woods of the Gallura around Tempio Pausania, Aggius and Padru, on the Montiferru and on Monte Arci.',
      },
      dataset: {
        region: 'Conditions index for porcini, ovoli and gallinacci in Sardinia',
        porcini: 'Conditions index for porcini in Sardinia',
        ovoli: 'Conditions index for ovoli in Sardinia',
        gallinacci: 'Conditions index for gallinacci in Sardinia',
      },
    },
  },
}
