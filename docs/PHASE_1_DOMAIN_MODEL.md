# Phase 1 Domain Model Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-006  
**Version:** 1.1.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines domain entity specifications, conceptual relationships, bounded context boundaries, and domain rules. No application source code, ORM models, database migrations, API controllers, Docker containers, or dependency manifests are created.

---

## 1. Overview & Core Philosophy

The domain model for the SIH 26100 platform establishes a normalized, auditable, and domain-driven design (DDD) structure for evaluating tender compliance in public procurement at Chennai Petroleum Corporation Limited (CPCL).

The domain model derives strictly from the frozen Phase 0 ground truth and Phase 1 Task 1 Architecture Constitution. It enforces strict separation between raw artifacts, interpreted data, authoritative external verifications, evidence records, deterministic evaluation outputs, analytical risk scores, human officer decisions, and tamper-evident audit logs.

---

## 2. Core Operational Axiom

$$\text{AI INTERPRETS} \longrightarrow \text{AUTHORIZED SOURCES VERIFY} \longrightarrow \text{RULES EVALUATE} \longrightarrow \text{EVIDENCE PROVES} \longrightarrow \text{HUMAN APPROVES}$$

Every domain entity and relationship in this model enforces this pipeline. System automation performs extraction, verification, evaluation, and evidence assembly, but the Human Procurement Officer maintains sole legal authority for final qualification and award decisions.

---

## 3. The 7 Critical Domain Separations

To prevent data corruption, audit ambiguity, or legal non-compliance, the domain model explicitly separates 7 core operational concepts into distinct entity boundaries. They MUST NOT be collapsed into generic or polymorphic single-table abstractions.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    THE 7 CRITICAL DOMAIN SEPARATIONS                        │
├──────────────────────────┬──────────────────────────────────────────────────┤
│ 1. SOURCE DOCUMENT       │ Original raw file uploaded (PDF, JPEG, TIFF)     │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 2. DOCUMENT EXTRACTION   │ AI/OCR interpretation of layout & field data     │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 3. GOVT VERIFICATION     │ Response returned by authorized government source│
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 4. EVIDENCE              │ Traceable, immutable proof linking data to rules │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 5. COMPLIANCE RESULT     │ Deterministic evaluation of a requirement threshold│
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 6. RISK ASSESSMENT       │ Independent analytical risk score & anomaly flags │
├──────────────────────────┼──────────────────────────────────────────────────┤
│ 7. OFFICER DECISION      │ Final human procurement officer decision & reason│
└──────────────────────────┴──────────────────────────────────────────────────┘
```

### Detailed Rationale for Domain Separations:

1. **Source Document vs. Document Extraction:**  
   The source document represents the unalterable physical upload stream (with SHA-256 file hash). The document extraction represents an AI/OCR model's *interpretation* of that document at a specific point in time using a specific model version. If the AI model is upgraded or re-run, a new `DocumentExtraction` record is created without mutating the underlying `SourceDocument`.

2. **Document Extraction vs. Government Verification:**  
   Extracted text (e.g., a PAN number read from a scanned PDF) is unverified bidder claim data. Government verification represents an independent, timestamped verification payload returned from an authorized government gateway (e.g., Protean OPV API or DigiLocker). Combining extracted document text with government API responses destroys data provenance.

3. **Government Verification vs. Evidence:**  
   Verification payloads are raw external responses. An `Evidence` entity is a specialized domain object that explicitly binds an extracted value or verified government payload to a specific `TenderRequirement` and `ComplianceRule`, capturing page numbers, bounding boxes `[x0, y0, x1, y1]`, and cryptographic payload hashes.

4. **Evidence vs. Compliance Result:**  
   Evidence is supporting proof. A `ComplianceResult` is the output of the deterministic Python rule engine comparing evidence parameters against requirement thresholds, generating an itemized status (`PASS`, `FAIL`, `REVIEW`, `MISSING`, `EXPIRED`, `CONFLICT`, `NOT_VERIFIED`, `NOT_APPLICABLE`).

5. **Compliance Result vs. Risk Assessment:**  
   Compliance Result represents binary or categorical requirement fulfillment. A `RiskAssessment` is a separate analytical dimension evaluating anomaly indicators, data conflict alerts, verification failures, suspicious document patterns, and vendor risk. A compliance failure sets `Qualification Outcome = NOT COMPLIANT`, but does NOT dictate the Risk Score.

6. **Compliance Result / Risk Assessment vs. Officer Decision:**  
   Rule outputs and risk scores are decision-support recommendations. An `OfficerDecision` represents the legally binding choice recorded by a named procurement officer (`QUALIFY`, `DISQUALIFY`, `SEEK_CLARIFICATION`), requiring a mandatory rationale string and cryptographic sign-off.

7. **Application Audit vs. Domain Records:**  
   Business records (`Tender`, `Bidder`, `Submission`) track domain state. `AuditEvent` records system actions in an append-only, tamper-evident SHA-256 hash-chained ledger separate from business domain tables.

---

## 4. Multi-Rule Requirement & Multi-Attempt Verification Domain Relationships

### 4.1 Tender Requirement to Compliance Rule Junction (`1 -> N -> 1`)
A single tender requirement (e.g. "Techno-Commercial Financial Qualification") may mandate multiple deterministic rules (e.g., Turnover Threshold Rule AND Net Worth Rule AND Solvency Ratio Rule).

```
┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
│   TENDER_REQUIREMENT    │ 1   N │  REQUIREMENT_RULE_MAP   │ N   1 │     COMPLIANCE_RULE     │
│                         ├──────►│                         ├──────►│                         │
│ • requirement_code      │       │ • rule_priority_order   │       │ • rule_expression       │
│ • description           │       │ • is_mandatory_for_req  │       │ • policy_version_id     │
└─────────────────────────┘       └─────────────────────────┘       └─────────────────────────┘
```
- **Rule Priority & Ordering:** Rules within a requirement are evaluated in sequence based on `rule_priority_order`.
- **Applicability & Versioning:** Each mapped rule references a deterministic `ComplianceRule` linked to an immutable `PolicyVersion`.

### 4.2 Government Verification Attempt Tracking (`1 -> N -> 1`)
External government verification lookups may experience transient timeouts, network retries, rate limits, or error states. The model explicitly separates the initial request from individual execution attempts and final response payloads to preserve historical attempt records without overwriting past attempts.

```
┌───────────────────────────┐     ┌───────────────────────────┐     ┌───────────────────────────┐
│   VERIFICATION_REQUEST    │ 1 N │   VERIFICATION_ATTEMPT    │ 1 1 │    VERIFICATION_RESULT    │
│                           ├────►│                           ├────►│                           │
│ • bidder_id               │     │ • attempt_number          │     │ • status (VERIFIED/ERROR) │
│ • identifier_type         │     │ • execution_mode          │     │ • raw_payload             │
│ • identifier_value        │     │ • HTTP status / error     │     │ • payload_hash            │
└───────────────────────────┘     └───────────────────────────┘     └───────────────────────────┘
```
- **Retry Preservation:** Every retry produces a new `VerificationAttempt` record with incremented `attempt_number` and timestamp, preserving complete history of timeouts, errors, and fallback transitions.

---

## 5. Pre-AI Data Protection & Privacy Pipeline

To ensure legal compliance under the Digital Personal Data Protection (DPDP) Act 2023 and prevent uncontrolled transmission of sensitive documents to cloud LLMs, all document ingestion passes through a multi-stage Pre-AI Data Protection Pipeline:

```
┌──────────────┐     ┌────────────────┐     ┌─────────────────────┐     ┌───────────────────┐
│ SOURCE FILE  │──►  │ CLASSIFICATION │──►  │ SENSITIVITY ASSESS  │──►  │ PII POLICY ENGINE │
└──────────────┘     └────────────────┘     └─────────────────────┘     └───────────────────┘
                                                                                  │
┌──────────────┐     ┌────────────────┐     ┌─────────────────────┐               │
│ AI PROVIDER  │◄──  │ AI ELIGIBILITY │◄──  │ DETERMINISTIC REDACT│◄──────────────┘
└──────────────┘     └────────────────┘     └─────────────────────┘
```

1. **Document Classification:** Identifies document category (e.g. Tax Invoice, Master Data PDF, Personal ID Copy).
2. **Sensitivity Assessment:** Rates document privacy risk. High-risk personal documents (e.g., passport copies, personal bank passbooks) are flagged.
3. **PII Detection & Policy Check:** Combines structured pattern detection (regex, dictionary matching) and document-type rules.
4. **Deterministic Redaction:** Redacts personal Aadhaar numbers, personal phone numbers, and individual bank details.
5. **External-AI Eligibility Check:** Evaluates whether document text is eligible for external cloud AI (Gemini/OpenAI) or MUST be restricted to local offline AI (Ollama Qwen) or blocked completely from AI processing.
6. **Human Review Trigger:** If sensitivity exceeds safe thresholds, document is routed to officer human review prior to any LLM processing.

---

## 6. Bounded Context Breakdown

The domain model is organized into **11 Bounded Contexts** encapsulating all 23 system modules established in Task 1.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         11 BOUNDED CONTEXTS                                 │
├───────────────────────────────────┬─────────────────────────────────────────┤
│ BC-1: Organization & Tenant       │ Users, Roles, Departments, Permissions   │
│ BC-2: Tender Management           │ Tenders, TenderVersions, Corrigenda     │
│ BC-3: Requirement & Rule          │ Requirements, RequirementRuleMaps, Rules│
│ BC-4: Bidder & Submission         │ Bidders, Identifiers, Submissions       │
│ BC-5: Document & OCR Intelligence │ SourceDocuments, Extractions, OCR Tokens │
│ BC-6: Government Verification     │ Requests, Attempts, Results, Adapters   │
│ BC-7: Evidence & Provenance       │ EvidenceRecords, Links, EvidenceHashes  │
│ BC-8: Evaluation & Risk           │ ComplianceResults, Outcomes, RiskScores │
│ BC-9: Officer Decision Workflow   │ OfficerDecisions, ManualOverrides       │
│ BC-10: Audit & Security Integrity │ AuditEvents, HashChainBlocks            │
│ BC-11: System Configuration       │ IntegrationConfigs, Mode Routing Rules │
└───────────────────────────────────┴─────────────────────────────────────────┘
```

---

## 7. Entity Complexity & MVP Classification Matrix

Every entity in the domain model is classified to maintain **minimum necessary complexity** for the MVP while preserving enterprise architectural integrity:

| Entity Name | Bounded Context | MVP Classification | Functional Justification |
| :--- | :--- | :--- | :--- |
| `organizations` | BC-1 | **CORE MVP** | Multi-tenant organization boundaries |
| `departments` | BC-1 | **CORE MVP** | CPCL department routing and access control |
| `users` | BC-1 | **CORE MVP** | Procurement officer profiles & authentication |
| `roles` & `user_roles` | BC-1 | **CORE MVP** | RBAC permission enforcement |
| `tenders` | BC-2 | **CORE MVP** | Tender parent entity |
| `tender_versions` | BC-2 | **CORE MVP** | Corrigenda versioning & deadline tracking |
| `tender_cover_definitions`| BC-2 | **CORE MVP** | Multi-cover tender separation (Fee/Tech/Fin) |
| `tender_requirements` | BC-3 | **CORE MVP** | Eligibility criteria definitions |
| `requirement_rule_maps` | BC-3 | **CORE MVP** | Junction linking requirements to N rules |
| `compliance_rules` | BC-3 | **CORE MVP** | Deterministic Pydantic rule expressions |
| `policy_versions` | BC-3 | **CORE MVP** | Regulatory policy versioning (MII/MSE) |
| `bidders` | BC-4 | **CORE MVP** | Bidder legal entity profiles |
| `bidder_identities` | BC-4 | **CORE MVP** | Child registration identifiers (PAN/GSTIN/CIN) |
| `bid_submissions` | BC-4 | **CORE MVP** | Bidder submission participation records |
| `submission_covers` | BC-4 | **CORE MVP** | Submitted cover containers |
| `source_documents` | BC-5 | **CORE MVP** | Uploaded file blobs & SHA-256 hashes |
| `document_extractions` | BC-5 | **CORE MVP** | AI/OCR extraction run metadata |
| `extracted_fields` | BC-5 | **CORE MVP** | Extracted field key-value pairs |
| `bounding_boxes` | BC-5 | **CORE MVP** | PDF page overlay coordinates `[x0,y0,x1,y1]` |
| `verification_requests` | BC-6 | **CORE MVP** | Government lookup job triggers |
| `verification_attempts` | BC-6 | **CORE MVP** | Historical retry and timeout tracking |
| `verification_results` | BC-6 | **CORE MVP** | Provenance-tagged external payloads |
| `evidence_records` | BC-7 | **CORE MVP** | Immutable evidence linking rules to proof |
| `compliance_evaluations` | BC-8 | **CORE MVP** | Itemized requirement pass/fail results |
| `qualification_outcomes` | BC-8 | **CORE MVP** | Overall bidder qualification outcome |
| `risk_assessment_profiles`| BC-8 | **CORE MVP** | Independent analytical risk scores |
| `risk_factor_signals` | BC-8 | **SUPPORTING MVP**| Granular risk factor breakdown signals |
| `officer_decisions` | BC-9 | **CORE MVP** | Sealed human qualification decisions |
| `manual_overrides` | BC-9 | **CORE MVP** | Officer status override rationale records |
| `audit_events` | BC-10 | **CORE MVP** | Application infrastructure audit logs |
| `audit_hash_chain_blocks`| BC-10 | **CORE MVP** | SHA-256 tamper-evident hash blocks |
| `system_configurations` | BC-11 | **SUPPORTING MVP**| Global integration adapter mode toggles |
| `tender_clause_embeddings`| BC-2/BC-3 | **FUTURE / RESERVED**| Optional semantic vector search (RAG) |
