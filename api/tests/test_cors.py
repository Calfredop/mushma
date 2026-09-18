from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestCors:
    def test_allows_a_vercel_production_domain(self) -> None:
        response = client.get("/health", headers={"Origin": "https://mushma.vercel.app"})
        assert response.headers["access-control-allow-origin"] == "https://mushma.vercel.app"

    def test_allows_a_vercel_preview_domain(self) -> None:
        origin = "https://mushma-web-git-feature-x-someteam.vercel.app"
        response = client.get("/health", headers={"Origin": origin})
        assert response.headers["access-control-allow-origin"] == origin

    def test_allows_localhost_for_dev(self) -> None:
        response = client.get("/health", headers={"Origin": "http://localhost:5173"})
        assert response.headers["access-control-allow-origin"] == "http://localhost:5173"

    def test_rejects_an_unrelated_origin(self) -> None:
        response = client.get("/health", headers={"Origin": "https://evil.example.com"})
        assert "access-control-allow-origin" not in response.headers

    def test_preflight_allows_get(self) -> None:
        response = client.options(
            "/scores",
            headers={
                "Origin": "https://mushma.vercel.app",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert response.headers["access-control-allow-origin"] == "https://mushma.vercel.app"
