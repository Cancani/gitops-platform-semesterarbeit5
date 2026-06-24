import os
import tempfile
from fastapi.testclient import TestClient

tmp = tempfile.mkdtemp()
os.environ["DATABASE_PATH"] = os.path.join(tmp, "test.db")

from main import app  # noqa: E402
from database import init_db  # noqa: E402

init_db()

client = TestClient(app)


def test_healthz_returns_200():
    response = client.get("/healthz")
    assert response.status_code == 200


def test_ready_returns_200_or_503():
    response = client.get("/ready")
    assert response.status_code in (200, 503)


def test_refresh_returns_200():
    response = client.post("/api/prices/refresh")
    assert response.status_code == 200
    assert "fetched" in response.json()


def test_get_prices_returns_list():
    response = client.get("/api/prices")
    assert response.status_code == 200
    assert isinstance(response.json()["prices"], list)
