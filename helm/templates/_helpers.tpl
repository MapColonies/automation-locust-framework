{{/* vim: set filetype=mustache: */}}

{{/* Expand the name of the chart */}}
{{- define "locust.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/* Generate the full name of the chart */}}
{{- define "locust.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/* Create chart name and version as used by the chart label */}}
{{- define "locust.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/* Generate master service name */}}
{{- define "locust.master-svc" -}}
{{- printf "%s-%s" (.Release.Name | trunc 52 | trimSuffix "-") "master-svc" -}}
{{- end -}}

{{/* Generate master name */}}
{{- define "locust.master" -}}
{{- printf "%s-%s" (.Release.Name | trunc 56 | trimSuffix "-") "master" -}}
{{- end -}}

{{/* Generate worker name */}}
{{- define "locust.worker" -}}
{{- printf "%s-%s" (.Release.Name | trunc 56 | trimSuffix "-") "worker" -}}
{{- end -}}

{{/* Selector labels */}}
{{- define "locust.selectorLabels" -}}
app.kubernetes.io/name: {{ include "locust.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
load_test: {{ .Values.global.name }}
{{- end }}

{{/* Common labels */}}
{{- define "locust.labels" -}}
helm.sh/chart: {{ include "locust.chart" . }}
{{ include "locust.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Generate external secret volume */}}
{{- define "locust.external_secret.volume" -}}
- name: external-secrets
  projected:
    sources:
{{- end -}}