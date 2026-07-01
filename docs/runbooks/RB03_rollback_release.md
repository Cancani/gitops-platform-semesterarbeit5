## Runbook 03: Rollback eines fehlerhaften Releases

**Zweck**

Dieses Runbook beschreibt den Rollback eines fehlerhaften Deployments via `git revert`.
Der fehlerhafte Stand wird durch einen Revert-Commit rückgängig gemacht. Argo CD erkennt
die Änderung und synct den vorherigen Stand automatisch zurück.

**Voraussetzungen**

- Plattform läuft gemäss RB-01
- Fehlerhafter Commit ist auf main gemergt
- SHA des fehlerhaften Commits ist bekannt

**Schritte**

1. Fehlerhaften Commit identifizieren

```bash
git log --oneline -5
```

Den SHA des fehlerhaften Commits notieren.

2. Pod-Status prüfen

```bash
kubectl get pods
```

Der neue Pod zeigt `ImagePullBackOff` oder `ErrImagePull`. Der alte Pod läuft noch.

3. Neuen Branch erstellen und Revert ausführen

```bash
git checkout main
git pull
git checkout -b feature/revert-bad-commit
git revert <bad-commit-sha> --no-edit
git push origin feature/revert-bad-commit
```

4. Pull Request auf main erstellen und mergen (Squash Merge)

Der Revert-Commit landet auf main. Argo CD erkennt die Änderung in `values.yaml`
und synct den vorherigen Image Tag zurück.

5. Sync abwarten und Pod-Status prüfen

```bash
kubectl get pods
```

Der fehlerhafte Pod verschwindet, der ursprüngliche Pod läuft wieder mit `Running`.

**Erfolgskriterium**

- `kubectl get pods` zeigt nur noch einen Pod mit Status `Running`
- Argo CD zeigt `Synced` und `Healthy`
- `values.yaml` auf main enthält wieder den korrekten Image Tag

**Nachweis**

- Bad Commit SHA: `4563f45`
- Revert Commit SHA: auf main nach PR einsehbar
- Screenshots: Pod in `ImagePullBackOff`, Pod wieder `Running`