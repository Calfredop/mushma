from api.fixtures.cells import CELLS
from api.fixtures.hotspots import build_hotspots


class TestBuildHotspots:
    def test_ranked_descending_by_score(self) -> None:
        cell_scores = [(cell, float(i)) for i, cell in enumerate(CELLS)]
        hotspots = build_hotspots(cell_scores, limit=10)
        scores = [h.score for h in hotspots]
        assert scores == sorted(scores, reverse=True)

    def test_respects_the_limit(self) -> None:
        cell_scores = [(cell, 1.0) for cell in CELLS]
        hotspots = build_hotspots(cell_scores, limit=3)
        assert len(hotspots) <= 3

    def test_every_hotspot_references_real_cells_with_the_top_score(self) -> None:
        cell_scores = [(cell, float(i % 5)) for i, cell in enumerate(CELLS)]
        hotspots = build_hotspots(cell_scores, limit=10)
        for hotspot in hotspots:
            assert len(hotspot.cell_ids) >= 1
            member_scores = [score for cell, score in cell_scores if cell.id in hotspot.cell_ids]
            assert hotspot.score == max(member_scores)

    def test_far_apart_top_cells_form_separate_hotspots(self) -> None:
        # Amiata (south) and Casentino (north-east) are ~150 km apart
        amiata = next(c for c in CELLS if c.comune == "Piancastagnaio")
        casentino = next(c for c in CELLS if c.comune == "Poppi")
        cell_scores = [(c, 1.0 if c.id in (amiata.id, casentino.id) else 0.1) for c in CELLS]
        hotspots = build_hotspots(cell_scores, limit=10)
        top_two_ids = {hotspots[0].id, hotspots[1].id}
        assert len(top_two_ids) == 2
