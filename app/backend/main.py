"""
FastAPI Backend der Preisüberwachungs WebApp.

Echte Anwendungslogik mit Pydantic Modellen, SQLite Persistenz, Preisquelle
und ausgeliefertem Frontend.

Lokaler Start:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from database import (
    check_connection,
    get_latest_prices,
    get_price_history,
    init_db,
    insert_prices,
)
from models import HistoryResponse, PricesResponse, RefreshResponse
from pricesource import fetch_prices

STATIC_DIR = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Beim Start die Datenbank initialisieren (Tabelle anlegen)
    init_db()
    yield


app = FastAPI(
    title="Price Watch API",
    description="Preisüberwachung für digitale Marktplatzobjekte",
    version="0.3.0",
    lifespan=lifespan,
)


@app.get("/healthz", tags=["health"])
def health_check() -> dict:
    """Liveness Probe: antwortet, solange der Prozess lebt."""
    return {"status": "ok"}


@app.get("/ready", tags=["health"])
def readiness_check() -> dict:
    """Readiness Probe: prüft zusätzlich die Datenbankverbindung."""
    try:
        check_connection()
    except Exception:
        raise HTTPException(status_code=503, detail="database not ready")
    return {"status": "ready"}


@app.get("/api/prices", tags=["prices"], response_model=PricesResponse)
def get_current_prices() -> dict:
    """Aktuelle Preise aller beobachteten Objekte (neuster Wert pro Objekt)."""
    return {"prices": get_latest_prices()}


@app.get("/api/prices/history", tags=["prices"], response_model=HistoryResponse)
def price_history(item: str | None = None) -> dict:
    """Historische Preisdaten, optional gefiltert nach Objekt via ?item=..."""
    return {"history": get_price_history(item)}


@app.post("/api/prices/refresh", tags=["prices"], response_model=RefreshResponse)
def refresh_prices() -> dict:
    """Ruft aktuelle Preise ab und speichert sie.

    Wird vom Kubernetes CronJob regelmässig aufgerufen.
    Manuell nutzbar für Tests und Demo.
    """
    entries = fetch_prices()
    insert_prices(entries)
    return {"fetched": len(entries)}

app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
