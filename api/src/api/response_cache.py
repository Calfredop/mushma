"""Origin response cache backed by Redis.

Caches serialized JSON bodies for the expensive GET routes. Keys include a per-region
generation counter, so a successful data recalculation only needs to ``INCR`` that counter —
old entries become unreachable and fall out under Redis LRU. No TTL as the primary
invalidation: the daily job (and any other writer that finishes a recompute) bumps the
generation.

``REDIS_URL`` unset → a no-op cache (local ``fastapi dev``, CI fixtures, unit tests that don't
opt in). The daily oneshot container shares the compose network with Redis, so it can bump
before ``ExecStartPost`` restarts the API.
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from typing import Protocol
from urllib.parse import urlparse

from pydantic import BaseModel

REDIS_URL_ENV = "REDIS_URL"
KEY_PREFIX = "mushma:v1"
GEN_PREFIX = "mushma:gen"
# National routes (/regions, /overview) that aren't scoped to one region.
NATIONAL_REGION = "_"

_cache: ResponseCache | None = None


class CacheBackend(Protocol):
    def get(self, key: str) -> bytes | None: ...

    def set(self, key: str, value: bytes) -> None: ...

    def incr(self, key: str) -> int: ...


class NullBackend:
    """Always misses; set/incr are no-ops. Used when REDIS_URL is unset."""

    def get(self, key: str) -> bytes | None:
        return None

    def set(self, key: str, value: bytes) -> None:
        return None

    def incr(self, key: str) -> int:
        return 0


class MemoryBackend:
    """In-process store for tests. Mirrors Redis: values are bytes, INCR is a byte integer."""

    def __init__(self) -> None:
        self._data: dict[str, bytes] = {}

    def get(self, key: str) -> bytes | None:
        return self._data.get(key)

    def set(self, key: str, value: bytes) -> None:
        self._data[key] = value

    def incr(self, key: str) -> int:
        current = int(self._data.get(key, b"0"))
        new = current + 1
        self._data[key] = str(new).encode()
        return new


class RedisBackend:
    def __init__(self, url: str) -> None:
        # Imported lazily so local/CI without redis-py still import this module when REDIS_URL
        # is unset (NullBackend). Production image always has the package.
        import redis

        self._client = redis.Redis.from_url(url, decode_responses=False)

    def get(self, key: str) -> bytes | None:
        value = self._client.get(key)
        return value if isinstance(value, (bytes, type(None))) else bytes(value)

    def set(self, key: str, value: bytes) -> None:
        self._client.set(key, value)

    def incr(self, key: str) -> int:
        return int(self._client.incr(key))


class ResponseCache:
    def __init__(self, backend: CacheBackend) -> None:
        self._backend = backend

    def get(self, region: str, name: str, **params: object) -> dict | None:
        raw = self._backend.get(self._entry_key(region, name, params))
        if raw is None:
            return None
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
        return payload if isinstance(payload, dict) else None

    def set(self, region: str, name: str, payload: dict, **params: object) -> None:
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
        self._backend.set(self._entry_key(region, name, params), body)

    def bump(self, region: str) -> int:
        """Invalidate every cached response for ``region`` (or ``NATIONAL_REGION``)."""
        return self._backend.incr(self._gen_key(region))

    def _generation(self, region: str) -> int:
        raw = self._backend.get(self._gen_key(region))
        if raw is None:
            return 0
        try:
            return int(raw)
        except (TypeError, ValueError):
            return 0

    def _entry_key(self, region: str, name: str, params: dict[str, object]) -> str:
        gen = self._generation(region)
        param_part = _stable_params(params)
        return f"{KEY_PREFIX}:{region}:{gen}:{name}:{param_part}"

    @staticmethod
    def _gen_key(region: str) -> str:
        return f"{GEN_PREFIX}:{region}"


def _stable_params(params: dict[str, object]) -> str:
    parts = []
    for key in sorted(params):
        value = params[key]
        if value is None:
            continue
        parts.append(f"{key}={value}")
    return "&".join(parts)


def _backend_from_env() -> CacheBackend:
    url = os.environ.get(REDIS_URL_ENV, "").strip()
    if not url:
        return NullBackend()
    # Reject nonsense early so a typo shows up at startup rather than on the first request.
    parsed = urlparse(url)
    if parsed.scheme not in {"redis", "rediss"}:
        raise ValueError(f"{REDIS_URL_ENV} must be a redis:// or rediss:// URL, got {url!r}")
    return RedisBackend(url)


def get_cache() -> ResponseCache:
    global _cache
    if _cache is None:
        _cache = ResponseCache(_backend_from_env())
    return _cache


def bump_region(region: str) -> int:
    """Bump one region's generation (and the national key, so /overview refreshes too)."""
    cache = get_cache()
    gen = cache.bump(region)
    if region != NATIONAL_REGION:
        cache.bump(NATIONAL_REGION)
    return gen


def cached_model[T: BaseModel](
    region: str,
    name: str,
    model: type[T],
    compute: Callable[[], T],
    **params: object,
) -> T:
    """Return a cached Pydantic response, or compute, store and return it."""
    cache = get_cache()
    key_params = {key: _param_value(value) for key, value in params.items()}
    hit = cache.get(region, name, **key_params)
    if hit is not None:
        return model.model_validate(hit)
    result = compute()
    cache.set(region, name, result.model_dump(mode="json"), **key_params)
    return result


def _param_value(value: object) -> object:
    if hasattr(value, "isoformat"):
        return value.isoformat()  # type: ignore[no-any-return]
    return value


def reset_cache_for_tests(backend: CacheBackend | None = None) -> ResponseCache:
    """Replace the process singleton. Tests only."""
    global _cache
    _cache = ResponseCache(backend if backend is not None else NullBackend())
    return _cache
