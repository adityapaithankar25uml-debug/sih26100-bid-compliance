# Phase 8 — Final Solution Architecture & Layered System Design

## Executive Architectural Summary

The **SIH26100 Platform** is built upon an evidence-first, deterministic, human-authoritative architecture engineered for public procurement workflows on government portals like GeM (Government e-Marketplace).

### The Core Architectural Axiom
> **AI INTERPRETS → SOURCES VERIFY → RULES EVALUATE → EVIDENCE PROVES → RISK PRIORITIZES → HUMAN DECIDES → AUDIT REMEMBERS**

---

## High-Level Layered Architecture Diagram

```
+-----------------------------------------------------------------------------------+
| 1. USER INTERFACE LAYER (Next.js 14, React 18, Vanilla CSS, Tailwind, Lucide)     |
|    - Dashboard Command Center | Tender Catalog | Bid Workspace | Verification     |
|    - Evidence Explorer | Advisory Risk Panel | Human Review Queue | Audit Explorer |
+-----------------------------------------------------------------------------------+
                                         │ (HTTPS REST API / JSON)
                                         ▼
+-----------------------------------------------------------------------------------+
| 2. API & SECURITY GATEWAY LAYER (FastAPI, OAuth2, JWT, RBAC, Problem Details)    |
|    - Auth Router | Tender Router | Submission Router | Verification Router        |
|    - Human Review Router | Risk Router | Audit Router | Middleware (Correlation) |
+-----------------------------------------------------------------------------------+
                         │                                    │
                         ▼                                    ▼
+------------------------------------+  +--------------------------------------------+
| 3. DOCUMENT INTELLIGENCE & AI      |  | 4. GOVERNMENT ADAPTER LAYER                |
|    - Upload Validator (Magic-Bytes) |  |    - Normalized Adapter Interface           |
|    - Pattern-Based PII Redactor    |  |    - 12 Government Portal Adapters          |
|    - Structured AI Gateway Parser  |  |      (GST, Udyam, PAN, EPFO, ESIC, MII,    |
|    - Text / Bounding Box Extractor |  |       Debarment, OEM, DigiLocker, etc.)     |
+------------------------------------+  +--------------------------------------------+
                         │                                    │
                         +-----------------+------------------+
                                           │
                                           ▼
+-----------------------------------------------------------------------------------+
| 5. EVIDENCE & DETERMINISTIC COMPLIANCE CORE ENGINE                                |
|    - 9-Dimension Evidence Model (Authority, Freshness, Integrity, Lineage)       |
|    - Deterministic Rule Evaluation Matrix (Boolean logic evaluation)              |
|    - Point-in-time Evaluation Snapshots (SHA-256 state hashes)                     |
+-----------------------------------------------------------------------------------+
                                           │
                                           ▼
+-----------------------------------------------------------------------------------+
| 6. ADVISORY RISK & HUMAN REVIEW WORKSPACE LAYER                                   |
|    - Advisory Risk Engine (Scoring, Signal Aggregation, Prioritization)           |
|    - Human Review Officer Queue (Task assignment, resolution tracking)            |
|    - Non-Destructive Manual Overrides & Four-Eyes Policy Threshold Engine         |
+-----------------------------------------------------------------------------------+
                                           │
                                           ▼
+-----------------------------------------------------------------------------------+
| 7. TAMPER-EVIDENT SHA-256 AUDIT HASH CHAIN LAYER                                  |
|    - Canonical Event Hashing (SHA-256)                                            |
|    - Prev_Hash Linked Block Lineage & Automated Verification                      |
+-----------------------------------------------------------------------------------+
                                           │
                                           ▼
+-----------------------------------------------------------------------------------+
| 8. DATA & INFRASTRUCTURE LAYER                                                    |
|    - PostgreSQL 16 (Relational Metadata & Audit Store)                            |
|    - Redis 7 & Celery (Asynchronous Task Queue & Caching)                          |
|    - MinIO Object Storage (Secure Document Vault & Quarantine)                    |
+-----------------------------------------------------------------------------------+
```

---

## Detailed System Component Description

### Layer 1: User Interface Layer
- **Tech Stack:** Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide icons.
- **Design Philosophy:** Sleek, high-density government portal aesthetic with role-aware UI navigation.
- **Key Modules:**
  - `Command Center Dashboard` (`/dashboard`): Overview of active tenders, submissions, pending review queues, and audit chain verification status.
  - `Bid Verification Workspace` (`/bids/[id]`): Multi-tab officer workspace containing Bidder 360, Document Extractions, Deterministic Compliance Matrix, Evidence Provenance, and Officer Decision panels.
  - `Government Verification Center` (`/verification`): Status matrix for 12 statutory government registries with explicit `MOCK / DEMO` integration badges.
  - `Evidence Explorer` (`/evidence`): Visualization of 9 independent evidence quality dimensions and lineage graph nodes.
  - `Tamper-Evident SHA-256 Audit Hash Chain Explorer` (`/audit`): Interactive verification tool executing block-by-block hash lineage validation.

### Layer 2: API & Security Gateway Layer
- **Tech Stack:** FastAPI (Python 3.10+), Pydantic v2, OAuth2 with Password Bearer, PyJWT.
- **Key Principles:**
  - Role-Based Access Control (RBAC): 7 predefined system roles (`ProcurementOfficer`, `SeniorReviewer`, `ComplianceOfficer`, `SystemAdmin`, `Auditor`, `Bidder`, `ServiceWorker`).
  - RFC 7807 Problem Details for standard error responses.
  - Middleware tracing for request correlation (`X-Correlation-ID`) and idempotency (`X-Idempotency-Key`).

### Layer 3: Document Intelligence & AI Gateway
- **Tech Stack:** PyMuPDF, Python text parsers, Pattern Redactor, AI Gateway Abstraction (`app/services/ai_gateway.py`).
- **Security & Privacy Safeguards:**
  - Upload magic-byte validation and malware scan abstraction.
  - Deterministic detection and redaction patterns for configured sensitive data categories before external AI processing.
  - Schema-enforced JSON structured output parser.
  - Advisory classification: AI extraction is advisory. Deterministic compliance rules evaluate structured facts. Evidence and provenance support the evaluation. The authorized human officer retains final procurement decision authority.

### Layer 4: Government Verification Adapter Layer
- **Architecture:** Standardized `GovernmentSourceAdapter` abstract interface.
- **12 Supported Statutory Registries:** GST, Udyam/MSME, PAN, MCA, EPFO, ESIC, DPIIT Startup India, NSIC, OEM Authorization, DigiLocker, Central Debarment List, GeM Seller Profile.
- **Resilience Safeguards:** Transport failures or API timeouts generate human review tasks rather than automatic disqualifications.

### Layer 5: Evidence & Deterministic Compliance Core Engine
- **Deterministic Rule Matrix:** Boolean rule evaluation (e.g., `turnover >= required_turnover`, `local_content_pct >= minimum_mii_pct`) for qualification checks.
- **9 Independent Evidence Quality Dimensions:** `source_authority`, `source_freshness`, `completeness`, `integrity_hash_validity`, `identity_linkage`, `document_authenticity`, `temporal_applicability`, `extraction_provenance`, `consistency`.
- **Evaluation Snapshots:** Point-in-time state records with SHA-256 hashes generated prior to any manual officer action.

### Layer 6: Advisory Risk & Human Review Workspace Layer
- **Advisory Risk Engine:** Calculates overall risk scores and signals for prioritization. Risk score is strictly advisory and cannot auto-disqualify.
- **Officer Decision Authority:** Authoritative human decision module where Procurement Officers record formal findings (`QUALIFIED`, `DISQUALIFIED`, `REQUIRES_CLARIFICATION`, `EVIDENCE_REQUESTED`).
- **Non-Destructive Manual Overrides & Four-Eyes Policy:** Manual rule overrides are recorded in a separate table (`ManualOverride`), preserving original rule results. Overrides exceeding threshold criteria enforce dual-officer approval (`PENDING_FOUR_EYES`).

### Layer 7: Tamper-Evident SHA-256 Audit Hash Chain Layer
- **Architecture:** Canonical JSON event logging where each audit event includes actor, role, action, resource, timestamp, payload, and a SHA-256 hash incorporating the previous event's hash (`prev_hash`).
- **Integrity Verification:** Automated block-by-block hash verification algorithm validates chain lineage and flags any historical tampering.

---

## Architectural Rationale

1. **Deterministic Rule Evaluation:** Qualification rules perform boolean evaluation without non-deterministic AI variance.
2. **Human-in-the-Loop Authority:** Procurement decisions carry statutory responsibility. Our platform maintains full human decision authority with non-destructive audit lineage.
3. **Structured Data Isolation:** Extracted text snippets pass through schema validation and deterministic rule logic.
