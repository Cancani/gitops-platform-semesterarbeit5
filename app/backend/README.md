# Price Watch Backend

FastAPI Backend der Preisüberwachungs WebApp. Preisabruf über die Steam
Market API mit Mock-Fallback, Persistenz in SQLite, ausgeliefertes
Frontend unter `/`.

## Voraussetzungen

- Python 3.12 (oder 3.11+)
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

## Endpoints

| Pfad | Methode | Beschreibung |
| --- | --- | --- |
| `/` | GET | Frontend (index.html mit Chart.js) |
| `/docs` | GET | OpenAPI Swagger UI |
| `/healthz` | GET | Liveness Probe |
| `/ready` | GET | Readiness Probe (inkl. DB-Check) |
| `/api/prices` | GET | Aktuelle Preise (neuster Wert pro Objekt) |
| `/api/prices/history` | GET | Historische Preise, optional `?item=...` |
| `/api/prices/refresh` | POST | Preise abrufen und speichern (CronJob) |

## Manueller Smoke Test

```bash
curl http://localhost:8000/healthz
# {"status":"ok"}

curl http://localhost:8000/ready
# {"status":"ready"}

curl -X POST http://localhost:8000/api/prices/refresh
# {"fetched":4}

curl http://localhost:8000/api/prices
# {"prices":[...]}
```

## Tests

```bash
pip install pytest httpx
pytest
```

Die Tests mocken die Steam Market API (kein Netzwerkzugriff nötig) und
verwenden eine temporäre SQLite Datenbank.
