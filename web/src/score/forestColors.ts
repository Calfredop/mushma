/**
 * Analysis mode's Bosco layer: one colour per forest type (habitat), in 5 families by broad
 * group (`api/src/api/config/habitats.yaml`), drawn on the map at full strength -- a cell's
 * forest type doesn't have a favourable/unfavourable direction the way a factor's value does, so
 * unlike `indicators.ts` there's no opacity-as-value here. Derivation and checks (Lago, the
 * Machado CVD simulation, the basemap): `.gavin-root/docs/visual-direction.md` -> Bosco layer.
 */

/** In the order the legend groups them. */
export const FOREST_GROUPS = [
  'broadleaf',
  'conifer',
  'mixed',
  'macchia',
  'transitional',
] as const
export type ForestGroup = (typeof FOREST_GROUPS)[number]

export interface ForestColor {
  group: ForestGroup
  color: string
}

const broadleaf = (color: string): ForestColor => ({ group: 'broadleaf', color })
const conifer = (color: string): ForestColor => ({ group: 'conifer', color })

/** Keyed by habitat id (`api/src/api/config/habitats.yaml`). */
export const FOREST_COLOR_BY_HABITAT: Readonly<Record<string, ForestColor>> = {
  beech: broadleaf('#A0C582'),
  chestnut: broadleaf('#8AAF6C'),
  deciduous_oak: broadleaf('#759958'),
  evergreen_oak: broadleaf('#618443'),
  mixed_broadleaf: broadleaf('#4D6F2F'),
  riparian: broadleaf('#3A5B19'),
  exotic_broadleaf: broadleaf('#284700'),

  mediterranean_pine: conifer('#38988E'),
  mountain_pine: conifer('#00736B'),
  fir_spruce: conifer('#004E48'),
  other_conifer: conifer('#002B27'),

  mixed_broadleaf_conifer: { group: 'mixed', color: '#223923' },
  macchia: { group: 'macchia', color: '#8E3B1C' },
  transitional_woodland_shrub: { group: 'transitional', color: '#D5D699' },
}

/** A habitat id the palette doesn't know yet still draws, in a neutral grey. */
export const NEUTRAL_FOREST_COLOR = '#7A827C'

export function forestColorOf(habitat: string): string {
  return FOREST_COLOR_BY_HABITAT[habitat]?.color ?? NEUTRAL_FOREST_COLOR
}

export function forestGroupOf(habitat: string): ForestGroup | undefined {
  return FOREST_COLOR_BY_HABITAT[habitat]?.group
}

/** Every known habitat, family-grouped, for the legend. */
export function forestHabitatsByGroup(): Record<ForestGroup, string[]> {
  const groups: Record<ForestGroup, string[]> = {
    broadleaf: [],
    conifer: [],
    mixed: [],
    macchia: [],
    transitional: [],
  }
  for (const [habitat, { group }] of Object.entries(FOREST_COLOR_BY_HABITAT)) {
    groups[group].push(habitat)
  }
  return groups
}
