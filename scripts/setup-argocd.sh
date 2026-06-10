#!/usr/bin/env bash
#
# Installiert Argo CD im lokalen kind Cluster.
# Idempotent: mehrfaches Ausführen ist gefahrlos.
#
# Voraussetzung: kind Cluster läuft (bash scripts/setup-cluster.sh)
#
# Siehe docs/dokumentation.md Kapitel 5.6 für Details.

set -euo pipefail

NAMESPACE="argocd"

echo "==> Argo CD Installation"
echo

# Voraussetzungen prüfen
for cmd in kubectl; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "FEHLER: '$cmd' ist nicht installiert." >&2
    exit 1
  fi
done

# Cluster erreichbar?
if ! kubectl cluster-info >/dev/null 2>&1; then
  echo "FEHLER: Kein Kubernetes Cluster erreichbar." >&2
  echo "  Cluster starten: bash scripts/setup-cluster.sh" >&2
  exit 1
fi

# Namespace erstellen (idempotent)
if kubectl get namespace "${NAMESPACE}" >/dev/null 2>&1; then
  echo "Namespace '${NAMESPACE}' existiert bereits."
else
  kubectl create namespace "${NAMESPACE}"
  echo "Namespace '${NAMESPACE}' erstellt."
fi

# Argo CD installieren (stable Release)
echo
echo "Installiere Argo CD (stable)..."
kubectl apply -n "${NAMESPACE}" \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Warten bis alle Argo CD Deployments Ready sind
echo
echo "Warte auf Argo CD Pods (bis zu 5 Minuten)..."
kubectl wait --for=condition=available deployment \
  -l "app.kubernetes.io/part-of=argocd" \
  -n "${NAMESPACE}" \
  --timeout=300s

echo
echo "==> Argo CD ist bereit"
echo

# Admin Passwort anzeigen
echo "Admin Passwort:"
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
echo
echo

echo "UI über Port Forward starten:"
echo "  kubectl port-forward svc/argocd-server -n argocd 8080:443"
echo
echo "Browser öffnen: https://localhost:8080"
echo "  Zertifikatswarnung akzeptieren (self-signed)"
echo "  Benutzername: admin"
echo "  Passwort: siehe oben"