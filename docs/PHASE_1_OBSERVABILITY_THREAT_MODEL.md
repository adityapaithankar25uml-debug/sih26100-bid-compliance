# Phase 1 — Telemetry-Specific STRIDE Threat Model Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 9 Observability Threat Model)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the telemetry-specific STRIDE threat model for the SIH26100 platform's observability subsystem. Observability infrastructure processes system event signals and metrics. Securing telemetry pipelines against data leakage, log injection, metric poisoning, and alert suppression is necessary to prevent monitoring compromise.

The governing threat modeling principle is:
> **"Observability controls manage risk but never eliminate it entirely. Every telemetry threat MUST be mapped to mitigations, detection mechanisms, and explicit residual risk assessments."**

---

## 2. Ten Telemetry STRIDE Threat Scenarios

| Threat ID | Target Telemetry Asset | Threat & Attack Vector | Impact | Architectural Mitigation | Detection Mechanism | Residual Risk Level & Owner |
|---|---|---|---|---|---|---|
| **TH-OBS-01** | Log Streams (`LogEvent`) | **Sensitive Data Leakage:** Log events capture unredacted PII, PAN numbers, or DB credentials. | High (Privacy breach, secret exposure) | Pre-Log Privacy Proxy scrubbing headers, secrets, and PII before log emission. | Automated log scanner checking log indices for unredacted regex patterns. | **Low** (Scrubber filters standard patterns) **Owner:** AppSec Lead |
| **TH-OBS-02** | Log Ingestion Pipeline | **Log Injection Attack:** Attacker embeds CRLF (`\r\n`) characters in uploaded filenames to forge log entries. | Medium (Forged log entries, audit confusion) | Control character stripping; structured JSON log formatting. | Log parsing error alerts in log aggregator. | **Low** (JSON formatting neutralizes CRLF) **Owner:** SecOps Lead |
| **TH-OBS-03** | Metric Store (TSDB) | **Metric Poisoning:** Attacker injects high-cardinality labels to exhaust metric TSDB memory. | Medium (TSDB Outage, monitoring DoS) | Metric label whitelist enforcement; TSDB scraping restricted to internal subnet. | High-cardinality metric label count alerts. | **Low** (Whitelist drops invalid labels) **Owner:** DevOps Lead |
| **TH-OBS-04** | Alertmanager / Dashboard | **Alert Suppression:** Rogue admin silences critical alerts to conceal unauthorized manual overrides. | Critical (Un-monitored vigilance violations) | Alert rule edits restricted to `SystemAdmin`; changes logged to audit ledger. | Audit event logging for all alert rule modifications. | **Medium** (Insiders with root admin access) **Owner:** Lead Auditor |
| **TH-OBS-05** | Distributed Traces | **Trace Context Manipulation:** Attacker injects forged `traceparent` headers to disrupt trace correlation. | Low (Corrupted trace graph linkage) | API Gateway validates incoming trace headers; injects verified correlation IDs. | Invalid trace parent header log alerts. | **Low** (Gateway overrides bad headers) **Owner:** AppSec Lead |
| **TH-OBS-06** | Operational Dashboards | **Unauthorized Dashboard Access:** Standard officer views restricted SecOps or Vigilance dashboards. | Medium (Unauthorized metadata exposure) | RBAC + Capability authorization matrix governing dashboard endpoints. | API Gateway 403 Forbidden audit logs. | **Low** (Authz matrix enforces checks) **Owner:** SecOps Lead |
| **TH-OBS-07** | Log Collector Storage | **Log Flooding DoS:** Attacker floods API with invalid calls to exhaust log disk storage. | Medium (Disk exhaustion, log drop) | Ingress rate limiting, log quota caps, non-blocking telemetry drop policies. | Disk volume capacity warning alerts ($> 85\%$). | **Low** (Rate limiters throttle traffic) **Owner:** Infrastructure Lead |
| **TH-OBS-08** | Log Cleanup Worker | **Retention Cleanup Bypass:** Automated cleanup script purges logs locked under active legal investigation. | High (Loss of legal evidence) | Dual-control `LegalHold` engine freezing cleanup for locked tenders. | Telemetry retention cleanup audit log checks. | **Low** (Legal hold overrides cleanup) **Owner:** Lead Auditor |
| **TH-OBS-09** | Application API Core | **Observability Platform Outage:** Log collector crash causes application API threads to block. | High (Application unavailability) | Non-blocking, asynchronous telemetry emission with bounded memory buffers. | Telemetry ring buffer drop count metrics. | **Low** (Buffers drop logs, API stays up) **Owner:** Platform Architect |
| **TH-OBS-10** | Error Stack Traces | **Credential Leak in Stack Traces:** Exception dump exposes DB connection password in error logs. | High (Database credential exposure) | Global exception handler scrubbing connection strings before log emission. | Automated secret scanner in log pipeline. | **Low** (Scrubber redacts credentials) **Owner:** AppSec Lead |

---

## 3. Summary of Telemetry Risk Balance

- **Critical Residual Risks:** 0
- **Medium Residual Risks:** 1 (TH-OBS-04 Alert Suppression by Root Admin)
- **Low Residual Risks:** 9
