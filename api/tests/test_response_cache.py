"""Server-side response cache: hit until data is recalculated, then miss."""

from __future__ import annotations

import json

import pytest

from api.response_cache import MemoryBackend, NullBackend, ResponseCache, reset_cache_for_tests


@pytest.fixture(autouse=True)
def _reset_cache() -> None:
    reset_cache_for_tests()


def test_null_backend_never_hits() -> None:
    cache = ResponseCache(NullBackend())
    cache.set("tuscany", "scores", {"cells": [1]}, species="porcini", date="2026-09-28")
    assert cache.get("tuscany", "scores", species="porcini", date="2026-09-28") is None


def test_stores_and_returns_a_payload() -> None:
    cache = ResponseCache(MemoryBackend())
    payload = {"cells": [{"cell_id": "a", "score": 0.7}]}
    cache.set("tuscany", "scores", payload, species="porcini", date="2026-09-28")
    assert cache.get("tuscany", "scores", species="porcini", date="2026-09-28") == payload


def test_different_params_are_different_keys() -> None:
    cache = ResponseCache(MemoryBackend())
    cache.set("tuscany", "scores", {"a": 1}, species="porcini", date="2026-09-28")
    assert cache.get("tuscany", "scores", species="ovoli", date="2026-09-28") is None


def test_bump_invalidates_previous_entries() -> None:
    cache = ResponseCache(MemoryBackend())
    cache.set("tuscany", "scores", {"v": 1}, species="porcini", date="2026-09-28")
    cache.bump("tuscany")
    assert cache.get("tuscany", "scores", species="porcini", date="2026-09-28") is None


def test_bump_is_per_region() -> None:
    cache = ResponseCache(MemoryBackend())
    cache.set("tuscany", "scores", {"v": 1}, species="porcini", date="2026-09-28")
    cache.set("umbria", "scores", {"v": 1}, species="porcini", date="2026-09-28")
    cache.bump("tuscany")
    assert cache.get("tuscany", "scores", species="porcini", date="2026-09-28") is None
    assert cache.get("umbria", "scores", species="porcini", date="2026-09-28") == {"v": 1}


def test_national_entries_use_a_shared_generation() -> None:
    cache = ResponseCache(MemoryBackend())
    cache.set("_", "overview", {"regions": []}, species="combined", date="2026-09-28")
    cache.bump("_")
    assert cache.get("_", "overview", species="combined", date="2026-09-28") is None


def test_set_after_bump_stores_under_the_new_generation() -> None:
    cache = ResponseCache(MemoryBackend())
    cache.set("tuscany", "scores", {"v": 1}, species="porcini", date="2026-09-28")
    cache.bump("tuscany")
    cache.set("tuscany", "scores", {"v": 2}, species="porcini", date="2026-09-28")
    assert cache.get("tuscany", "scores", species="porcini", date="2026-09-28") == {"v": 2}


def test_params_are_stable_regardless_of_order() -> None:
    cache = ResponseCache(MemoryBackend())
    cache.set("tuscany", "hotspots", {"n": 1}, date="2026-09-28", limit=10, species="porcini")
    assert cache.get("tuscany", "hotspots", species="porcini", limit=10, date="2026-09-28") == {
        "n": 1
    }


def test_payload_round_trips_through_json() -> None:
    # Redis stores bytes; the memory backend mirrors that so we catch non-JSON types early.
    cache = ResponseCache(MemoryBackend())
    payload = {"score": 0.5, "date": "2026-09-28", "ok": True, "n": None}
    cache.set("tuscany", "status", payload)
    got = cache.get("tuscany", "status")
    assert got == payload
    assert json.dumps(got, sort_keys=True) == json.dumps(payload, sort_keys=True)
