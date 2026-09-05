# Phase 1 Architectural Inconsistency Register

**Project:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
**Organization:** Ministry of Petroleum & Natural Gas / CPCL
**Phase:** Phase 1 — Architecture & Design
**Task:** Task 12 — Final Architecture Integration, Consistency, Traceability & Implementation Readiness Review
**Document Status:** DESIGN DRAFT / READ-ONLY VALIDATION READY

---

## 1. Executive Summary & Review Scope

This register documents the results of an aggressive cross-task integration review conducted across Tasks 1 through 11. The objective is to identify, document, and categorize any discrepancies, terminology collisions, duplicated responsibilities, or subtle contradictions that emerged as the architectural specifications evolved across 11 detailed design tasks.

### Strict Governance Rule
**No frozen documents (Tasks 1–11) have been modified silently.** All identified inconsistencies are cataloged here, assigned a severity level (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `INFORMATIONAL`), and provided with an authoritative Phase 1 reconciliation decision or designated for Phase 2 implementation binding.

---

## 2. Inconsistency Findings & Classification Register

### 2.1 Audit Ledger Terminology & Storage Semantics
- **Category:** Audit Semantics / Terminology
- **Severity:** `MEDIUM` (Corrected in Task 9 Review; unified in Task 12)
- **Description:** Early task specifications (Task 1, Task 2) referred to the audit trail as an "immutable PostgreSQL audit table". In Task 8 and Task 9, this was refined to "tamper-evident AuditEvent ledger using SHA-256 hash chaining" to avoid inaccurate claims of native database storage immutability without specialized hardware or PKI.
- **Affected Tasks:** Task 1 §5, Task 2 §7.3 vs. Task 8 §7.1, Task 9 §4.1
- **Authoritative Resolution:** The authoritative formulation across Phase 1 is **"tamper-evident AuditEvent ledger with SHA-256 cryptographic hash chaining"**. PostgreSQL database tables are append-only by role privilege; cryptographic hash chaining provides detection of unauthorized tampering. No digital signatures or PKI are claimed.

---

### 2.2 Government API Technical Failure vs. Bidder Compliance Outcome
- **Category:** Government Verification Authority / Compliance Engine
- **Severity:** `INFORMATIONAL` (Fully Consistent; Formally Reiterated)
- **Description:** Review verified whether any task implied that a government API HTTP 500/502/503 timeout could result in a bidder being marked `NON_COMPLIANT` or `REJECTED`.
- **Affected Tasks:** Task 3 §8, Task 5 §4.2, Task 6 §5.1, Task 7 §6.2
- **Authoritative Resolution:** Perfect alignment maintained across all tasks. Technical failure of an external government endpoint produces `verification_status = TECHNICAL_UNAVAILABLE` or `MANUAL_FALLBACK`. The compliance engine evaluates this as `UNVERIFIED_SOURCE` and assigns a `HUMAN_REVIEW` checkpoint. **Technical government API failure NEVER equals bidder non-compliance.**

---

### 2.3 Evidence Evaluation Status Taxonomy Alignment
- **Category:** Status Taxonomy Alignment
- **Severity:** `LOW`
- **Description:** Task 2 (§6.2) defined evidence status as `VERIFIED`, `UNVERIFIED`, `CONFLICTING`, `MISSING`. Task 6 (§5.3) introduced `STALE`, `INVALID`, `NOT_APPLICABLE`, `MISSING_EVIDENCE`. Task 11 (§5.1) dashboard used `PENDING_VERIFICATION` in UI mockups.
- **Affected Tasks:** Task 2 §6.2, Task 6 §5.3, Task 11 §5.1
- **Authoritative Resolution:** The unified Phase 1 Status Taxonomy is established as:
  - **Compliance Status:** `COMPLIANT`, `NON_COMPLIANT`, `MISSING_EVIDENCE`, `NEEDS_HUMAN_REVIEW`, `NOT_APPLICABLE`.
  - **Government Verification Status:** `VERIFIED`, `UNVERIFIED`, `STALE`, `CONFLICTING`, `INVALID`, `TECHNICAL_UNAVAILABLE`, `MANUAL_FALLBACK`.
  - **Evidence Confidence / Quality:** `HIGH`, `MEDIUM`, `LOW`, `UNREADABLE`.
  - **AI Extraction Confidence:** Numerical float `[0.00 to 1.00]`.
  - **Risk Score:** Numerical composite float `[0.0 to 100.0]` with levels (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
  - **Workflow Status:** `PENDING`, `RUNNING`, `PAUSED_HUMAN_REVIEW`, `COMPLETED`, `FAILED`, `CANCELLED`.
  - **Human Review Status:** `NOT_REQUIRED`, `PENDING_REVIEW`, `IN_REVIEW`, `OVERRIDDEN`, `APPROVED`.

---

### 2.4 Procurement Officer vs. Senior Reviewer Role Boundaries
- **Category:** Inconsistent Role Names & Authorization Scopes
- **Severity:** `LOW`
- **Description:** Task 1 (§4.2) referred generally to "Procurement Officer". Task 8 (§4.2) introduced explicit RBAC roles: `PROCUREMENT_OFFICER`, `SENIOR_REVIEWER`, `AUDITOR`, `SYSTEM_ADMIN`. Task 11 (§4.4) UI workspace designated dual-control override permissions for rules flagged as `CRITICAL_ELIGIBILITY`.
- **Affected Tasks:** Task 1 §4.2, Task 8 §4.2, Task 11 §4.4
- **Authoritative Resolution:** Task 8 RBAC matrix is the single authoritative source. `PROCUREMENT_OFFICER` can execute standard overrides and sign final qualification decisions. `SENIOR_REVIEWER` approval is required ONLY when overriding a `CRITICAL_ELIGIBILITY` rule (e.g., Debarment/Blacklisting status).

---

### 2.5 Container Compute Specification vs. Deployment Portability
- **Category:** Deployment Assumptions / Portability Boundary
- **Severity:** `INFORMATIONAL` (Re-validated)
- **Description:** Task 10 (§3.1) specified AWS ECS Fargate container deployment. Review verified that this does not create a vendor lock-in dependency that breaks container portability.
- **Affected Tasks:** Task 1 §8.1, Task 10 §3.1
- **Authoritative Resolution:** AWS ECS Fargate is established strictly as a **Reference Deployment Architecture**. The application architecture (FastAPI backend, Celery workers, React frontend) is packaged into standard OCI-compliant Docker containers (Task 10 §4.1) and remains 100% portable to Kubernetes (EKS/AKS), Red Hat OpenShift, or on-premises Docker Swarm.

---

### 2.6 Document Retention & Legal Hold Policy Terminology
- **Category:** Inconsistent Retention Language
- **Severity:** `INFORMATIONAL`
- **Description:** Task 2 (§9.1) stated bidder documents are retained for "8 years per CVC guidelines". Task 8 (§8.2) specified "7 years standard, with automated Legal Hold extension".
- **Affected Tasks:** Task 2 §9.1, Task 8 §8.2
- **Authoritative Resolution:** Task 8 §8.2 is authoritative: Base retention is configured via parameter `CONFIG_RETENTION_PERIOD_YEARS` (default: 8 years to satisfy CVC/CPCL maximum guidelines), with an explicit API lock flag `legal_hold_active = True` to halt automated deletion when under investigation.

---

### 2.7 Verification of Other Inconsistency Categories

| Inconsistency Category | Finding Status | Details |
| :--- | :--- | :--- |
| **Contradictory Terminology** | None Found | Core terms (`Tender`, `BidSubmission`, `EvidenceRecord`) are uniform. |
| **Duplicate Responsibilities** | None Found | Clear component boundaries between AI, Rules Engine, and Govt Adapters. |
| **Inconsistent Security Boundaries** | None Found | Task 8 and Task 11 uniformly treat Backend as sole authz boundary. |
| **Inconsistent AI Authority** | None Found | `is_authoritative = False` strictly enforced across Tasks 1–11. |
| **Inconsistent Risk Semantics** | None Found | Risk score is uniformly non-qualifying and advisory across all tasks. |
| **Inconsistent Versioning** | None Found | `TenderVersion` and `PolicyVersion` maintain append-only semantics. |
| **Unsupported Claims** | None Found | No zero-trust PKI or automatic legal qualification claims exist. |
| **Implementation Commitments** | None Found | All tasks remain 100% design/specification only. |

---

## 3. Conclusion & Risk Summary

No `CRITICAL` or `HIGH` architectural inconsistencies exist across the Phase 1 specifications. The minor `MEDIUM` and `LOW` terminology and taxonomy refinements documented above are formally resolved via Task 12 and ADR-108. The Phase 1 architecture is fully coherent and integrated.
