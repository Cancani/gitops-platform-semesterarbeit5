# Semesterarbeit 5: Aufbau einer GitOps basierten Kubernetes Plattform mit Preisüberwachungs WebApp

| Feld | Wert |
|------|------|
| Autor | Efekan Demirci |
| Klasse | ITCNE24 |
| Schule | Technische Berufsschule Zürich TBZ, Höhere Fachschule |
| Lehrgang | Dipl. Informatiker HF, Cloud Native Engineer |
| Semesterarbeit | Nummer 5 |
| Fachexperte IaCA, CNC, CNA | Marcel Bernet |
| Fachexperte Projektmanagement | Thanam Pangri |
| Module | Projektmanagement, IaCA, CNC und CNA, optional DevOps |
| Geplanter Aufwand | ca. 50 Stunden über 9 Wochen |
| Repository | https://github.com/Cancani/gitops-platform-semesterarbeit5 |
| Pages | https://cancani.com/gitops-platform-sem5/ |
| Version | 0.2, Stand nach Kickoff Anpassung |

# Semesterarbeit 5: Aufbau einer GitOps basierten Kubernetes Plattform mit Preisüberwachungs WebApp

| Feld | Wert |
|------|------|
| Autor | Efekan Demirci |
| Klasse | ITCNE24 |
| Schule | Technische Berufsschule Zürich TBZ, Höhere Fachschule |
| Lehrgang | Dipl. Informatiker HF, Cloud Native Engineer |
| Semesterarbeit | Nummer 5 |
| Fachexperte IaCA, CNC, CNA | Marcel Bernet |
| Fachexperte Projektmanagement | Thanam Pangri |
| Module | Projektmanagement, IaCA, CNC und CNA, optional DevOps |
| Geplanter Aufwand | ca. 50 Stunden über 9 Wochen |
| Repository | https://github.com/Cancani/gitops-platform-semesterarbeit5 |
| Pages | https://cancani.com/gitops-platform-sem5/ |
| Version | 0.2, Stand nach Kickoff Anpassung |

## Inhaltsverzeichnis

- [Semesterarbeit 5: Aufbau einer GitOps basierten Kubernetes Plattform mit Preisüberwachungs WebApp](#semesterarbeit-5-aufbau-einer-gitops-basierten-kubernetes-plattform-mit-preisüberwachungs-webapp)
- [Semesterarbeit 5: Aufbau einer GitOps basierten Kubernetes Plattform mit Preisüberwachungs WebApp](#semesterarbeit-5-aufbau-einer-gitops-basierten-kubernetes-plattform-mit-preisüberwachungs-webapp-1)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [1. Management Summary](#1-management-summary)
  - [2. Einleitung](#2-einleitung)
    - [2.1 Ausgangslage](#21-ausgangslage)
    - [2.2 Zielgruppe](#22-zielgruppe)
    - [2.3 Zielsetzung und Messkriterien](#23-zielsetzung-und-messkriterien)
    - [2.4 Abgrenzung](#24-abgrenzung)
    - [2.5 Themenfeldabdeckung](#25-themenfeldabdeckung)
    - [2.6 Anpassung der Projektdauer nach Kickoff Präsentation](#26-anpassung-der-projektdauer-nach-kickoff-präsentation)
  - [3. Projektmanagement](#3-projektmanagement)
    - [3.1 Vorgehensmodell](#31-vorgehensmodell)
    - [3.2 Sprintplan](#32-sprintplan)
      - [Sprint 1, Wochen 1 bis 3, Setup und Fundament](#sprint-1-wochen-1-bis-3-setup-und-fundament)
      - [Sprint 2, Wochen 4 bis 6, GitOps Durchstich](#sprint-2-wochen-4-bis-6-gitops-durchstich)
      - [Sprint 3, Wochen 7 bis 9, Stabilisierung, Runbooks, Doku](#sprint-3-wochen-7-bis-9-stabilisierung-runbooks-doku)
    - [3.3 Sprint Reviews und Retrospektiven (Vorlage)](#33-sprint-reviews-und-retrospektiven-vorlage)
    - [3.4 Branching Strategie](#34-branching-strategie)
    - [3.5 Repository Strategie: Monorepo](#35-repository-strategie-monorepo)
    - [3.6 Definition of Done](#36-definition-of-done)

---

## 1. Management Summary

In dieser Semesterarbeit wird eine kleine, aber realistische Cloud Native Plattform auf Basis von Kubernetes aufgebaut. Auf der Plattform läuft eine einfache Preisüberwachungs WebApp als Referenzanwendung. Sie ruft regelmässig Preisdaten von digitalen Marktplatzobjekten ab, speichert aktuelle und historische Werte und stellt diese über eine einfache Weboberfläche dar.

Der fachliche Fokus liegt nicht auf der WebApp, sondern auf der Plattform und dem Bereitstellungsprozess. Konkret werden Containerisierung, deklarative Konfiguration mit Helm, eine CI Pipeline mit Container Registry sowie GitOps mit Argo CD umgesetzt. Der gewünschte Soll Zustand der Anwendung wird im Git Repository abgelegt. Argo CD synchronisiert ihn automatisch in den Cluster. Änderungen erfolgen deklarativ, sind nachvollziehbar und reproduzierbar.

Die Arbeit zeigt anhand eines praxisnahen Use Cases, wie zentrale Cloud Native Konzepte in einer überschaubaren, prüfbaren Umgebung kombiniert werden können. Sie deckt die Pflichtmodule Projektmanagement, IaCA und CNC/CNA ab und tangiert das optionale Modul DevOps durch CI Pipeline, Container Registry und automatisierte Auslieferung. Die Anwendung selbst bleibt bewusst einfach. Der Mehrwert liegt im strukturierten Plattformaufbau und in der nachvollziehbaren Betriebsdokumentation.

**Ergebnis:** Ein versionierter, deklarativer und automatisierbarer Deployment Workflow auf einer kleinen Kubernetes Plattform, dokumentiert mit Architekturdiagrammen, Runbooks und einer reproduzierbaren Umgebung.

---

## 2. Einleitung

### 2.1 Ausgangslage

Containerisierte Anwendungen werden in vielen Umgebungen noch manuell oder nur teilweise automatisiert bereitgestellt. Daraus ergeben sich typische Probleme:

- Deployments sind schwer nachvollziehbar.
- Rollbacks sind nicht eindeutig definiert.
- Konfigurationen sind nicht zentral dokumentiert.
- Der Soll Zustand einer Anwendung ist nicht versioniert.
- Wer was wann geändert hat, lässt sich nachträglich oft nur mit Aufwand rekonstruieren.

GitOps adressiert diese Probleme, indem der Soll Zustand der Plattform und der Anwendung in einem Git Repository definiert wird. Ein Operator wie Argo CD synchronisiert diesen Zustand automatisch in den Cluster und meldet Abweichungen.

### 2.2 Zielgruppe

Diese Dokumentation richtet sich an:

- den Fachexperten und die Lehrgangsleitung der TBZ,
- spätere Studierende, die einen vergleichbaren Plattformaufbau als Referenz nutzen wollen,
- den Autor selbst als Nachschlagewerk im Betrieb der Plattform.

### 2.3 Zielsetzung und Messkriterien

| Nr. | Ziel | Messkriterium |
|----|------|---------------|
| 1 | Kubernetes Umgebung aufbauen | Cluster ist lauffähig und mit `kubectl` erreichbar. |
| 2 | Preisüberwachungs WebApp erstellen | WebApp zeigt aktuelle und gespeicherte Preisdaten an. |
| 3 | Anwendung mit Helm paketieren | Anwendung kann über ein Helm Chart reproduzierbar installiert werden. |
| 4 | GitOps mit Argo CD umsetzen | Änderungen im Git Repository werden durch Argo CD auf Kubernetes synchronisiert. |
| 5 | Build und Image Veröffentlichung automatisieren | CI Pipeline erstellt ein Container Image und veröffentlicht es in einer Container Registry. |
| 6 | Dokumentation und Runbooks erstellen | Dokumentation enthält Architektur, Aufbau, Deployment Ablauf und mindestens drei Runbooks. |

### 2.4 Abgrenzung

Bewusst nicht im Scope:

- produktive Hochverfügbarkeit, Multi Cluster, Service Mesh,
- vollwertiger Observability Stack (Prometheus, Grafana, Loki) als Pflicht; falls Zeit übrig, optional,
- Identity Provider Integration (OIDC, SSO) für Argo CD,
- vollständige Sicherheitshärtung wie Network Policies, Pod Security Standards, RBAC für mehrere Teams,
- vollständige Frontend Architektur, das UI bleibt absichtlich minimal.

### 2.5 Themenfeldabdeckung

| Modul | Abdeckung in dieser Arbeit |
|-------|----------------------------|
| Projektmanagement (PRJ) | Projektplanung, Sprints, User Stories, Risikomanagement, Reflexion |
| IaCA (Infrastructure as Code Advanced) | Cluster Bootstrap per Skript, Helm Chart als deklarative Anwendungsbeschreibung, Argo CD Manifeste, alles versioniert |
| CNC, Cloud Native Core | Kubernetes Grundlagen, Pods, Services, Deployments, ConfigMaps, Secrets, CronJob |
| CNA, Cloud Native Advanced | Helm, GitOps mit Argo CD, Health Checks, deklarative Application Lifecycle |
| DevOps (optional) | CI Pipeline mit GitHub Actions, Container Registry, automatisierte Auslieferung |

### 2.6 Anpassung der Projektdauer nach Kickoff Präsentation

Die ursprüngliche Planung im Einreichungsformular ging von einer Projektdauer von 12 Wochen aus, aufgeteilt in vier Sprints zu je drei Wochen. In der Kickoff Präsentation wurde durch die Lehrgangsleitung präzisiert, dass die Semesterarbeit tatsächlich nur **9 Wochen** dauert. Empfohlen wurde eine Sprintdauer von drei Wochen, sodass insgesamt drei Sprints durchgeführt werden.

Die beiden Zwischenpräsentationen fallen damit jeweils auf das Ende von Sprint 1 und Sprint 2. Sie bieten eine strukturierte Gelegenheit, den Fortschritt zu reflektieren und gegebenenfalls den Plan anzupassen.

Konsequenzen für diese Arbeit:

- Die Sprintplanung wurde von vier auf drei Sprints reduziert (siehe Kapitel 3.2).
- Inhaltlich wurden die ursprünglichen 21 User Stories auf 16 verdichtet, wobei der GitOps Durchstich von Sprint 3 auf **Sprint 2** vorgezogen wurde.
- Die Doku Pflege erfolgt parallel ab Sprint 1, damit Sprint 3 nicht durch Doku Nachholarbeit unter Druck gerät.
- Optional geplante Erweiterungen (Argo CD Image Updater, mehrere Values Profile, PostgreSQL als Subchart, vollwertiges Monitoring) wurden gestrichen oder als reine Bonus Items eingestuft.

Diese Anpassung wurde nicht als Risiko, sondern als Präzisierung des Scopes verstanden. Der reduzierte Zeitrahmen schärft den Fokus auf die Plattform und auf einen sauberen GitOps Lifecycle.

---

## 3. Projektmanagement

### 3.1 Vorgehensmodell

Die Arbeit folgt einem schlanken, agilen Vorgehensmodell mit drei Sprints zu je drei Wochen. Pro Sprint werden ein Sprint Ziel, eine kleine Anzahl User Stories und ein definierter Demo Stand festgelegt. Am Ende jedes Sprints werden Sprint Review und Sprint Retrospektive im Dokument festgehalten.

Das Projektmanagement erfolgt vollständig auf GitHub:

- **Issues** für User Stories, Tasks, Bugs und technische Abklärungen,
- **GitHub Projects** als Kanban Board (Spalten: Backlog, Ready, In Progress, Review, Done),
- **Custom Fields** im Project Board für Story Points, Priority und Sprint Zuordnung,
- **Milestones** pro Sprint (Sprint 1, Sprint 2, Sprint 3),
- **Pull Requests** für Code Reviews mit sich selbst, das heisst jede grössere Änderung wird über einen Branch und PR eingebracht,
- **Tags und Releases** für Sprint Abschlüsse und die Demo Version.

### 3.2 Sprintplan

Realistisch geplant mit ca. 50 Stunden Aufwand verteilt auf 9 Wochen, also rund 5 bis 6 Stunden pro Woche.

#### Sprint 1, Wochen 1 bis 3, Setup und Fundament

**Sprint Ziel:** Repository, Cluster, WebApp Skelett und Container sind lokal lauffähig.

| Story | Inhalt | Story Points |
|-------|--------|--------------|
| US01 | Repository, Project Board, Milestones, Branch Protection, Issue Templates aufgesetzt | 1 |
| US02 | Architekturentscheide dokumentiert (mindestens 5 ADRs) | 2 |
| US03 | Lokaler Kubernetes Cluster mit kind, idempotentes Setup Skript | 3 |
| US04 | WebApp Skelett mit FastAPI, Endpoints `/`, `/healthz`, `/ready`, lokal lauffähig | 3 |
| US05 | Dockerfile baut Image lokal, Container startet, `/healthz` liefert 200 | 2 |

**Sprint 1 Total:** 11 Story Points.

**Demo Stand am Sprint Ende, Zwischenpräsentation 1:**
- Cluster läuft, `kubectl get nodes` zeigt zwei Ready Nodes.
- WebApp läuft per `docker run`, Browser zeigt Hello World mit Health Check.
- Repository, Board und Doku Skelett sind auf Pages sichtbar.

#### Sprint 2, Wochen 4 bis 6, GitOps Durchstich

**Sprint Ziel:** Push auf `main` führt automatisch zu Build, Push, Sync und Deployment im Cluster.

| Story | Inhalt | Story Points |
|-------|--------|--------------|
| US06 | Preisabruf gegen Quelle oder Testdaten implementiert, Daten in SQLite | 3 |
| US07 | API liefert aktuelle und historische Preise, Frontend zeigt Tabelle und einfachen Verlauf | 3 |
| US08 | GitHub Actions Workflow baut Image und pusht nach GHCR | 3 |
| US09 | Helm Chart `price-watch` mit Deployment, Service, ConfigMap, Secret, PVC, CronJob | 3 |
| US10 | Argo CD installiert, Application zeigt auf Helm Chart, automatisches Sync funktioniert | 3 |
| US11 | Liveness und Readiness Probes konfiguriert | 1 |

**Sprint 2 Total:** 16 Story Points. Bewusst der schwerste Sprint, da hier der Durchstich entsteht.

**Demo Stand am Sprint Ende, Zwischenpräsentation 2:**
- Push auf `main` führt zu CI Build, Argo CD synct, neue Version läuft im Cluster.
- WebApp im Cluster zeigt Preise (echt oder Testdaten).
- Argo CD UI zeigt Application im Status `Synced, Healthy`.

#### Sprint 3, Wochen 7 bis 9, Stabilisierung, Runbooks, Doku

**Sprint Ziel:** Plattform und Dokumentation sind prüfbar abgeschlossen, Schlussdemo ist vorbereitet.

| Story | Inhalt | Story Points |
|-------|--------|--------------|
| US12 | Rollback Szenario per Git Revert dokumentiert | 2 |
| US13 | Drei Runbooks erstellt, getestet und in Doku eingebunden | 3 |
| US14 | Tests und Lint laufen automatisiert in der Pipeline | 2 |
| US15 | Architekturdiagramme, Glossar, Quellen, Abbildungsverzeichnis vollständig | 2 |
| US16 | Management Summary, Reflexion und Demo Skript fertig | 3 |

**Sprint 3 Total:** 12 Story Points.

**Demo Stand am Sprint Ende, Schlusspräsentation:**
- Komplette Toolchain läuft, Live Demo zeigt Push und Sync.
- Rollback per `git revert` wird vorgeführt.
- Doku ist vollständig auf Pages erreichbar.

### 3.3 Sprint Reviews und Retrospektiven (Vorlage)

Pro Sprint nach diesem Schema dokumentieren:

```markdown
#### Sprint X Review
- Geplante Stories: ...
- Erreicht: ...
- Nicht erreicht und Grund: ...
- Demo Stand: ...

#### Sprint X Retrospektive
- Was lief gut?
- Was war schwierig?
- Was nehme ich in den nächsten Sprint mit?
```

### 3.4 Branching Strategie

Bewusst einfach gehalten, passend für ein Einpersonen Projekt mit Nachweisanspruch.

- `main` ist der stabile Hauptbranch und gleichzeitig der GitOps Soll Zustand. Direktpushes sind durch Branch Protection unterbunden.
- `develop` ist der permanente Arbeitsbranch. Hier erfolgen die täglichen Commits.
- `gh-pages` wird ausschliesslich vom MkDocs Workflow geschrieben, niemals manuell.
- Pull Requests gehen `develop` nach `main`, jeweils am Sprint Ende, per Squash Merge.
- Optional Feature Branches `feat/<kurzname>` für grössere parallele Themen.
- Tags pro Sprint Abschluss: `sprint-1`, `sprint-2`, `sprint-3` und `demo`.

Branch Protection ist über GitHub Rulesets umgesetzt:

| Branch | Schutz |
|--------|--------|
| `main` | kein Direktpush, PR Pflicht, linear history, kein Force Push, keine Löschung |
| `develop` | keine Löschung, kein Force Push |
| `gh-pages` | keine Löschung (Force Push erlaubt, da MkDocs gh-deploy ihn benötigt) |

### 3.5 Repository Strategie: Monorepo

Es wurde zwischen Monorepo und mehreren Repositories abgewogen.

| Kriterium | Monorepo | Multi Repo |
|-----------|----------|------------|
| Komplexität | gering | höher |
| Nachvollziehbarkeit Commit zu Deployment | direkt | indirekt, mehrere Repos beobachten |
| GitOps Konfiguration | einfacher Pfad in Argo CD | benötigt zusätzliches Konfigurations Repo |
| Realistisch für 50 Stunden Projekt | ja | nein |
| HF Bewertbarkeit, alles an einem Ort | ja | nein |

**Entscheid:** Monorepo. Code, Helm Chart, Argo CD Application und Dokumentation liegen in einem Repository. Argo CD beobachtet `helm/price-watch`. Die Anwendung wird im selben Repository entwickelt, wodurch der Lifecycle transparent ist.

### 3.6 Definition of Done

Eine User Story gilt als erledigt, wenn:

1. der Code auf `main` ist (über `develop` und Pull Request),
2. ein Issue Eintrag dokumentiert, was erledigt wurde,
3. relevante Screenshots oder Logs in `docs/screenshots/` abgelegt sind,
4. die Funktion lokal reproduzierbar ist (Anleitung in der Doku oder im Runbook),
5. wo sinnvoll, Tests oder Lint Schritte in der Pipeline grün sind,
6. wo zutreffend, Argo CD die Application im Status `Synced, Healthy` zeigt.

---