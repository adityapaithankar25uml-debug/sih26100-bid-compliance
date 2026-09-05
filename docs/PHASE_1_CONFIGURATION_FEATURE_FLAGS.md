# Phase 1 — Configuration & Feature Flag Governance Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Configuration Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines runtime configuration management, dynamic feature flag controls, environment variable standards, and feature activation governance.

The feature flag governance principle is:
> **"Feature flags enable runtime operational toggles (e.g. government adapter mode switches, AI fallback toggles). Feature flags MUST BE auditable and MUST NEVER bypass security authentication or deterministic rule evaluations."**

---

## 2. Dynamic Feature Flag Inventory

| Feature Flag Key | Default State | Allowed Values | Governance Purpose & Description |
|---|---|---|---|
| **`GOVT_ADAPTER_MODE_MCA21`** | `LIVE` | `LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK` | Toggles MCA21 integration adapter runtime operating mode |
| **`GOVT_ADAPTER_MODE_GSTN`** | `LIVE` | `LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK` | Toggles GSTN integration adapter runtime operating mode |
| **`AI_GATEWAY_PRIMARY_ROUTE`** | `PRIMARY_CLOUD` | `PRIMARY_CLOUD`, `SECONDARY_CLOUD`, `LOCAL_MODEL` | Controls AI Gateway primary model routing target |
| **`DOCUMENT_CDR_STRICT_MODE`** | `ENABLED` | `ENABLED`, `PERMISSIVE` | Enforces strict macro disarming & sanitization during PDF uploads |
| **`COMPLIANCE_FOUR_EYES_GATE`**| `POLICY_CONTROLLED`| `ENABLED`, `DISABLED`, `POLICY_CONTROLLED` | Controls mandatory senior officer approval requirement for overrides |

---

## 3. Feature Flag Audit & Change Rules

1. **Auditable Toggles:** Modifying a feature flag value emits a structured `FEATURE_FLAG_TOGGLED` event written to the tamper-evident audit ledger.
2. **Environment Scoping:** Feature flags are scoped to specific environment identifiers; toggling a flag in `DEVELOPMENT` cannot affect `PRODUCTION`.
