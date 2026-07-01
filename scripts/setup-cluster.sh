set -euo pipefail

CLUSTER_NAME="gitops-platform"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIND_CONFIG="${SCRIPT_DIR}/../kind/cluster.yaml"

echo "==> kind Cluster Setup"
echo

for cmd in docker kind kubectl; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "FEHLER: '$cmd' ist nicht installiert oder nicht im PATH." >&2
    case "$cmd" in
      docker)  echo "  Installation: https://docs.docker.com/get-docker/" >&2 ;;
      kind)    echo "  Installation: https://kind.sigs.k8s.io/docs/user/quick-start/#installation" >&2 ;;
      kubectl) echo "  Installation: https://kubernetes.io/docs/tasks/tools/" >&2 ;;
    esac
    exit 1
  fi
done

if ! docker info >/dev/null 2>&1; then
  echo "FEHLER: Docker Daemon läuft nicht." >&2
  echo "  Bitte Docker Desktop bzw. den Docker Daemon starten und Skript erneut ausführen." >&2
  exit 1
fi

if [[ ! -f "${KIND_CONFIG}" ]]; then
  echo "FEHLER: Konfigurationsdatei nicht gefunden: ${KIND_CONFIG}" >&2
  exit 1
fi

# Idempotenz: existiert der Cluster bereits?
if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
  echo "Cluster '${CLUSTER_NAME}' existiert bereits."
  kubectl config use-context "kind-${CLUSTER_NAME}" >/dev/null
  echo
  echo "Aktueller Status:"
  kubectl get nodes -o wide
  exit 0
fi

# Cluster erstellen
echo "Erstelle kind Cluster '${CLUSTER_NAME}'..."
echo "  Konfiguration: ${KIND_CONFIG}"
echo

kind create cluster \
  --name "${CLUSTER_NAME}" \
  --config "${KIND_CONFIG}" \
  --wait 60s

kubectl config use-context "kind-${CLUSTER_NAME}" >/dev/null

echo
echo "==> Cluster ist bereit"
echo
kubectl get nodes -o wide
echo
echo "Nächste Schritte:"
echo "  - kubectl cluster-info"
echo "  - Cluster löschen: bash scripts/teardown-cluster.sh"