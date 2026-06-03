{{/*
Chart Name expandieren, mit nameOverride Support.
*/}}
{{- define "price-watch.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Vollqualifizierter App Name (Release Name plus Chart Name).
*/}}
{{- define "price-watch.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Chart Name plus Version als Label.
*/}}
{{- define "price-watch.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Gemeinsame Labels für alle Ressourcen.
*/}}
{{- define "price-watch.labels" -}}
helm.sh/chart: {{ include "price-watch.chart" . }}
{{ include "price-watch.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector Labels für Deployment Selector und Service Selector.
Bewusst nur app.kubernetes.io/name und app.kubernetes.io/instance, damit der
Selector stabil bleibt, wenn der Chart Version Label sich ändert.
*/}}
{{- define "price-watch.selectorLabels" -}}
app.kubernetes.io/name: {{ include "price-watch.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}