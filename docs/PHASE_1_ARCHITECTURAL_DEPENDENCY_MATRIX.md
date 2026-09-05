# Phase 1 Architectural Dependency & Layer Interaction Matrix

**Project:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
**Organization:** Ministry of Petroleum & Natural Gas / CPCL
**Phase:** Phase 1 — Architecture & Design
**Task:** Task 12 — Final Architecture Integration, Consistency, Traceability & Implementation Readiness Review
**Document Status:** DESIGN DRAFT / READ-ONLY VALIDATION READY

---

## 1. Executive Summary

This document details the architectural interdependencies, layer interactions, and shared invariant constraints across the 11 frozen specification tasks of Phase 1. It provides a formal dependency graph and analysis matrix to verify that:
1. Every architectural layer depends only on stable, well-defined upstream abstractions.
2. Shared invariants are enforced symmetrically across all dependent layers.
3. Potential circular dependencies between domain models, APIs, workflows, and frontend state are identified and eliminated.

---

## 2. Global Architectural Task Dependency Topology

```
+-----------------------------------------------------------------------------------+
|                                TASK 1: System Architecture                        |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                             TASK 2: Domain & Data Model                           |
+-----------------------------------------------------------------------------------+
     |                                    |                                    |
     v                                    v                                    v
+-----------------------+   +---------------------------+   +-----------------------+
| TASK 4: AI Pipeline   |   | TASK 5: Govt Integrations |   | TASK 6: Compliance    |
| & Model Governance    |   | & Verification            |   | AST Rules Engine      |
+-----------------------+   +---------------------------+   +-----------------------+
     |                                    |                                    |
     +------------------------------------+------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        TASK 8: Security & Privacy Architecture                    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     TASK 7: Workflow Orchestration & Job Execution               |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                          TASK 3: API Architecture & Contracts                     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     TASK 11: Frontend, UX & Officer Dashboard                     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                    TASK 10: Infrastructure, DevOps & Deployment                   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                    TASK 9: Observability & Operational Telemetry                  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Comprehensive Task Dependency Matrix

| Task # | Task Title | Upstream Dependencies | Downstream Dependents | Key Shared Invariants |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1** | System Architecture | None (Root Architecture) | Tasks 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 | Overall 5-stage conceptual pipeline model; core system boundaries. |
| **Task 2** | Domain & Data Model | Task 1 | Tasks 3, 4, 5, 6, 7, 8, 11 | Relational schemas, entity identities, immutable history tables. |
| **Task 3** | API Architecture & Contracts | Tasks 1, 2, 8 | Task 11 | OpenAPI 3.1 contracts, Pydantic DTOs, REST standard response envelopes. |
| **Task 4** | AI Pipeline Architecture | Tasks 1, 2 | Tasks 6, 7, 8, 11 | AI output is strictly advisory (`is_authoritative=False`); confidence scores. |
| **Task 5** | Govt Integrations Architecture | Tasks 1, 2 | Tasks 6, 7, 8, 11 | Technical Govt API failures route to `MANUAL_FALLBACK`, never `FAIL`. |
| **Task 6** | Deterministic Compliance Engine | Tasks 1, 2, 4, 5 | Tasks 3, 7, 11 | `MISSING_EVIDENCE != FAIL`; Python AST rule execution sandbox. |
| **Task 7** | Workflow Orchestration | Tasks 1, 2, 4, 5, 6, 8 | Tasks 3, 9, 11 | Workflow execution states decoupled from business compliance state. |
| **Task 8** | Security Architecture | Tasks 1, 2 | Tasks 3, 4, 5, 6, 7, 9, 10, 11 | Backend-authoritative RBAC; SHA-256 tamper-evident hash chain logging. |
| **Task 9** | Observability Architecture | Tasks 1–8, 10, 11 | Operations / SRE | Observability logs and traces are operational telemetry, not compliance facts. |
| **Task 10** | Infrastructure & DevOps | Tasks 1–8 | Task 9 | ECS Fargate reference container model; environment parameterization. |
| **Task 11** | Frontend & UX Architecture | Tasks 1–8 | Task 9, 10 | Frontend consumes REST APIs; cannot make authoritative state decisions. |

---

## 4. Detailed Layer-by-Layer Interaction Analysis

### 4.1 AI Pipeline (Task 4) $\rightarrow$ Data Model (Task 2) $\rightarrow$ Security (Task 8)
- **Interaction Pattern:** The AI Pipeline consumes raw `SourceDocument` text blocks from Task 2, invokes LLM/VLM gateways governed by Task 8 security boundaries (scrubbing PII and credentials), and writes back `ExtractedFact` records.
- **Enforced Invariant:** Facts created by Task 4 carry `is_authoritative = False` and `confidence_score`. Task 8 encrypts all raw storage and scrubbed prompts.

### 4.2 Govt Integrations (Task 5) $\rightarrow$ Compliance Engine (Task 6)
- **Interaction Pattern:** Task 5 queries official government sources (GSTN, MCA21, UDIN) and yields `GovernmentVerificationRecord` items. Task 6 transforms these into `NormalizedFact` records to feed into the AST evaluation engine.
- **Enforced Invariant:** Technical connection timeout or HTTP `5xx` error in Task 5 creates a verification status of `TECHNICAL_UNAVAILABLE` (or `MANUAL_FALLBACK`). Task 6 strictly evaluates this as `UNVERIFIED_SOURCE` and triggers human review, never evaluating it as bidder non-compliance.

### 4.3 Compliance Engine (Task 6) $\rightarrow$ Workflow Orchestration (Task 7)
- **Interaction Pattern:** Task 7 triggers Celery tasks that load Task 6 AST policy rules and execute them against the `EvidenceRecord` bundle for a `BidSubmission`.
- **Enforced Invariant:** Task 7 manages task attempt states (`PENDING`, `RUNNING`, `SUCCESS`, `FAILED_RETRYABLE`). These workflow attempt states are completely isolated from the business evaluation states (`COMPLIANT`, `NON_COMPLIANT`, `MISSING_EVIDENCE`).

### 4.4 API Contracts (Task 3) $\rightarrow$ Security (Task 8) $\rightarrow$ Frontend UX (Task 11)
- **Interaction Pattern:** Task 11 React frontend sends HTTPS requests carrying JWT Bearer tokens to Task 3 FastAPI endpoints. Task 8 middleware validates JWT signatures, checks RBAC permissions against scopes, and logs `AuditEvent` records.
- **Enforced Invariant:** The Task 11 UI hides action buttons for unauthorized roles (e.g., Senior Reviewer override buttons hidden from basic Procurement Officers), but Task 3/8 backend APIs enforce strict server-side authorization check before executing any mutation.

---

## 5. Analysis & Mitigation of Potential Circular Dependencies

During integration review, three potential circular dependencies were analyzed and resolved:

### 5.1 Circular Risk: Workflow State vs. Compliance Evaluation State
- **Potential Risk:** Workflow engine waiting for compliance state to update, while compliance evaluation engine waits for workflow DAG to complete.
- **Architectural Resolution:** Clear separation established in Task 7 and Task 6. Workflow DAG status (`task_attempt.status`) tracks execution progress of Celery workers. Compliance evaluation status (`compliance_evaluation.status`) is a domain entity state written upon task completion. The workflow DAG emits event signals upon state write; it does not poll domain state.

### 5.2 Circular Risk: AI Fact Extraction vs. Document Security Sanitization
- **Potential Risk:** AI pipeline requiring sanitized text, while sanitization engine requires AI classification to detect PII/sensitive sections.
- **Architectural Resolution:** Deterministic multi-stage processing defined in Task 8 §6. Stage 1 applies deterministic regex/presidio PII redaction and malware scanning. Stage 2 produces `SanitizedDerivative`. Stage 3 passes `SanitizedDerivative` to Task 4 AI Gateway. AI processing never executes on un-scanned raw files.

### 5.3 Circular Risk: Audit Event Hash Chaining vs. Database Transactions
- **Potential Risk:** Computing SHA-256 hash of `AuditEvent` requiring `created_at` timestamp and DB `id`, while DB insertion requires hash calculation.
- **Architectural Resolution:** Canonical representation defined in Task 8 §7.1 and Task 9 §4.1. Hash is computed using pre-assigned UUIDv4, sequence counter, and deterministic payload serializer prior to DB commit.

---

## 6. Architectural Dependency Verification Conclusion

The Phase 1 architecture exhibits clean, acyclic dependency topology. Every layer depends upon lower-level abstractions with strict invariant enforcement. No circular dependencies exist.
