from fastapi import FastAPI

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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
