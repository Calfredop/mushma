"""api.live.hotspots: connected components of adjacent, above-threshold woodland cells."""

import pandas as pd

from api.grid.cells import cell_id as make_cell_id
from api.live.hotspots import cluster_hotspots

SIZE = 1000


def _cell(x: int, y: int, score: float, comune: str = "Comune", place: str = "Place") -> dict:
    return {
        "cell_id": make_cell_id(x, y, SIZE),
        "x_min": x,
        "y_min": y,
        "lon": x / 100_000,  # arbitrary but distinct, deterministic
        "lat": y / 100_000,
        "comune_name": comune,
        "place_name": place,
        "score": score,
    }


def _df(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


class TestClusterHotspots:
    def test_edge_adjacent_hot_cells_join_one_cluster(self) -> None:
        rows = [
            _cell(0, 0, 0.9, comune="Top", place="TopPlace"),
            _cell(SIZE, 0, 0.8),
            _cell(0, SIZE, 0.7),
        ]
        clusters = cluster_hotspots(_df(rows), threshold=0.5)
        assert len(clusters) == 1
        assert set(clusters[0].cell_ids) == {row["cell_id"] for row in rows}
        assert clusters[0].score == 0.9
        assert clusters[0].comune == "Top"
        assert clusters[0].nearest_place == "TopPlace"

    def test_diagonal_only_cells_stay_separate(self) -> None:
        rows = [_cell(0, 0, 0.9), _cell(SIZE, SIZE, 0.85)]
        clusters = cluster_hotspots(_df(rows), threshold=0.5)
        assert len(clusters) == 2
        assert {len(c.cell_ids) for c in clusters} == {1}

    def test_below_threshold_cells_are_dropped_and_never_bridge_clusters(self) -> None:
        rows = [
            _cell(0, 0, 0.9),
            _cell(SIZE, 0, 0.2),  # below threshold: dropped, doesn't bridge
            _cell(2 * SIZE, 0, 0.8),
        ]
        clusters = cluster_hotspots(_df(rows), threshold=0.5)
        assert len(clusters) == 2
        for cluster in clusters:
            assert len(cluster.cell_ids) == 1

    def test_ranked_by_top_cell_score_descending(self) -> None:
        rows = [
            _cell(0, 0, 0.6),
            _cell(10 * SIZE, 0, 0.95),
            _cell(20 * SIZE, 0, 0.75),
        ]
        clusters = cluster_hotspots(_df(rows), threshold=0.5)
        assert [c.score for c in clusters] == [0.95, 0.75, 0.6]

    def test_limit_caps_the_result(self) -> None:
        rows = [_cell(i * 10 * SIZE, 0, 0.5 + i * 0.01) for i in range(5)]
        clusters = cluster_hotspots(_df(rows), threshold=0.5, limit=2)
        assert len(clusters) == 2
        assert clusters[0].score >= clusters[1].score

    def test_no_cells_above_threshold_returns_no_clusters(self) -> None:
        rows = [_cell(0, 0, 0.1), _cell(SIZE, 0, 0.2)]
        assert cluster_hotspots(_df(rows), threshold=0.5) == []

    def test_centroid_is_the_mean_of_the_cluster_cells(self) -> None:
        rows = [_cell(0, 0, 0.9), _cell(SIZE, 0, 0.8)]
        clusters = cluster_hotspots(_df(rows), threshold=0.5)
        expected_lon = (rows[0]["lon"] + rows[1]["lon"]) / 2
        assert clusters[0].lon == expected_lon
