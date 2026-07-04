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

# Referenz auf die echte Parser-Funktion, bevor die autouse Fixture sie ersetzt
_REAL_FETCH_STEAM_PRICE = pricesource._fetch_steam_price


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


def test_ready_returns_200_when_db_ok():
    """Positivfall: initialisierte Datenbank ergibt 200."""
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_ready_returns_503_when_db_broken(monkeypatch):
    """Negativfall: kaputte Datenbankverbindung ergibt 503."""
    import main

    def broken_connection():
        raise RuntimeError("db down")

    monkeypatch.setattr(main, "check_connection", broken_connection)
    response = client.get("/ready")
    assert response.status_code == 503


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


def test_fallback_to_mock_when_steam_unavailable(monkeypatch):
    """Steam nicht erreichbar: Quelle wechselt auf Mock mit plausiblem Preis."""
    monkeypatch.setattr(pricesource, "_fetch_steam_price", lambda name: None)
    entries = pricesource.fetch_prices()
    assert len(entries) == len(pricesource.WATCHED_ITEMS)
    for entry in entries:
        assert entry.source == "mock"
        base = pricesource.WATCHED_ITEMS[entry.item_name]["base"]
        assert abs(entry.price - base) <= base * 0.05


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("CHF 141.87", 141.87),
        ("886.34 CHF", 886.34),
        ("1,234.56 CHF", 1234.56),
        ("CHF 42.--", 42.00),
    ],
)
def test_steam_price_parser_handles_chf_formats(monkeypatch, raw, expected):
    """Der Parser verarbeitet die bekannten CHF Formate der Steam API."""
    monkeypatch.setattr(pricesource, "_fetch_steam_price", _REAL_FETCH_STEAM_PRICE)
    payload = {"success": True, "lowest_price": raw}
    monkeypatch.setattr(
        pricesource.httpx, "get", lambda *a, **kw: _FakeResponse(payload)
    )
    assert pricesource._fetch_steam_price("egal") == expected


def test_steam_price_parser_returns_none_on_failure(monkeypatch):
    """success false oder Netzwerkfehler ergeben None (Fallback greift)."""
    monkeypatch.setattr(pricesource, "_fetch_steam_price", _REAL_FETCH_STEAM_PRICE)
    monkeypatch.setattr(
        pricesource.httpx,
        "get",
        lambda *a, **kw: _FakeResponse({"success": False}),
    )
    assert pricesource._fetch_steam_price("egal") is None

    def boom(*a, **kw):
        raise RuntimeError("network down")

    monkeypatch.setattr(pricesource.httpx, "get", boom)
    assert pricesource._fetch_steam_price("egal") is None


def test_refresh_writes_new_rows():
    """POST /api/prices/refresh schreibt pro Aufruf neue Datensätze."""
    item = next(iter(pricesource.WATCHED_ITEMS))

    def history_count() -> int:
        response = client.get("/api/prices/history", params={"item": item})
        return len(response.json()["history"])

    before = history_count()
    client.post("/api/prices/refresh")
    assert history_count() == before + 1


def test_history_grows_over_multiple_refreshes():
    """Der History Endpoint liefert nach mehreren Refreshs mehrere Einträge."""
    item = next(iter(pricesource.WATCHED_ITEMS))
    client.post("/api/prices/refresh")
    client.post("/api/prices/refresh")
    history = client.get("/api/prices/history", params={"item": item}).json()["history"]
    assert len(history) >= 2
    for entry in history:
        assert entry["item_name"] == item
