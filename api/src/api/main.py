from fastapi import FastAPI

app = FastAPI(title="mushma API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
