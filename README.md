<div align="center">

# GitOps Plattform mit Preisüberwachungs WebApp

**Cloud Native Deployment auf Kubernetes mit Helm, Argo CD und GitHub Actions**

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

Die vollständige Projektdokumentation ist auf GitHub Pages verfügbar:

**GitHub Pages:** [https://cancani.com/gitops-platform-semesterarbeit5/](https://cancani.com/gitops-platform-semesterarbeit5/)

| Dokument | Inhalt |
| --- | --- |
| [Dokumentation](./docs/dokumentation.md) | Hauptdokument, alle Kapitel von Management Summary bis Reflexion |
| [Einreichungsformular](./docs/ITCNE24_Semesterarbeit-5_GitOps_Platform.pdf) | Ursprüngliche Projekteingabe der Semesterarbeit (PDF) |
| [Runbook 01: Plattform Initial Setup](docs/runbooks/RB01_plattform_initial_setup.md) | Cluster und Argo CD initial aufbauen |
| [Runbook 02: Neue Version deployen](docs/runbooks/RB02_neue_version_deployen.md) | Standard GitOps Release Workflow |
| [Runbook 03: Rollback Release](docs/runbooks/RB03_rollback_release.md) | Rollback eines fehlerhaften Releases |

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
| Sprint 3 | 7 bis 9 | Stabilisierung, Runbooks, Doku, Demo | ![status](https://img.shields.io/badge/done-brightgreen?style=flat-square) |

---

## Architektur auf einen Blick

```mermaid
flowchart LR
    Dev[Entwickler] -->|git push| Repo[(GitHub Repository)]
    Repo -->|Trigger| CI[GitHub Actions CI]
    CI -->|Build und Push| Reg[(GHCR)]
    CI -->|values.yaml Update| Repo
    Repo -->|Helm Chart Pfad| Argo[Argo CD]
    Argo -->|Sync| K8s[(Kubernetes Cluster)]
    Reg -->|Image Pull| K8s
    K8s --> App[Preisüberwachungs WebApp]
    App --> DB[(SQLite)]
    App -->|HTTP, NodePort 30080| User[Benutzer]
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
| Datenbank | SQLite mit PVC |
| Job Scheduling | Kubernetes CronJob für regelmässigen Preisabruf |
| Preisdaten | Steam Market API mit Mock-Fallback |
| Doku | MkDocs Material auf GitHub Pages |

---

## GitOps Workflow

Änderungen am Deployment erfolgen ausschliesslich über Commits im Git Repository. Es wird nicht direkt im Cluster konfiguriert.

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Entwickler
    participant Git as GitHub Repository
    participant CI as GitHub Actions
    participant Reg as GHCR
    participant Argo as Argo CD
    participant K8s as Kubernetes

    Dev->>Git: git push (Code oder Helm Werte)
    Git->>CI: trigger lint-and-test
    CI->>CI: ruff, pytest, helm lint, helm template
    CI->>CI: build-and-push, nur wenn lint-and-test grün
    CI->>Reg: docker push image, sha-Tag und latest
    CI->>Git: values.yaml Update, Commit mit skip ci
    Argo->>Git: Polling auf Änderung
    Argo->>K8s: apply Manifeste aus Helm Chart
    K8s->>Reg: pull image
    K8s-->>Argo: Status Healthy
    Argo-->>Dev: sichtbar im Argo CD UI
```

---

## Repository Struktur

```
.
├── README.md
├── mkdocs.yml
├── docs/
│   ├── index.md
│   ├── dokumentation.md
│   └── runbooks/
│       ├── RB01_plattform_initial_setup.md
│       ├── RB02_neue_version_deployen.md
│       └── RB03_rollback_release.md
├── app/
│   ├── argocd/
│   │   └── price-watch.app.yaml
│   └── backend/
│       ├── main.py
│       ├── models.py
│       ├── database.py
│       ├── pricesource.py
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── pyproject.toml
│       ├── static/
│       │   └── index.html
│       └── tests/
│           └── test_api.py
├── helm/
│   └── price-watch/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── _helpers.tpl
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── configmap.yaml
│           ├── pvc.yaml
│           └── cronjob.yaml
├── kind/
│   └── cluster.yaml
├── scripts/
│   ├── setup-cluster.sh
│   ├── setup-argocd.sh
│   └── teardown-cluster.sh
└── .github/
    └── workflows/
        ├── ci.yaml
        └── docs.yaml
```

---

## Quick Start, lokales Setup

Voraussetzungen: Docker Desktop, kubectl, Helm, kind, Git.

```bash
# 1. Repository klonen
git clone https://github.com/Cancani/gitops-platform-semesterarbeit5.git
cd gitops-platform-semesterarbeit5

# 2. Cluster erstellen
bash scripts/setup-cluster.sh

# 3. Argo CD installieren
bash scripts/setup-argocd.sh

# 4. price-watch App registrieren
kubectl apply -f app/argocd/price-watch.app.yaml

# 5. Argo CD UI erreichbar machen
kubectl port-forward svc/argocd-server -n argocd 8080:443

# 6. App im Browser öffnen, direkt über NodePort erreichbar
# http://localhost:30080
```

Eine vollständige Anleitung mit Screenshots befindet sich in [RB-01: Plattform Initial Setup](docs/runbooks/RB01_plattform_initial_setup.md).

---

## Referenzprojekt aus früherer Semesterarbeit

- **Dokumentation Sem 4:** [https://cancani.com/geraeteausleihe-sem4/dokumentation/](https://cancani.com/geraeteausleihe-sem4/dokumentation/)
- **Projektseite Sem 4:** [https://cancani.com/geraeteausleihe-sem4](https://cancani.com/geraeteausleihe-sem4)

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
| Kolloquium | 08.07.2026 |
| Repository | [github.com/Cancani/gitops-platform-semesterarbeit5](https://github.com/Cancani/gitops-platform-semesterarbeit5) |
