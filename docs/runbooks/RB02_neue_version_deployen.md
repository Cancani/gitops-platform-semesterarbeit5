## Runbook 02: Neue Version deployen

**Zweck**

Dieses Runbook beschreibt den normalen GitOps Release Workflow. Eine Änderung im
Repository löst automatisch einen neuen Build und ein neues Deployment aus.

**Voraussetzungen**

- Plattform läuft gemäss RB-01
- Schreibzugriff auf das Repository
- GitHub Actions aktiv

**Schritte**

1. Änderung im Backend vornehmen und committen

```bash
git checkout -b feature/mein-change
# Änderung vornehmen
git add .
git commit -m "feat(app): beschreibung der änderung"
git push origin feature/mein-change
```

2. Pull Request erstellen und auf main mergen (Squash Merge)

Nach dem Merge auf main startet die CI-Pipeline automatisch.

3. Pipeline beobachten

Unter `https://github.com/Cancani/gitops-platform-semesterarbeit5/actions` den
laufenden Workflow `CI - Build und Push` beobachten. Die Jobs `lint-and-test`
und `build-and-push` müssen grün sein.

4. Argo CD Sync beobachten

Argo CD prüft alle 3 Minuten das Repository. Nach dem CI-Lauf aktualisiert die
Pipeline `helm/price-watch/values.yaml` mit dem neuen Image Tag. Argo CD erkennt
die Änderung und synct automatisch.

Manueller Sync falls nötig:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
# In der UI: App anklicken -> Sync
```

5. Neuen Pod prüfen

```bash
kubectl get pods
kubectl describe pod <pod-name>
```

Der Pod zeigt den neuen Image Tag unter `Image:`.

**Erfolgskriterium**

- CI-Pipeline grün
- `values.yaml` auf main enthält neuen SHA Tag
- Argo CD zeigt `Synced` und `Healthy`
- Neuer Pod läuft mit dem neuen Image

**Nachweis**

Screenshot CI-Pipeline grün, Screenshot Argo CD nach Sync mit neuem Image Tag.