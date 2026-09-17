"""Presence-only validation metrics.

A sighting says the species fruited in a cell on a day; nothing says where it did not. So each
sighting's score is compared with a **background** of cell-days it could have been instead, and the
AUC is the chance that the sighting outscores a background cell-day (ties count half). Averaging
the per-sighting AUCs over sightings gives an AUC stratified by sighting, which lets every sighting
bring its own background: the same day elsewhere, the same cell on other days.
"""

import numpy as np

from api.grid.cells import parse_cell_id


def presence_auc(score: float, background: np.ndarray, weights: np.ndarray | None = None) -> float:
    """Weighted share of the background scoring below ``score``, ties counting half."""
    background = np.asarray(background, dtype=float)
    weights = np.ones_like(background) if weights is None else np.asarray(weights, dtype=float)
    valid = ~np.isnan(background) & (weights > 0)
    if np.isnan(score) or not valid.any():
        return float("nan")
    background, weights = background[valid], weights[valid]
    below = weights[background < score].sum()
    tied = weights[background == score].sum()
    return float((below + 0.5 * tied) / weights.sum())


def lift(percentiles: np.ndarray, top: float) -> float:
    """How over-represented sightings are in the top ``top`` fraction of their background:
    the share of sightings at or above the ``1 - top`` percentile, divided by ``top``."""
    percentiles = np.asarray(percentiles, dtype=float)
    percentiles = percentiles[~np.isnan(percentiles)]
    if not len(percentiles):
        return float("nan")
    return float((percentiles >= 1 - top).mean() / top)


def bootstrap_interval(
    values: np.ndarray, level: float = 0.9, draws: int = 2000, seed: int = 0
) -> tuple[float, float]:
    """Percentile bootstrap interval of the mean over sightings."""
    values = np.asarray(values, dtype=float)
    values = values[~np.isnan(values)]
    if not len(values):
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    means = rng.choice(values, size=(draws, len(values)), replace=True).mean(axis=1)
    tail = (1 - level) / 2
    return float(np.quantile(means, tail)), float(np.quantile(means, 1 - tail))


def cell_centres_m(cell_ids: np.ndarray) -> np.ndarray:
    """``(cells, 2)`` EPSG:3035 centre coordinates from EEA grid cell codes."""
    parsed = [parse_cell_id(str(c)) for c in cell_ids]
    return np.array([(x + size / 2, y + size / 2) for x, y, size in parsed], dtype=float)


def cells_within(
    cell_id: str,
    cell_ids: np.ndarray,
    radius_km: float,
    centres: np.ndarray | None = None,
) -> np.ndarray:
    """Which of ``cell_ids`` lie within ``radius_km`` of ``cell_id`` (centre to centre), the cell
    itself excluded."""
    centres = cell_centres_m(cell_ids) if centres is None else centres
    x, y, size = parse_cell_id(cell_id)
    distance = np.hypot(centres[:, 0] - (x + size / 2), centres[:, 1] - (y + size / 2))
    return (distance <= radius_km * 1000) & (cell_ids != cell_id)
