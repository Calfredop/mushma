"""Greedy proximity clustering of scored fixture cells into hotspots.

Stands in for M4-api.md's real "cluster of adjacent high-scoring cells" (which
needs the M2 grid's cell adjacency); here cells within `cluster_radius_km` of
a cluster's top-scoring cell join it.
"""

import math
from dataclasses import dataclass

from api.fixtures.cells import CellSpec

DEFAULT_CLUSTER_RADIUS_KM = 18.0
EARTH_RADIUS_KM = 6371.0


@dataclass(frozen=True)
class HotspotCluster:
    id: str
    cell_ids: list[str]
    score: float
    comune: str
    nearest_place: str
    lon: float
    lat: float


def _haversine_km(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(d_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(a))


def build_hotspots(
    cell_scores: list[tuple[CellSpec, float]],
    *,
    cluster_radius_km: float = DEFAULT_CLUSTER_RADIUS_KM,
    limit: int = 10,
) -> list[HotspotCluster]:
    ranked = sorted(cell_scores, key=lambda cs: cs[1], reverse=True)
    clusters: list[list[tuple[CellSpec, float]]] = []
    for cell, score in ranked:
        for cluster in clusters:
            top_cell, _ = cluster[0]
            if _haversine_km(cell.lon, cell.lat, top_cell.lon, top_cell.lat) <= cluster_radius_km:
                cluster.append((cell, score))
                break
        else:
            clusters.append([(cell, score)])

    hotspots = []
    for i, cluster in enumerate(clusters[:limit]):
        top_cell, top_score = cluster[0]
        hotspots.append(
            HotspotCluster(
                id=f"hotspot-{i + 1}",
                cell_ids=[cell.id for cell, _ in cluster],
                score=top_score,
                comune=top_cell.comune,
                nearest_place=top_cell.nearest_place,
                lon=sum(cell.lon for cell, _ in cluster) / len(cluster),
                lat=sum(cell.lat for cell, _ in cluster) / len(cluster),
            )
        )
    return hotspots
