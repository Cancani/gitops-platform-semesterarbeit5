"""
FastAPI Skelett der Preisüberwachungs WebApp (Sprint 1, US04).

Stand: Minimales Skelett mit Health Endpoints und Platzhalter API.
Echte Preisabruf- und Persistenzlogik folgt in Sprint 2.

Lokaler Start:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI

app = FastAPI(
    title="Price Watch API",
    description="Preisüberwachung für digitale Marktplatzobjekte",
    version="0.1.0",
)


@app.get("/healthz", tags=["health"])
def health_check() -> dict:
    """Liveness Probe.

    Antwortet, solange der Prozess lebt. Wird in Sprint 2 als Kubernetes
    Liveness Probe konfiguriert, damit abgestürzte Pods neu gestartet werden.
    """
    return {"status": "ok"}


@app.get("/ready", tags=["health"])
def readiness_check() -> dict:
    """Readiness Probe.

    Antwortet, sobald der Service Anfragen annehmen kann. Im Skelett
    immer "ready". In Sprint 2 wird hier zusätzlich die SQLite Verbindung
    geprüft (siehe ADR-003).
    """
    return {"status": "ready"}


@app.get("/api/prices", tags=["prices"])
def get_current_prices() -> dict:
    """Aktuelle Preise aller beobachteten Objekte.

    Skelett: liefert eine leere Liste. Die Datenabfrage aus SQLite
    folgt in Sprint 2.
    """
    return {"prices": []}


@app.get("/api/prices/history", tags=["prices"])
def get_price_history() -> dict:
    """Historische Preisdaten aller beobachteten Objekte.

    Skelett: liefert eine leere Liste. Die Historie wird in Sprint 2
    durch den Kubernetes CronJob befüllt, der die Preisquelle abruft.
    """
    return {"history": []}
# Kommentar für ci.yaml