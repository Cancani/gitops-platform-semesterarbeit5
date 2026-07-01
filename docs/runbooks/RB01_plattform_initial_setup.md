## Runbook 01: Plattform Initial Setup

**Zweck**

Dieses Runbook beschreibt den vollständigen Aufbau der Plattform ab einem leeren Rechner
bis zu einem laufenden kind-Cluster mit Argo CD und der price-watch Applikation.

**Voraussetzungen**

- Docker Desktop installiert und gestartet
- kind installiert (`winget install kind` oder via Binary)
- kubectl installiert
- helm installiert
- Git installiert
- Repository geklont: `git clone https://github.com/Cancani/gitops-platform-semesterarbeit5`

**Schritte**

1. Cluster erstellen

```bash
bash scripts/setup-cluster.sh
```

Prüfen ob der Cluster läuft:

```bash
kubectl cluster-info --context kind-kind
```

2. Argo CD installieren

```bash
bash scripts/setup-argocd.sh
```

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

Command für Passwort ausführen.

3. Argo CD UI erreichbar machen

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

UI erreichbar unter `https://localhost:8080`. Login: `admin` / Passwort aus Schritt 2.

4. price-watch Applikation registrieren

```bash
kubectl apply -f app/argocd/price-watch.app.yaml
```

5. Sync abwarten

In der Argo CD UI erscheint die Applikation `price-watch` und wechselt nach ca. 30 Sekunden
auf `Synced` und `Healthy`.

6. Applikation im Browser öffnen

Die Applikation ist direkt über NodePort erreichbar, kein Port-Forward nötig:

`http://localhost:30080`

**Erfolgskriterium**

- Argo CD UI zeigt `price-watch` als `Synced` und `Healthy`
- `http://localhost:30080` zeigt die price-watch Weboberfläche
- `kubectl get pods` zeigt einen laufenden Pod
