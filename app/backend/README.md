# Price Watch Backend

FastAPI Backend der Preisüberwachungs WebApp. Das Skelett wird in Sprint 1
(US04) aufgebaut. Fachliche Logik (Preisabruf, Persistenz) folgt in Sprint 2.

## Voraussetzungen

- Python 3.11 oder neuer
- pip

## Lokale Entwicklung

```bash
# In den Backend Ordner wechseln
cd app/backend

# Virtuelle Umgebung erstellen
python -m venv .venv

# Aktivieren (Linux, macOS, WSL)
source .venv/bin/activate

# Aktivieren (PowerShell auf Windows)
.venv\Scripts\Activate.ps1

# Abhängigkeiten installieren
pip install -r requirements.txt

# Entwicklungsserver starten mit Auto-Reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Der Server ist unter `http://localhost:8000` erreichbar. Die interaktive
OpenAPI Doku liegt unter `http://localhost:8000/docs`.

## Endpoints im Skelett

| Pfad | Methode | Beschreibung | Status |
| --- | --- | --- | --- |
| `/docs` | GET | OpenAPI Swagger UI | aktiv |
| `/healthz` | GET | Liveness Probe | aktiv |
| `/ready` | GET | Readiness Probe | aktiv |
| `/api/prices` | GET | Aktuelle Preise | Skelett (Sprint 2) |
| `/api/prices/history` | GET | Historische Preise | Skelett (Sprint 2) |

## Manueller Smoke Test

```bash
curl http://localhost:8000/healthz
# {"status":"ok"}

curl http://localhost:8000/ready
# {"status":"ready"}

curl http://localhost:8000/api/prices
# {"prices":[]}
```

## Tests

Automatisierte Tests werden in Sprint 2 zusammen mit der fachlichen Logik
ergänzt (siehe Sprint 2 Planung in `docs/dokumentation.md`).