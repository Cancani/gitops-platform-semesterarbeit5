#!/usr/bin/env bash
# Löscht den lokalen kind Cluster
# Idempotent: Wenn der Cluster nicht existiert, beendet sich das Skript
# ohne Fehler.

set -euo pipefail

CLUSTER_NAME="gitops-platform"

if ! command -v kind >/dev/null 2>&1; then
  echo "FEHLER: 'kind' ist nicht installiert." >&2
  exit 1
fi

if ! kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
  echo "Cluster '${CLUSTER_NAME}' existiert nicht."
  exit 0
fi

echo "Lösche kind Cluster '${CLUSTER_NAME}'..."
kind delete cluster --name "${CLUSTER_NAME}"
echo "Cluster gelöscht."