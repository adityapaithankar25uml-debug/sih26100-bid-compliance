# Phase 1 — Observability Master Risk Register

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 9 Observability Risk Register)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification documents the Task 9 Observability Risk Register for the SIH26100 platform. Deploying an operational monitoring and telemetry subsystem introduces technical, operational, and data protection risks that must be tracked and managed.

The core risk management axiom is:
> **"Telemetry systems reduce operational uncertainty but introduce technical and privacy risks. Risk management requires transparent identification, continuous controls, clear ownership, and realistic residual risk assessments."**

---

## 2. Exhaustive 15-Risk Observability Register

| Risk ID | Category | Risk Description | Initial Likelihood | Initial Impact | Architectural Mitigations | Detection Mechanism | Residual Risk Level | Assigned Owner | Lifecycle State |
|---|---|---|---|---|---|---|---|---|---|
| **OR-01** | Privacy | Log streams accidentally capture unredacted bidder PII or PAN numbers. | Possible | High | Pre-Log Privacy Proxy executing regex/NLP PII tokenization. | Automated log scanner alerts. | **Low** | Data Privacy Officer | Proposed |
| **OR-02** | Security | Attacker executes log injection via CRLF characters in document filenames. | Likely | Medium | Control character stripping; structured JSON log formatting. | Log parser error logs. | **Low** | AppSec Lead | Proposed |
| **OR-03** | Operations | High log volume causes disk space exhaustion on log storage nodes. | Likely | Medium | Rate limiting, non-blocking log drop policies, retention caps. | Disk volume capacity alerts. | **Low** | Infrastructure Lead | Proposed |
| **OR-04** | Security | Rogue administrator silences production alerts to conceal unauthorized overrides. | Unlikely | Critical | Alert rule edits restricted to `SystemAdmin`; logged to audit ledger. | Audit event logs. | **Medium** | Lead Auditor | Proposed |
| **OR-05** | Reliability | Log collector outage causes main application API request threads to block. | Possible | High | Asynchronous log emission with bounded memory ring buffers. | Ring buffer drop metrics. | **Low** | Platform Architect | Proposed |
| **OR-06** | Performance| High-cardinality metric labels cause TSDB memory exhaustion. | Likely | Medium | Metric label whitelist enforcement; TSDB scraping restricted. | Label count metrics. | **Low** | DevOps Lead | Proposed |
| **OR-07** | Cost | High-volume AI token usage or trace sampling causes cloud cost overruns. | Possible | Medium | Adaptive sampling, token usage tracking, budget alert triggers. | Cost budget alerts. | **Low** | Operations Lead | Proposed |
| **OR-08** | Compliance | Telemetry retention worker purges logs locked under active legal investigation. | Unlikely | High | Dual-control `LegalHold` engine overriding retention cleanup. | Retention cleanup logs. | **Low** | Lead Auditor | Proposed |
| **OR-09** | Reliability | Government portal outage causes thundering herd alert flood to on-call ops. | Likely | Medium | Alert deduplication, 15-min grouping, circuit breaker isolation. | Alertmanager metrics. | **Low** | Integration Lead | Proposed |
| **OR-10** | Security | Exception stack trace dumps raw database connection password into logs. | Unlikely | High | Global exception handler scrubbing connection strings before logging. | Secret scanner alerts. | **Low** | AppSec Lead | Proposed |
| **OR-11** | Operations | Asynchronous Celery tasks fail to propagate `correlationId` across retries. | Possible | Medium | Task metadata header injection enforcing context propagation. | Missing correlation logs. | **Low** | Software Architect | Proposed |
| **OR-12** | Security | Unauthorized user gains access to restricted vigilance audit dashboards. | Unlikely | Medium | 5D authorization matrix governing dashboard endpoints. | 403 Forbidden logs. | **Low** | SecOps Lead | Proposed |
| **OR-13** | AI Safety | High AI schema failure rate causes background worker queue backlog. | Possible | Medium | AI Gateway automatic fallback to secondary provider or local model. | Schema failure metrics. | **Low** | AI Lead | Proposed |
| **OR-14** | Data Quality| Stale government verification data used in rule evaluation without alert. | Possible | Medium | Source freshness tracking; `stale_evidence_flag` alerting. | Freshness metrics. | **Low** | Integration Lead | Proposed |
| **OR-15** | Governance | Metric definitions drift across components without central catalog updates. | Likely | Low | Metric Card specification governance and version control. | Metric catalog audit. | **Low** | Lead Architect | Proposed |

---

## 3. Residual Risk Summary

- **Critical Residual Risks:** 0
- **Medium Residual Risks:** 1 (OR-04 Alert Suppression by Root Admin)
- **Low Residual Risks:** 14
