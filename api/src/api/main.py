import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

app = FastAPI(
    title="mushma API",
    description=(
        "Fruiting-conditions scores, cell detail, hotspots and sightings for "
        "wild edible mushrooms in Tuscany. Scores are a 0-1 conditions index, "
        "never a probability or an edibility claim."
    ),
    version="0.1.0",
)
app.include_router(router)

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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
