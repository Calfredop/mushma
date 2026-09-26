"""Which regions the API serves: configured, with stores on disk, and with species rules."""

from pathlib import Path

import pytest

import api.regions as regions


def _stores(root: Path, region_id: str) -> None:
    (root / "grid" / region_id).mkdir(parents=True)
    (root / "grid" / region_id / "cells.parquet").write_bytes(b"")
    (root / "scores" / region_id).mkdir(parents=True)
    (root / "scores" / region_id / "meta.json").write_text("{}")


def test_a_region_with_stores_but_no_rules_is_not_served(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A region's config can reach main before its rules do (umbria.yaml did), and its stores can
    # reach the server before either: serving it would make /regions and /overview raise.
    monkeypatch.setattr(regions, "list_configured_regions", lambda: ["ghost", "tuscany"])
    monkeypatch.setattr(regions, "list_rule_regions", lambda: ["tuscany"])
    _stores(tmp_path, "ghost")
    _stores(tmp_path, "tuscany")

    assert regions.list_served_region_ids(tmp_path) == ["tuscany"]
