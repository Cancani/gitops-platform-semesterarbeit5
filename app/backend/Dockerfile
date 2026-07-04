# syntax=docker/dockerfile:1.7
# Build:
#   docker build -t price-watch-backend:dev app/backend
#
# Run:
#   docker run --rm -p 8000:8000 price-watch-backend:dev

FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Virtuelle Umgebung als isolierte Ziel-Location für Pakete
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

# OCI Image Labels für Metadaten (https://specs.opencontainers.org/image-spec/)
LABEL org.opencontainers.image.title="Price Watch Backend" \
      org.opencontainers.image.description="FastAPI Backend der Preisüberwachungs WebApp" \
      org.opencontainers.image.source="https://github.com/Cancani/gitops-platform-semesterarbeit5" \
      org.opencontainers.image.licenses="Apache-2.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}"

# Non-Root User anlegen, damit der Container nicht als root läuft
RUN groupadd --system --gid 1001 app && \
    useradd --system --uid 1001 --gid app --create-home --home-dir /home/app app

WORKDIR /app

# Abhängigkeiten aus dem Builder Stage übernehmen
COPY --from=builder /opt/venv /opt/venv

# Anwendungscode mit korrekter Ownership kopieren
COPY --chown=app:app . .

# Non-Root User aktivieren
USER app

EXPOSE 8000

# Container interner Health Check, unabhängig von Kubernetes Probes.
# Nutzt urllib statt curl, da curl im slim Image nicht installiert ist.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz').read()" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]