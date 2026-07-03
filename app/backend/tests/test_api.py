"""API Tests. Die Steam Market API wird gemockt, damit die Tests
deterministisch und ohne Netzwerkzugriff laufen (wichtig für die CI)."""

import os
import tempfile

os.environ["DATABASE_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import pricesource  # noqa: E402
from database import init_db  # noqa: E402
from main import app  # noqa: E402

init_db()

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_steam_api(monkeypatch):
    """Ersetzt den echten Steam-API-Aufruf durch einen festen Preis.

    Dadurch machen die Tests keine Live-HTTP-Requests (4 Items x 5s Timeout
    würden die CI verlangsamen und flaky machen).
    """
    monkeypatch.setattr(pricesource, "_fetch_steam_price", lambda name: 42.0)


def test_healthz_returns_200():
    response = client.get("/healthz")
    assert response.status_code == 200


def test_ready_returns_200_or_503():
    response = client.get("/ready")
    assert response.status_code in (200, 503)


def test_refresh_returns_200():
    response = client.post("/api/prices/refresh")
    assert response.status_code == 200
    assert response.json()["fetched"] == len(pricesource.WATCHED_ITEMS)


def test_get_prices_returns_list():
    response = client.get("/api/prices")
    assert response.status_code == 200
    prices = response.json()["prices"]
    assert isinstance(prices, list)


def test_prices_use_mocked_steam_source():
    client.post("/api/prices/refresh")
    response = client.get("/api/prices")
    for entry in response.json()["prices"]:
        assert entry["price"] == 42.0
        assert entry["source"] == "steam"
