# Phase 1 Architecture Constitution

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Category:** Software | **Theme:** Smart Automation  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-001  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines architectural principles, module boundaries, interface specifications, data contracts, and governance rules. No application source code, database migrations, API clients, Docker containers, or dependency installations are authorized or created during Task 1.

---

## 1. Primary Objective & Architectural Mandate

The primary objective of the SIH 26100 platform is to provide Chennai Petroleum Corporation Limited (CPCL) procurement officers with an auditable, evidence-backed, AI-assisted bid compliance evaluation system for public procurement tenders published on GeM and NIC e-procurement portals.

This Architecture Constitution establishes the non-negotiable technical principles, structural boundaries, integration abstraction rules, and decision-making governance for the entire platform.

All designs in Phase 1 derive directly from the frozen Phase 0 ground truth baseline.

---

## 2. Non-Negotiable Core Principle

```
AI INTERPRETS → AUTHORIZED SOURCES VERIFY → RULES EVALUATE → EVIDENCE PROVES → HUMAN PROCUREMENT OFFICER APPROVES
```

The system operates as a **Human-in-the-Loop Decision Support System**, not an autonomous decision-making engine.

---

## 3. Explicit AI Prohibitions (MUST NOT)

To maintain compliance with Central Vigilance Commission (CVC) procurement guidelines, General Financial Rules (GFR 2017), and the Information Technology Act 2000, the AI subsystem is subject to strict operational boundaries:

1. **Qualification Decisions:** AI MUST NOT independently qualify or disqualify any bidder.
2. **Rule Modification:** AI MUST NOT create, alter, delete, or parameterize compliance rules or Make in India policy thresholds.
3. **Government Verification Fabrication:** AI MUST NOT fabricate, simulate, or mock government verification responses as if they were live data.
4. **Audit Log & Evidence Manipulation:** AI MUST NOT delete, modify, suppress, or re-order audit log entries, document hashes, or evidence records.
5. **Direct System Access:** AI MUST NOT directly call external government APIs or scrape government portals outside the application adapter layer.
6. **Decision Override:** AI MUST NOT override human procurement officer decisions or recommendations.
7. **Silent Execution:** AI MUST NOT auto-action any compliance recommendation without explicit officer review and confirmation.

---

## 4. Architectural Style & Technical Blueprint

### 4.1 Modular Monolith for SIH MVP
The platform architecture is specified as a **Modular Monolith**. 

- **Rationale:** Microservices introduce operational overhead (distributed tracing, network latency, multi-repo synchronization, complex deployment) unsuitable for an SIH hackathon team. A Modular Monolith provides strict domain boundary separation within a single, highly maintainable deployment unit, allowing future extraction into microservices if enterprise scale requires.
- **Enforcement:** Each domain module must maintain strict encapsulation — communicating via internal service interfaces or in-memory event buses, never bypassing database boundaries of other modules.

### 4.2 Core Technology Stack Specification

| Layer | Recommended Technology | Architectural Justification |
|-------|-----------------------|-----------------------------|
| **Application Backend** | Python 3.11+ (FastAPI) | Asynchronous execution, native Pydantic typing for deterministic schemas, deep AI/ML library ecosystem |
| **Presentation Frontend** | Next.js 14+ / React (TypeScript) | Component-driven UI, SSR/SSG capabilities, responsive dashboard layout, strong developer ecosystem |
| **Primary Database** | PostgreSQL 16+ | Strong ACID compliance for decision workflows, native JSONB support for document metadata and rule execution traces |
| **Cache & Async Coordinator** | Redis 7+ | Fast session management, verification result caching with TTL, background job queue management |
| **Object Storage** | MinIO / S3-Compatible Storage | Encrypted storage for scanned PDFs and extracted document artifacts with SHA-256 hash validation |
| **AI Provider Layer** | Gemini / OpenAI / Local LLM (Ollama) | Unified provider-agnostic abstraction for OCR token extraction and natural language explanation generation |
| **Integration Layer** | Python Adapter Pattern | Isolation of external government integrations behind uniform `LIVE`, `SANDBOX`, `MOCK`, `MANUAL` interfaces |

---

## 5. Integration Principles & Multi-Tier Gateway Strategy

### 5.1 Government Adapter Abstraction
Every external government data source (GSTN, PAN, MCA, Udyam, EPFO, ESIC, Startup India, NSIC, CPPP, DigiLocker, BIS) MUST be implemented behind an abstracted Adapter Interface.

The application core MUST NEVER depend directly on third-party vendor SDKs or specific government REST endpoints.

```
┌─────────────────────────────────────────────────────────┐
│                 APPLICATION CORE                        │
│         (Rule Engine / Verification Service)            │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│           GOVERNMENT INTEGRATION GATEWAY                │
│  • Uniform Interface: verify(identifier, context)       │
│  • Configurable Routing: LIVE | SANDBOX | MOCK | MANUAL  │
└──────┬──────────────┬──────────────┬──────────────┬─────┘
       │              │              │              │
       ▼              ▼              ▼              ▼
  ┌─────────┐    ┌──────────┐   ┌─────────┐    ┌──────────┐
  │  LIVE   │    │ SANDBOX  │   │  MOCK   │    │ MANUAL   │
  │ ADAPTER │    │ ADAPTER  │   │ ADAPTER │    │ FALLBACK │
  └─────────┘    └──────────┘   └─────────┘    └──────────┘
```

### 5.2 Mandatory Runtime Verification Modes
Each adapter MUST support four runtime modes, configurable per environment and per domain:

1. **`LIVE`**: Direct REST/OAuth 2.0 calls to production government APIs (e.g., Protean OPV for PAN, GSP for GSTN). Requires official entity onboarding.
2. **`SANDBOX`**: Calls to official government developer staging/testing environments (e.g., DigiLocker Sandbox, API Setu Staging).
3. **`MOCK`**: Local deterministic mock services returning pre-configured verification responses for hackathon demos.
4. **`MANUAL`**: Manual verification workflow where procurement officers review uploaded documents and confirm validity.

### 5.3 UI Labeling Mandate
The presentation layer MUST explicitly, visually label the verification provenance on every display card, table cell, and export report:

- 🟢 `[LIVE_VERIFIED]` — Real-time production API response.
- 🟡 `[SANDBOX_VERIFIED]` — Staging sandbox API response.
- 🟠 `[MOCK_SIMULATED]` — Local hackathon mock gateway response.
- 🔵 `[MANUAL_VERIFIED]` — Officer-reviewed document OCR / manual lookup response.

---

## 6. Evidence-First Architecture & Provenance Model

Every compliance result evaluated by the platform MUST be backed by an immutable, cryptographically verifiable evidence chain.

### 6.1 Conceptual Evidence Relationship

$$\text{Tender Requirement} \longrightarrow \text{Compliance Rule} \longrightarrow \text{Document / API Data} \longrightarrow \text{Verification Event} \longrightarrow \text{Compliance Result} \longrightarrow \text{Risk Profile} \longrightarrow \text{Officer Decision}$$

### 6.2 Mandatory Evidence Record Metadata
Every evidence artifact captured by the system MUST contain at minimum:

```json
{
  "evidence_id": "UUID",
  "tender_id": "UUID",
  "bidder_id": "UUID",
  "requirement_id": "UUID",
  "source_type": "DOCUMENT | GOVERNMENT_API | SELF_DECLARATION | OFFICER_NOTE",
  "source_system": "string (e.g., 'developer.gst.gov.in', 'bidder_upload')",
  "document_reference": {
    "file_id": "UUID",
    "file_hash": "SHA-256 string",
    "page_number": "integer",
    "bounding_box": {"x0": 0, "y0": 0, "x1": 100, "y1": 100}
  },
  "extracted_value": "string / json",
  "verified_value": "string / json",
  "verification_mode": "LIVE | SANDBOX | MOCK | MANUAL",
  "compliance_status": "PASS | FAIL | REVIEW | MISSING | EXPIRED | CONFLICT | NOT_VERIFIED | NOT_APPLICABLE",
  "confidence_score": "float (0.0 - 1.0)",
  "timestamp": "ISO-8601 UTC string",
  "evidence_hash": "SHA-256 string",
  "rule_version": "string",
  "verifier_identity": "string (System Component ID or Officer User ID)",
  "audit_reference_id": "UUID"
}
```

---

## 7. Compliance Status Model & State Rules

The compliance rule engine evaluates requirements using the standardized 8-state model established in Phase 0:

| Status | Code | Triggers & Evaluation Conditions |
|--------|------|---------------------------------|
| **PASS** | `PASS` | Extracted & verified data fully satisfies requirement threshold; supporting evidence confirmed. |
| **FAIL** | `FAIL` | Verified data explicitly contradicts requirement (e.g., turnover < threshold, entity debarred). |
| **REVIEW** | `REVIEW` | Evidence submitted, but AI extraction confidence < 0.85 or requirement mandates human officer judgment. |
| **MISSING** | `MISSING` | Mandatory document or field required by tender clause was not submitted by bidder. |
| **EXPIRED** | `EXPIRED` | Document or registration exists, but validity end-date precedes tender evaluation deadline. |
| **CONFLICT** | `CONFLICT` | Identifier or legal parameter contradicts another authoritative source (e.g., GST name != PAN name). |
| **NOT_VERIFIED** | `NOT_VERIFIED` | Document submitted, but external verification endpoint failed, timed out, or returned error. |
| **NOT_APPLICABLE** | `N/A` | Requirement is conditionally excluded for this bidder (e.g., EMD waiver applied to MSE Manufacturer). |

---

## 8. Three-Dimensional Compliance Scoring Model

The architecture explicitly rejects single percentage scoring in favor of a 3-dimensional analytical model:

```
┌─────────────────────────────────────────────────────────┐
│                THREE-DIMENSIONAL RISK MATRIX            │
├───────────────────┬─────────────────────────────────────┤
│ 1. COMPLIANCE     │ % of mandatory & preferred          │
│    SCORE (0-100)  │ requirements evaluated as PASS      │
├───────────────────┼─────────────────────────────────────┤
│ 2. EVIDENCE       │ Weighted confidence & verifiability │
│    CONFIDENCE     │ score of underlying evidence        │
├───────────────────┼─────────────────────────────────────┤
│ 3. RISK SCORE     │ Aggregate risk level from conflicts,│
│    (0-100)        │ missing items, & debarment checks   │
└───────────────────┴─────────────────────────────────────┘
```

### Mandatory Non-Linear Escalation Rule
Regardless of aggregate scores, if **ANY single mandatory requirement** yields a `FAIL` status or a debarment match is detected:
- The **Risk Score** automatically escalates to `100.0 (CRITICAL)`.
- The overall recommendation defaults to `DISQUALIFY`.
- The procurement officer is alerted with a critical compliance red-flag card.

---

## 9. Human-in-the-Loop Governance Workflow

The platform provides a decision-support workbench for CPCL procurement officers:

1. **Evidence Inspection:** Officer views side-by-side split screen showing evaluation findings alongside original PDF documents with bounding-box highlights.
2. **Provenance Traceability:** Officer clicks any value to view the complete API payload or OCR token coordinate snippet.
3. **Authorized Manual Override:** Officer may override any system status (e.g., `FAIL` → `PASS`), requiring entry of a **mandatory non-empty justification rationale**.
4. **Immutable Decision Recording:** The officer records the final status (`QUALIFY`, `DISQUALIFY`, `SEEK_CLARIFICATION`). The decision snapshot, rationale, user ID, timestamp, and evidence state are cryptographically sealed into the audit log.

---

## 10. Security, Privacy (DPDP Act 2023), & Resilience Architecture

### 10.1 Access Control & Privilege Separation
- **Role-Based Access Control (RBAC):** Strict segregation of duties:
  - *Tender Creator:* Can setup tenders and parameterize rules; cannot evaluate.
  - *Procurement Officer:* Can review evaluations, override statuses, and make qualification decisions.
  - *Auditor:* Read-only access to evaluations, evidence chains, and audit logs.
  - *System Administrator:* User management & adapter configuration; zero access to tender evaluations.

### 10.2 DPDP Act 2023 PII Masking Architecture
Before any bidder document or field is transmitted to external AI providers (Gemini / OpenAI API):
- A local deterministic regex redactor masks personal Aadhaar numbers, personal phone numbers, and individual bank account details.
- Only organizational PII (GSTIN, PAN, CIN, Official Corporate Address) necessary for bid evaluation is processed.

### 10.3 Degraded Mode & External Service Resilience
If an external government portal or API fails (timeout, 5xx server error, rate limit):
1. The adapter catches the failure and logs an `IntegrationFailureEvent`.
2. The verification status transitions gracefully to `NOT_VERIFIED` or `MANUAL_FALLBACK`.
3. The system DOES NOT fabricate a `PASS` or `FAIL`.
4. The officer is notified with a option to trigger an async retry or perform a manual web-portal verification.
5. Evaluation of other independent requirements continues uninterrupted (Circuit Breaker Pattern).

---

## 11. Zero Application Code Enforcement Rules

To ensure strict compliance with Phase 1 Task 1 constraints:
- NO application code files (`.py`, `.ts`, `.js`, `.jsx`, `.tsx`, `.sql`, `.html`, `.css`) shall be written in project execution directories.
- NO database migrations or schema execution scripts shall be generated.
- NO package manifests (`package.json`, `requirements.txt`, `pyproject.toml`) shall be initialized.
- NO Dockerfiles, `docker-compose.yml`, or CI/CD pipelines shall be created.
- Architecture artifacts MUST remain strictly in Markdown format under `docs/`.
