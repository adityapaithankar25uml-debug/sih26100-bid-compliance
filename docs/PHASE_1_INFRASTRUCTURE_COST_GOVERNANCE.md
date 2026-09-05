# Phase 1 — Infrastructure Cost Governance & Resource Tagging Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Cost Governance Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines infrastructure cost governance, resource tagging standards, budget anomaly detection, and environment cost isolation.

---

## 2. Resource Tagging Standard Matrix

| Mandatory Tag Key | Allowed Tag Values | Governance Purpose |
|---|---|---|
| **`Project`** | `SIH26100` | Universal project cost aggregation |
| **`Environment`** | `local`, `dev`, `staging`, `prod` | Multi-environment cost allocation |
| **`Owner`** | `cpcl-procurement-ops`, `sih-core-team` | Departmental cost center tracking |
| **`Component`** | `api`, `ui`, `worker-ocr`, `db`, `ai-gateway` | Subsystem resource consumption breakdown |
| **`ManagedBy`** | `terraform`, `cloudformation` | IaC provenance tracking |

---

## 3. Cost Anomaly Triggers & Budget Alerts

1. **Budget Threshold Alert:** Triggers an `INFORMATIONAL` notification when monthly spend reaches 80% of forecasted budget.
2. **Anomaly Detection Spike:** Triggers a `WARNING` alert if daily compute or AI provider cost spikes by $> 50\%$ above rolling baseline.
