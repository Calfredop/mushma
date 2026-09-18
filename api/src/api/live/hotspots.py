"""Cluster adjacent, above-threshold woodland cells into hotspots.

Fixture mode's proximity clustering (``api.fixtures.hotspots``) was an explicit stand-in for this
("needs the M2 grid's cell adjacency"). Now that cells exist, adjacency is exact rather than a
radius guess: a cell id encodes its ``(x_min, y_min)`` corner (``api.grid.cells``), so two cells
are neighbors iff they share an edge on the 1 km grid. Clusters are the connected components of
cells scoring at or above ``threshold``.
"""

from dataclasses import dataclass

import pandas as pd

from api.grid.cells import parse_cell_id

# Where a cell-day is "worth a special mention" on the map -- API aggregation, not a species rule,
# so it needs no citation, just this comment: high enough that "hotspots" stays a short list even
# on a strong day, low enough that a middling season still has somewhere to point to.
DEFAULT_SCORE_THRESHOLD = 0.5


@dataclass(frozen=True)
class HotspotCluster:
    cell_ids: list[str]
    score: float
    comune: str
    nearest_place: str
    lon: float
    lat: float


def cluster_hotspots(
    cells: pd.DataFrame,
    *,
    threshold: float = DEFAULT_SCORE_THRESHOLD,
    limit: int = 10,
) -> list[HotspotCluster]:
    """``cells`` has one row per scored woodland cell: ``cell_id, x_min, y_min, lon, lat,
    comune_name, place_name, score``. Clusters are ranked by their top cell's score, descending,
    and capped at ``limit``; each is labelled by its top cell's place."""
    hot = cells[cells["score"] >= threshold]
    if hot.empty:
        return []

    size = parse_cell_id(hot.iloc[0]["cell_id"])[2]
    corners = {(int(row.x_min), int(row.y_min)): row.cell_id for row in hot.itertuples()}
    by_id = hot.set_index("cell_id")

    visited: set[str] = set()
    components: list[list[str]] = []
    for start_id in corners.values():
        if start_id in visited:
            continue
        visited.add(start_id)
        stack, component = [start_id], []
        while stack:
            current = stack.pop()
            component.append(current)
            x, y, _ = parse_cell_id(current)
            for neighbor_corner in ((x + size, y), (x - size, y), (x, y + size), (x, y - size)):
                neighbor = corners.get(neighbor_corner)
                if neighbor is not None and neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        components.append(component)

    clusters = []
    for component in components:
        rows = by_id.loc[component]
        top = rows.loc[rows["score"].idxmax()]
        clusters.append(
            HotspotCluster(
                cell_ids=sorted(component),
                score=float(top["score"]),
                comune=top["comune_name"],
                nearest_place=top["place_name"],
                lon=float(rows["lon"].mean()),
                lat=float(rows["lat"].mean()),
            )
        )
    clusters.sort(key=lambda c: c.score, reverse=True)
    return clusters[:limit]
