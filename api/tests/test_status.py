from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_status_in_fixture_mode() -> None:
    response = client.get("/status")
    assert response.status_code == 200
    body = response.json()
    assert body["rules_version"] == "fixtures"
    assert body["updated_at"] is not None
