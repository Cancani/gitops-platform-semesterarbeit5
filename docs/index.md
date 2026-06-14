<div align="center">

GitOps Plattform mit Preisüberwachungs WebApp, Cloud Native Deployment auf Kubernetes mit Helm, Argo CD und GitHub Actions

<p>
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/3.12-blue?style=for-the-badge" alt="3.12" />
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
<img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes" />
<img src="https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white" alt="Helm" />
<img src="https://img.shields.io/badge/Argo_CD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white" alt="Argo CD" />
<img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions" />
<img src="https://img.shields.io/badge/GitOps-F05032?style=for-the-badge&logo=git&logoColor=white" alt="GitOps" />
</p>

</div>

---

## Dokumentation

Die laufende Projektdokumentation ist auf GitHub Pages verfügbar:

**GitHub Pages:** [https://cancani.com/gitops-platform-sem5/](https://cancani.com/gitops-platform-sem5/)

| Dokument | Inhalt |
| --- | --- |
| [Dokumentation](dokumentation.md) | Hauptdokument, alle Kapitel von Management Summary bis Reflexion |
| Runbook 01: Plattform Initial Setup | Cluster und Argo CD initial aufbauen (folgt in Sprint 3, US13) |
| Runbook 02: Neue Version deployen | Standard GitOps Release Workflow (folgt in Sprint 3, US13) |
| Runbook 03: Rollback Release | Rollback eines fehlerhaften Releases (folgt in Sprint 3, US13) |

---

## Kurzbeschreibung

Containerisierte Anwendungen werden in vielen Umgebungen noch manuell oder nur teilweise automatisiert bereitgestellt. Deployments sind dadurch schwer nachvollziehbar, Rollbacks nicht sauber definiert und der Soll Zustand der Anwendung ist nicht zentral versioniert.

Diese Semesterarbeit baut eine kleine, aber realistische Cloud Native Plattform auf Kubernetes auf. Der Soll Zustand wird im Git Repository gepflegt. Argo CD synchronisiert ihn automatisch in den Cluster. Eine Preisüberwachungs WebApp dient als realistischer Workload und ist bewusst einfach gehalten. Der Fokus der Arbeit liegt auf Plattform, GitOps, Helm und CI Pipeline.

---

## Sprint Status

| Sprint | Wochen | Sprint Ziel | Status |
| --- | --- | --- | --- |
| Sprint 1 | 1 bis 3 | Setup, Cluster, WebApp Skelett, Container | ![status](https://img.shields.io/badge/done-brightgreen?style=flat-square) |
| Sprint 2 | 4 bis 6 | GitOps Durchstich (CI, Helm, Argo CD) | ![status](https://img.shields.io/badge/done-brightgreen?style=flat-square) |
| Sprint 3 | 7 bis 9 | Stabilisierung, Runbooks, Doku, Demo | ![status](https://img.shields.io/badge/in__progress-yellow?style=flat-square) |

---

## Architektur auf einen Blick

```mermaid
flowchart LR
    Dev[Entwickler] -->|git push| Repo[(GitHub Repository)]
    Repo -->|Trigger| CI[GitHub Actions CI]
    CI -->|Build und Push| Reg[(GitHub Container Registry)]
    Repo -->|Helm Chart Pfad| Argo[Argo CD]
    Argo -->|kubectl apply, Sync| K8s[(Kubernetes Cluster)]
    Reg -->|Image Pull| K8s
    K8s --> App[Preisüberwachungs WebApp]
    App --> DB[(SQLite)]
    App -->|HTTPS| User[Benutzer]
```

---

## Tech Stack

| Bereich | Technologie |
| --- | --- |
| Cluster | kind (Kubernetes in Docker) |
| Orchestrierung | Kubernetes |
| Paketierung | Helm |
| GitOps | Argo CD |
| CI Pipeline | GitHub Actions |
| Container Build | Docker |
| Registry | GitHub Container Registry (ghcr.io) |
| Backend | Python 3.12, FastAPI |
| Frontend | minimales HTML mit Chart.js |
| Datenbank | SQLite (PVC folgt in Sprint 3) |
| Job Scheduling | Kubernetes CronJob für regelmässigen Preisabruf (folgt in Sprint 3) |
| Quelle Preisdaten | Mock Preisquelle mit echten Steam CDN Bildern, echte API folgt |
| Doku | MkDocs Material auf GitHub Pages |

---

## GitOps Workflow

Änderungen am Deployment erfolgen ausschliesslich über Commits im Git Repository. Es wird nicht direkt im Cluster konfiguriert.

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Entwickler
    participant Git as GitHub
    participant CI as GitHub Actions
    participant Reg as GHCR
    participant Argo as Argo CD
    participant K8s as Kubernetes

    Dev->>Git: git push (Code oder Helm Werte)
    Git->>CI: trigger workflow
    CI->>CI: Build, Test, Lint
    CI->>Reg: docker push image:tag
    Argo->>Git: poll oder webhook
    Argo->>K8s: apply Manifeste aus Helm Chart
    K8s->>Reg: pull image
    K8s-->>Argo: Status Healthy
    Argo-->>Dev: sichtbar im Argo CD UI
```

---

## Repository Struktur

```
.
├── README.md                       # Repository Einstieg
├── mkdocs.yml                      # MkDocs Material Konfiguration
├── docs/                           # gesamte Doku, wird zur Pages Seite
│   ├── index.md                    # diese Startseite
│   ├── dokumentation.md            # Hauptdokument der Semesterarbeit
│   ├── runbooks/                   # drei Runbooks (folgt Sprint 3)
│   └── img/                        # Screenshots und Abbildungen
├── app/
│   └── backend/                    # FastAPI Service: API, Preisabruf, DB Zugriff
│       ├── main.py                 # FastAPI Anwendung
│       ├── database.py             # SQLite Datenzugriff
│       ├── models.py               # Pydantic Modelle
│       ├── pricesource.py          # Preisquelle (Mock mit Steam CDN Bildern)
│       ├── requirements.txt        # Python Abhängigkeiten
│       ├── Dockerfile              # Multi-Stage Container Build
│       └── static/                 # Frontend (index.html mit Chart.js)
├── helm/
│   └── price-watch/                # Helm Chart der WebApp
├── app/argocd/
│   └── price-watch.app.yaml        # Argo CD Application Definition
├── kind/
│   └── cluster.yaml                # kind Cluster Konfiguration
├── .github/
│   ├── workflows/
│   │   ├── ci.yaml                 # Build und Push in Registry
│   │   └── docs.yaml               # MkDocs Build und Pages Deploy
│   └── ISSUE_TEMPLATE/             # User Story Templates
└── scripts/
    ├── setup-cluster.sh            # kind Cluster aufsetzen
    ├── setup-argocd.sh             # Argo CD installieren
    └── teardown-cluster.sh         # Cluster abbauen
```

---

## Quick Start, lokales Setup

Voraussetzungen: Docker, kubectl, Helm, kind, Git.

```bash
# 1. Repository klonen
git clone https://github.com/Cancani/gitops-platform-semesterarbeit5.git
cd gitops-platform-semesterarbeit5

# 2. Lokalen Cluster bauen
bash scripts/setup-cluster.sh
kubectl get nodes                     # erwartet: 2 Nodes Ready

# 3. Argo CD installieren
bash scripts/setup-argocd.sh

# 4. Argo CD Application registrieren
kubectl apply -f app/argocd/price-watch.app.yaml

# 5. Argo CD UI aufrufen (Port Forward offen lassen)
kubectl port-forward svc/argocd-server -n argocd 8080:443
# Browser: https://localhost:8080

# 6. Status prüfen
kubectl get application -n argocd price-watch
kubectl get pods
```

---

## Referenzprojekt aus früherer Semesterarbeit

Die 4. Semesterarbeit ist als Referenzprojekt verlinkt und dient als Nachweis für vorhandene Erfahrung mit strukturierter Projektdokumentation, CI/CD, Docker und Microservice Architektur.

- **Dokumentation Sem 4:** [https://cancani.com/geraeteausleihe-sem4/dokumentation/](https://cancani.com/geraeteausleihe-sem4/dokumentation/)
- **Projektseite Sem 4:** [https://cancani.com/geraeteausleihe-sem4](https://cancani.com/geraeteausleihe-sem4)

Die neue Semesterarbeit ist keine Wiederholung, sondern eine fachliche Erweiterung in Richtung Kubernetes, GitOps, Helm, Argo CD und Cloud Native Plattform Engineering. Details und Lerntransfer sind in der [Dokumentation](dokumentation.md) im Abschnitt Reflexion beschrieben.

---

## Autor und Rahmen

| Feld | Wert |
| --- | --- |
| Autor | Efekan Demirci |
| Klasse | ITCNE24 |
| Schule | Technische Berufsschule Zürich TBZ, Höhere Fachschule |
| Semester | 5 |
| Fachexperte IaCA, CNC, CNA | Marcel Bernet |
| Fachexperte PRJ | Thanam Pangri |
| Module | Projektmanagement, IaCA, CNC und CNA, optional DevOps |
| Geplanter Aufwand | ca. 50 Stunden über 9 Wochen |
| Repository | [github.com/Cancani/gitops-platform-semesterarbeit5](https://github.com/Cancani/gitops-platform-semesterarbeit5) |
