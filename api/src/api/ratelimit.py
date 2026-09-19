"""Per-IP rate limiting for the public, GET-only, cookie-less API (see the CORS comment in
main.py): protects the single small Fly machine (``min_machines_running = 0``, no Redis) from a
runaway client. In-memory (``limits``' moving-window strategy) is enough at this scale, and
simply resets on redeploy/restart -- an acceptable tradeoff for a hobby-scale app.

A plain ASGI middleware rather than a Starlette ``BaseHTTPMiddleware`` (which the `slowapi`
package builds on): ``BaseHTTPMiddleware`` reconstructs every response as a stream, which drops
the `Content-Length` `api.main`'s `GZipMiddleware` relies on to skip small responses (verified:
it broke tests/test_compression.py's tiny-response case). This middleware never touches the
response for a request under the limit -- it forwards ``send`` untouched -- so it can't do that.

``/health`` and ``/status`` are exempt: Fly's own health checks and any uptime pinger must never
be throttled. Disabled entirely under ``MUSHMA_FIXTURES=1`` (dev, CI and the contract test suite,
which shares one client "IP" across hundreds of requests a second -- nothing a real deployment
would ever see from one visitor, so there's nothing to protect there).
"""

import os

from limits import RateLimitItemPerMinute
from limits.storage import MemoryStorage
from limits.strategies import MovingWindowRateLimiter
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

DEFAULT_LIMIT_PER_MINUTE = 60
EXEMPT_PATHS = frozenset({"/health", "/status"})


def client_ip(request: Request) -> str:
    """Fly's edge sets `Fly-Client-IP`; `X-Forwarded-For`'s first hop is the fallback for any
    other proxy, and the raw socket address for local dev with no proxy in front at all."""
    fly_ip = request.headers.get("fly-client-ip")
    if fly_ip:
        return fly_ip
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


class RateLimitMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        *,
        per_minute: int = DEFAULT_LIMIT_PER_MINUTE,
        exempt_paths: frozenset[str] = EXEMPT_PATHS,
    ) -> None:
        self.app = app
        self.limit = RateLimitItemPerMinute(per_minute)
        self.exempt_paths = exempt_paths
        self._strategy = MovingWindowRateLimiter(MemoryStorage())

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if (
            scope["type"] != "http"
            or scope["path"] in self.exempt_paths
            or os.environ.get("MUSHMA_FIXTURES") == "1"
        ):
            await self.app(scope, receive, send)
            return
        key = client_ip(Request(scope))
        if self._strategy.hit(self.limit, key):
            await self.app(scope, receive, send)
            return
        response = JSONResponse(
            {"error": f"Rate limit exceeded: {self.limit.amount} per minute"}, status_code=429
        )
        await response(scope, receive, send)
