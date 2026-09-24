/**
 * API responses → GeoJSON for MapLibre. Coordinates are [lon, lat] (WGS84).
 *
 * The contract gives each cell's centre, not its polygon, so the map draws a
 * square of the cell's size around it. If M4 changes how the grid is
 * delivered, this is the one module to change.
 */
import type { Feature, FeatureCollection, Point, Polygon, Position } from 'geojson'
import type { components } from '../api/schema'

type GridCellScore = components['schemas']['GridCellScore']
type CellFactors = components['schemas']['CellFactors']
type SightingCount = components['schemas']['SightingCount']

/** Anything with a cell centre: a score, a factor row. */
export interface CellCentre {
  cell_id: string
  lon: number
  lat: number
}

export interface CellProperties {
  cell_id: string
  score: number
}

/** Analysis mode: each factor's 0–1 value under its id; a factor the cell lacks is absent. */
export type FactorProperties = { cell_id: string } & Record<string, number | string>

export interface SightingProperties {
  cell_id: string
  count: number
}

const KM_PER_DEGREE_LAT = 111.32

export function cellSquare(lon: number, lat: number, sizeKm: number): Position[][] {
  const halfLat = sizeKm / 2 / KM_PER_DEGREE_LAT
  const halfLon = sizeKm / 2 / (KM_PER_DEGREE_LAT * Math.cos((lat * Math.PI) / 180))
  const west = lon - halfLon
  const east = lon + halfLon
  const south = lat - halfLat
  const north = lat + halfLat
  return [
    [
      [west, south],
      [east, south],
      [east, north],
      [west, north],
      [west, south],
    ],
  ]
}

export function cellsToPoints(
  cells: GridCellScore[],
): FeatureCollection<Point, CellProperties> {
  return {
    type: 'FeatureCollection',
    features: cells.map((cell): Feature<Point, CellProperties> => ({
      type: 'Feature',
      id: cell.cell_id,
      geometry: { type: 'Point', coordinates: [cell.lon, cell.lat] },
      properties: { cell_id: cell.cell_id, score: cell.score },
    })),
  }
}

export function cellsToSquares(
  cells: GridCellScore[],
  sizeKm = 1,
): FeatureCollection<Polygon, CellProperties> {
  return {
    type: 'FeatureCollection',
    features: cells.map((cell): Feature<Polygon, CellProperties> => ({
      type: 'Feature',
      id: cell.cell_id,
      geometry: { type: 'Polygon', coordinates: cellSquare(cell.lon, cell.lat, sizeKm) },
      properties: { cell_id: cell.cell_id, score: cell.score },
    })),
  }
}

/** Bosco layer: a cell's dominant forest type, keyed by cell_id. Static -- doesn't vary by
 * species or day, unlike the factor values, so it's merged in rather than fetched per cell row. */
export type ForestTypesByCell = ReadonlyMap<string, string>

function factorProperties(
  cell: CellFactors,
  ids: readonly string[],
  forestTypes: ForestTypesByCell | undefined,
): FactorProperties {
  const properties: FactorProperties = { cell_id: cell.cell_id }
  cell.values.forEach((value, i) => {
    if (value !== null && ids[i] !== undefined) properties[ids[i]] = value
  })
  const forestType = forestTypes?.get(cell.cell_id)
  if (forestType !== undefined) properties.forest_type = forestType
  return properties
}

/** `ids` are the response's factor ids, in the order of each cell's `values`. */
export function factorCellsToPoints(
  cells: CellFactors[],
  ids: readonly string[],
  forestTypes?: ForestTypesByCell,
): FeatureCollection<Point, FactorProperties> {
  return {
    type: 'FeatureCollection',
    features: cells.map((cell): Feature<Point, FactorProperties> => ({
      type: 'Feature',
      id: cell.cell_id,
      geometry: { type: 'Point', coordinates: [cell.lon, cell.lat] },
      properties: factorProperties(cell, ids, forestTypes),
    })),
  }
}

export function factorCellsToSquares(
  cells: CellFactors[],
  ids: readonly string[],
  sizeKm = 1,
  forestTypes?: ForestTypesByCell,
): FeatureCollection<Polygon, FactorProperties> {
  return {
    type: 'FeatureCollection',
    features: cells.map((cell): Feature<Polygon, FactorProperties> => ({
      type: 'Feature',
      id: cell.cell_id,
      geometry: { type: 'Polygon', coordinates: cellSquare(cell.lon, cell.lat, sizeKm) },
      properties: factorProperties(cell, ids, forestTypes),
    })),
  }
}

/** Total sightings per cell across every response (species) and source. */
export function sightingsByCell(
  responses: { counts: SightingCount[] }[],
): Map<string, number> {
  const totals = new Map<string, number>()
  for (const { counts } of responses) {
    for (const { cell_id, count } of counts) {
      totals.set(cell_id, (totals.get(cell_id) ?? 0) + count)
    }
  }
  return totals
}

/** One point per cell at the cell centre (PRD → Sightings privacy: counts per cell only). */
export function sightingsToPoints(
  totals: Map<string, number>,
  cells: readonly CellCentre[],
): FeatureCollection<Point, SightingProperties> {
  const features: Feature<Point, SightingProperties>[] = []
  for (const cell of cells) {
    const count = totals.get(cell.cell_id)
    if (!count) continue
    features.push({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [cell.lon, cell.lat] },
      properties: { cell_id: cell.cell_id, count },
    })
  }
  return { type: 'FeatureCollection', features }
}
