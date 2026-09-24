import os

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from api.ratelimit import RateLimitMiddleware
from api.regions import RegionNotServed
from api.routes import region_problem, router

# Error tracking (M7 · production hardening): only when a DSN is set, so local dev, CI and
# fixtures mode need no Sentry project at all. Sampling stays low/zero to stay well inside the
# free tier at this app's scale.
if os.environ.get("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        traces_sample_rate=0.0,
        send_default_pii=False,
    )

app = FastAPI(
    title="mushma API",
    description=(
        "Fruiting-conditions scores, cell detail, hotspots and sightings for "
        "wild edible mushrooms across served Italian regions. Scores are a 0-1 "
        "conditions index, never a probability or an edibility claim. Every data "
        "route takes a `region` query parameter (default `tuscany`)."
    ),
    version="0.1.0",
)
app.include_router(router)


@app.exception_handler(RegionNotServed)
async def _region_not_served(_request: Request, exc: RegionNotServed):
    return region_problem(exc)


app.add_middleware(RateLimitMiddleware)

# The web app (M5) is a static SPA on Vercel: any of its preview deployments and its production
# domain must be able to call this read-only, GET-only, cookie-less API. CORS_ORIGINS lets a
# custom production domain (once one exists) be allowed without a redeploy; local dev origins are
# included so `pnpm dev` works against a local `fastapi dev` without extra config.
DEFAULT_CORS_ORIGINS = "http://localhost:5173,http://localhost:4173"
CORS_ORIGINS = [
    origin for origin in os.environ.get("CORS_ORIGINS", DEFAULT_CORS_ORIGINS).split(",") if origin
]
CORS_ORIGIN_REGEX = os.environ.get("CORS_ORIGIN_REGEX", r"^https://.*\.vercel\.app$")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# The grids (/scores, /history/season/{year}) are ~11k cells of JSON: about 0.8 MB raw and a
# sixth of that gzipped (PRD -> Architecture -> Grid delivery). Caddy in front of it
# (deploy/Caddyfile) doesn't compress, so the API does.
app.add_middleware(GZipMiddleware, minimum_size=1024)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
