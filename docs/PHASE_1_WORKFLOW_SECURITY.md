# Phase 1 — Workflow Security, Resource Governance & Concurrency Boundaries Specification

## Overview

The **Workflow Security & Resource Governance Specification** defines the security boundaries, authorization controls, resource limits, and concurrency protections governing workflow orchestration in the **SIH26100 Bid Compliance Verification Platform**.

---

## 1. Workflow Authorization & Role-Based Access Control (RBAC)

Workflow operations are protected by explicit capability-based RBAC policies (Task 3 API Authorization Matrix):

```
[Incoming Workflow Command] ──► [Inspect Authentication Token & Capability]
                                             │
      ┌──────────────────────────────────────┴──────────────────────────────────────┐
      ▼ (Authorized Role & Capability Met)                                          ▼ (Unauthorized)
[Execute Workflow Transition]                                               [Return 403 Forbidden]
```

| Workflow Command / API Endpoint | Required Role | Required RBAC Capability | Resource Boundary Check |
| :--- | :--- | :--- | :--- |
| `POST /api/v1/submissions/{id}/evaluate` | Procurement Officer / System | `WORKFLOW_DISPATCH` | User belongs to tender organization. |
| `GET /api/v1/workflows/{id}` | Procurement Officer / Auditor | `WORKFLOW_VIEW` | Tenant/organization scope check. |
| `POST /api/v1/workflows/{id}/cancel` | Authorized Senior Officer | `WORKFLOW_CANCEL` | Four-eyes check if mandated by policy. |
| `POST /api/v1/workflows/{id}/retry` | System Admin / Officer | `WORKFLOW_RETRY` | Checkpoint ownership validation. |
| `POST /api/v1/submissions/{id}/override` | Authorized Procurement Officer | `MANUAL_OVERRIDE_CREATE` | Mandatory justification & proof required. |

---

## 2. Resource Governance & Abuse Protection

To protect the platform against Denial-of-Service (DoS) attacks, runaway task loops, or oversized workloads, the orchestrator enforces resource boundaries:

1. **Configurable DAG Node Limit:** Maximum allowed tasks per workflow DAG is a deployment-configurable setting (e.g., max 100 tasks).
2. **Configurable Execution Timeouts:** Maximum total workflow execution duration is capped by policy (e.g. 3600 seconds max runtime before transitioning to `TIMEOUT` / `WAITING`).
3. **Queue Backpressure Controls:** If task queues exceed configured depth thresholds, job dispatchers apply backpressure by rejecting new low-priority evaluations with `HTTP 429 Too Many Requests`.
4. **No Arbitrary Executable Workflows:** Users cannot submit custom code or executable scripts. Workflow definitions are static, schema-validated JSON/YAML objects approved during deployment.

---

## 3. Strict Subsystem Access Control Invariants

> [!CAUTION]
> **RESTRICTED SUBSYSTEM BOUNDARIES:**
> 1. **AI Subsystem Isolation:** AI Gateway models cannot directly execute workflow state transitions or invoke external government web APIs.
> 2. **Worker Isolation:** Background workers run with least-privilege service credentials and cannot bypass DB row-level security policies.
> 3. **PII Masking:** Logs and metric events automatically sanitize and mask PII fields (PAN numbers, bank accounts, personal names).
