# Phase 1 Domain Model Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-006  
**Version:** 1.0.0  
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

## 4. Bounded Context Breakdown

The domain model is organized into **11 Bounded Contexts** encapsulating all 23 system modules established in Task 1.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         11 BOUNDED CONTEXTS                                 │
├───────────────────────────────────┬─────────────────────────────────────────┤
│ BC-1: Organization & Tenant       │ Users, Roles, Departments, Permissions   │
│ BC-2: Tender Management           │ Tenders, TenderVersions, Corrigenda     │
│ BC-3: Requirement & Rule          │ TenderRequirements, Rules, PolicyVersions│
│ BC-4: Bidder & Submission         │ Bidders, Identifiers, Submissions       │
│ BC-5: Document & OCR Intelligence │ SourceDocuments, Extractions, OCR Tokens │
│ BC-6: Government Verification     │ VerificationRequests, Results, Adapters │
│ BC-7: Evidence & Provenance       │ EvidenceRecords, Links, EvidenceHashes  │
│ BC-8: Evaluation & Risk           │ ComplianceResults, Outcomes, RiskScores │
│ BC-9: Officer Decision Workflow   │ OfficerDecisions, ManualOverrides       │
│ BC-10: Audit & Security Integrity │ AuditEvents, HashChainBlocks            │
│ BC-11: System Configuration       │ IntegrationConfigs, Mode Routing Rules │
└───────────────────────────────────┴─────────────────────────────────────────┘
```

### BC-1: Organization & Tenant Bounded Context
- **Aggregates:** `Organization` (Tenant Root), `Department`, `User` (User Root), `Role`.
- **Entities:** `Organization`, `Department`, `User`, `Role`, `Permission`, `UserRole`.
- **Responsibility:** Manages organizational hierarchy, user profiles, RBAC assignments, and multi-tenant access boundaries for CPCL departments.

### BC-2: Tender Management Bounded Context
- **Aggregates:** `Tender` (Tender Aggregate Root), `TenderVersion`.
- **Entities:** `Tender`, `TenderVersion`, `TenderCorrigendum`, `TenderCoverDefinition`.
- **Domain Rule:** Tenders are parent container entities. Every publication or corrigendum creates a new immutable `TenderVersion`. Requirements and rules MUST link to a specific `TenderVersion`, ensuring historical point-in-time explainability when corrigenda alter eligibility criteria.

### BC-3: Requirement & Rule Bounded Context
- **Aggregates:** `TenderRequirement` (Requirement Root), `ComplianceRule`, `PolicyVersion`.
- **Entities:** `TenderRequirement`, `ComplianceRule`, `PolicyVersion`, `RequirementRuleMap`.
- **Domain Rule:** AI requirement extractions create `TenderRequirement` proposals marked as `UNCONFIRMED`. Procurement officers must explicitly confirm requirement schemas before activation. Rules link to immutable `PolicyVersion` definitions (e.g., PPP-MII Order 2017/2024).

### BC-4: Bidder & Submission Bounded Context
- **Aggregates:** `Bidder` (Bidder Root), `BidSubmission` (Submission Root).
- **Entities:** `Bidder`, `BidderIdentity`, `BidSubmission`, `SubmissionCoverManifest`.
- **Domain Rule:** Bidders are legal entities identified by an immutable internal ULID. PAN, GSTIN, CIN, and Udyam are child `BidderIdentity` records. A Bidder can submit to multiple Tenders; a Tender receives multiple Bidders. This N:M relationship is captured by `BidSubmission`.

### BC-5: Document & OCR Intelligence Bounded Context
- **Aggregates:** `SourceDocument` (Document Root), `DocumentExtraction`.
- **Entities:** `SourceDocument`, `DocumentExtraction`, `ExtractedField`, `BoundingBoxCoordinate`.
- **Domain Rule:** `SourceDocument` stores file metadata, SHA-256 checksums, and MinIO storage URIs. `DocumentExtraction` captures AI/OCR model runs, extracted text tokens, confidence scores, and bounding box coordinates `[x0, y0, x1, y1]`.

### BC-6: Government Verification Bounded Context
- **Aggregates:** `GovernmentVerificationRequest` (Verification Root).
- **Entities:** `GovernmentVerificationRequest`, `GovernmentVerificationResult`, `VerificationAdapterLog`.
- **Domain Rule:** Captures external government lookups across GSTN, PAN, MCA, Udyam, etc. Every record retains provenance: runtime mode (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`), source authority, raw payload, and response timestamp.

### BC-7: Evidence & Provenance Bounded Context
- **Aggregates:** `EvidenceRecord` (Evidence Root).
- **Entities:** `EvidenceRecord`, `EvidenceLink`, `EvidenceHashLedger`.
- **Domain Rule:** First-class domain object answering "What proves this compliance evaluation?". Connects requirement evaluation to document bounding boxes or API verification payloads with cryptographic SHA-256 hashes. Evidence is append-only; corrections create new evidence records.

### BC-8: Evaluation & Risk Bounded Context
- **Aggregates:** `ComplianceEvaluation` (Evaluation Root), `RiskProfile`.
- **Entities:** `RequirementComplianceResult`, `SubmissionQualificationOutcome`, `EvidenceConfidenceScore`, `RiskAssessmentProfile`, `RiskFactorSignal`.
- **Domain Rule:** Evaluates requirement compliance deterministically (`PASS`, `FAIL`, `REVIEW`, etc.) and determines `Qualification Outcome` (`COMPLIANT`, `NOT COMPLIANT`, `PROVISIONAL`). `RiskAssessmentProfile` computes analytical risk scores (0.0 to 100.0) independently. Risk score CANNOT independently qualify/disqualify a bidder.

### BC-9: Officer Decision Workflow Bounded Context
- **Aggregates:** `OfficerDecision` (Decision Root).
- **Entities:** `OfficerDecision`, `ManualOverrideRecord`, `OfficerDecisionSnapshot`.
- **Domain Rule:** Records final human qualification decisions (`QUALIFY`, `DISQUALIFY`, `SEEK_CLARIFICATION`). Requires mandatory justification rationale text for overrides. Sealed into the audit log.

### BC-10: Audit & Security Integrity Bounded Context
- **Aggregates:** `AuditEvent` (Audit Root).
- **Entities:** `AuditEvent`, `AuditHashChainBlock`.
- **Domain Rule:** Append-only tamper-evident log using SHA-256 hash chaining (`Block_n = SHA256(Block_{n-1} + Timestamp + Actor + Payload)`). Provides undeniable mathematical proof of tampering.

### BC-11: System & Integration Configuration Bounded Context
- **Aggregates:** `SystemConfiguration`.
- **Entities:** `SystemConfiguration`, `GovernmentSourceConfig`, `AdapterModeRouting`.
- **Domain Rule:** Controls integration adapter modes per domain, global rate limits, and system parameters.

---

## 5. Temporal Explainability & Versioning Model

The domain model guarantees **historical explainability**. An evaluation performed on a given date remains 100% reproducible even if tenders, policies, rules, government data, or bidder attributes change over time.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     POINT-IN-TIME EXPLAINABILITY MODEL                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. TenderVersion       ──► Locks tender eligibility criteria on publication  │
│ 2. PolicyVersion       ──► Locks regulatory policy (e.g., MII Order 2017)   │
│ 3. ComplianceRule      ──► Versioned deterministic expression schema         │
│ 4. DocumentExtraction  ──► Locked OCR model version & prompt version         │
│ 5. VerificationResult  ──► Timestamped snapshot of API response payload     │
│ 6. EvidenceRecord      ──► Cryptographically hashed proof snapshot           │
│ 7. OfficerDecision     ──► Sealed decision snapshot at time of sign-off      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Module Data Ownership & Prohibitions Matrix

| System Module (MOD) | Primary Data Ownership (Entities) | Read Access Rights | Strict Data Prohibitions (MUST NOT) |
| :--- | :--- | :--- | :--- |
| **MOD-001 Auth** | `users`, `user_roles`, `permissions` | All modules (token validation) | MUST NOT modify tenders or evaluate rules |
| **MOD-003 Tender** | `tenders`, `tender_versions`, `corrigenda` | All modules | MUST NOT execute AI extraction or evaluate bidders |
| **MOD-004 Req Intel** | `proposed_requirements` | Tender Module, Rule Engine | MUST NOT auto-confirm rules without human sign-off |
| **MOD-005 Doc Mgr** | `source_documents` | Doc Intel, Evidence Ledger | MUST NOT parse text or execute OCR logic |
| **MOD-006 Doc Intel** | `document_extractions`, `extracted_fields` | Rule Engine, Evidence Ledger | MUST NOT compare numbers against rules or assign PASS/FAIL |
| **MOD-007 Bidder** | `bidders`, `bidder_identities`, `bid_submissions` | Verification Gateway, Rule Engine | MUST NOT execute government verifications or score eligibility |
| **MOD-009 Govt Gateway**| `verification_requests`, `verification_results` | Rule Engine, Evidence Ledger | MUST NOT bypass government approval or present mocks as live |
| **MOD-012 Rule Engine** | `compliance_results`, `qualification_outcomes` | Risk Engine, Decision Workflow | MUST NOT use non-deterministic LLM logic for evaluation |
| **MOD-014 Risk Engine** | `risk_profiles`, `risk_factors` | Decision Workflow | MUST NOT allow risk score to determine qualification status |
| **MOD-017 Evidence** | `evidence_records`, `evidence_links` | Decision Workflow, Audit Module | MUST NOT allow UPDATE or DELETE of committed evidence |
| **MOD-018 Audit Logger**| `audit_events`, `audit_hash_chain` | Auditor Dashboard | MUST NOT support UPDATE or DELETE on audit logs |
| **MOD-019 Officer Decision**| `officer_decisions`, `manual_overrides` | Reporting Module, Audit Module | MUST NOT allow decision sign-off without mandatory rationale |
