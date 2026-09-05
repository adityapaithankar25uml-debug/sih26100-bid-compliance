# 02 — Functional Requirements

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05

---

## FR-01: Tender Management

### FR-01.1: Tender Import
- The system SHALL allow procurement officers to upload tender documents in PDF, DOCX, and scanned-image formats.
- The system SHALL support import of tenders from CPCL's e-procurement portal (manual upload initially).
- The system SHALL support import of corrigenda/amendments linked to a parent tender.

### FR-01.2: Tender Requirement Extraction
- The system SHALL use AI to extract eligibility requirements from uploaded tender documents.
- Each extracted requirement SHALL be classified by category (financial, technical, legal, statutory, experience, local content, declarations).
- Each requirement SHALL indicate: mandatory/preferred, threshold value (if any), evidence type required.
- Each requirement SHALL reference the source clause (section number, page number).
- The system SHALL present extracted requirements to the procurement officer for confirmation, modification, or addition.

### FR-01.3: Corrigendum Management
- The system SHALL track corrigenda/amendments and highlight changes from the original tender.
- The system SHALL re-evaluate affected requirements when a corrigendum is processed.

---

## FR-02: Bidder Management

### FR-02.1: Bidder Registration
- The system SHALL allow procurement officers to add bidders to a tender evaluation.
- Each bidder SHALL have a profile containing: legal name, PAN, GSTIN, CIN/LLPIN, Udyam number, contact details.
- The system SHALL validate identifier formats upon entry (PAN: AAAAA9999A, GSTIN: 15 chars, CIN: 21 chars, Udyam: UDYAM-XX-00-0000000).

### FR-02.2: Entity Resolution
- The system SHALL cross-reference PAN, GSTIN, CIN, and Udyam to verify they belong to the same legal entity.
- The system SHALL flag discrepancies (e.g., PAN embedded in GSTIN doesn't match separately provided PAN).
- The system SHALL support entity name fuzzy matching with confidence scoring.

---

## FR-03: Document Processing

### FR-03.1: Document Upload
- The system SHALL accept bidder documents in PDF, JPEG, PNG, TIFF, and DOCX formats.
- The system SHALL support batch upload of multiple documents per bidder.

### FR-03.2: Document Classification
- The system SHALL automatically classify uploaded documents into categories (PAN card, GST certificate, Udyam certificate, financial statement, OEM authorization, experience certificate, etc.).
- The system SHALL allow procurement officers to correct AI classification.

### FR-03.3: Field Extraction
- The system SHALL extract key fields from classified documents using AI (OCR + NLP).
- Extracted fields SHALL include confidence scores.
- Low-confidence extractions SHALL be flagged for human review.

### FR-03.4: Document Validity
- The system SHALL check document dates for expiry where applicable.
- The system SHALL flag documents that will expire before the tender evaluation completion date.

---

## FR-04: Government Verification

### FR-04.1: Multi-Mode Verification
- The system SHALL support four verification modes for each integration:
  - **LIVE**: Real-time API call to government system
  - **SANDBOX**: API call to government sandbox/test environment
  - **MOCK**: Simulated response from internal mock service (clearly labelled)
  - **MANUAL**: Officer manually verifies and records result

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

### FR-04.2: Verification Domains
The system SHALL support verification for the following domains (with appropriate mode):

| Domain | Verification Target | Initial Mode | Claim Classification |
|--------|-------------------|--------------|----------------------|
| PAN | Identity, name, status | MOCK → LIVE (via Protean/API Setu) | REQUIRES_GOVERNMENT_APPROVAL |
| GST | Registration status, filing status | SANDBOX/LIVE (via GSP/developer.gst.gov.in) | REQUIRES_GOVERNMENT_APPROVAL |
| MCA/CIN | Company status, directors, charges | MOCK (no suitable public API confirmed) | MOCK_ONLY |
| Udyam/MSME | Registration validity, classification | MOCK (no suitable public API confirmed) | MOCK_ONLY |
| EPFO | Employer registration status | MANUAL (no suitable public API confirmed) | MANUAL_FALLBACK |
| ESIC | Registration status | MANUAL (no suitable public API confirmed) | MANUAL_FALLBACK |
| Startup India | DPIIT recognition status | MANUAL (no suitable public API confirmed) | MANUAL_FALLBACK |
| NSIC | Registration validity | MANUAL (no suitable public API confirmed) | MANUAL_FALLBACK |
| DigiLocker | Document authenticity | SANDBOX (via partners.apisetu.gov.in) | REQUIRES_GOVERNMENT_APPROVAL |
| Debarment | Blacklisting status | MANUAL + CPPP search | MANUAL_FALLBACK |

### FR-04.3: Verification Results
- Each verification SHALL produce a result: VERIFIED, NOT_VERIFIED, EXPIRED, ERROR, UNAVAILABLE.
- Each result SHALL include: timestamp, source, mode used, raw response (where applicable).
- Verification results SHALL be cached with configurable TTL.

---

## FR-05: Compliance Evaluation

### FR-05.1: Rule Engine
- The system SHALL evaluate each tender requirement against verified bidder data using a deterministic rule engine.
- Rules SHALL NOT be hard-coded; they SHALL be configurable per tender.
- The rule engine SHALL produce a result per requirement: PASS, FAIL, REVIEW, MISSING, EXPIRED, CONFLICT, NOT_VERIFIED, NOT_APPLICABLE.

### FR-05.2: Make in India Compliance
- The system SHALL support Make in India evaluation per the Public Procurement (Preference to Make in India) Order, 2017 (as amended July 2024).
- The system SHALL support Class-I (≥50% local content), Class-II (≥20% to <50%), and Non-Local (<20%) classification.
- Local content calculation SHALL exclude imported items resold locally, royalties, and rebranded products.
- The system SHALL support tender-specific threshold overrides (as nodal ministries may set higher thresholds).
- Policy version SHALL be tracked and rules SHALL be versioned.

### FR-05.3: Cross-Source Conflict Detection
- The system SHALL compare data from different sources for the same field and flag conflicts.
- Examples: PAN name vs. GST name vs. MCA name; registered address mismatches; entity type mismatches.
- Each conflict SHALL be classified by severity: CRITICAL, HIGH, MEDIUM, LOW.

---

## FR-06: Risk Scoring & Classification

### FR-06.1: Multi-Dimensional Scoring
- The system SHALL NOT rely on a single percentage score.
- The system SHALL produce three separate scores:
  - **Compliance Score** (0–100): Percentage of requirements met
  - **Evidence Confidence** (0–100): Quality and verifiability of supporting evidence
  - **Risk Score** (0–100): Aggregate risk from conflicts, missing data, and anomalies

### FR-06.2: Risk Classification
- The system SHALL classify each bidder into risk categories: LOW, MEDIUM, HIGH, CRITICAL.
- Classification SHALL be based on scoring thresholds and critical-failure rules (e.g., any FAIL on a mandatory requirement = CRITICAL risk).

---

## FR-07: AI Recommendations

### FR-07.1: Compliance Explanation
- The system SHALL generate natural-language explanations for each compliance result.
- Explanations SHALL cite specific evidence (document, page, field, verification result).
- Explanations SHALL distinguish between FACT (verified), ASSUMPTION, and UNVERIFIED data.

### FR-07.2: Recommendations
- The system SHALL generate recommendations for the procurement officer (e.g., "Request clarification on turnover figures", "OEM authorization expired on DD/MM/YYYY").
- Recommendations SHALL be clearly labelled as AI-generated suggestions.
- The system SHALL NOT recommend qualification or disqualification directly.

---

## FR-08: Human Decision Workflow

### FR-08.1: Officer Review
- The system SHALL present a comprehensive evaluation dashboard per bidder.
- The procurement officer SHALL review AI-extracted data, verification results, compliance scores, conflicts, and recommendations.
- The officer SHALL be able to override any AI classification with documented rationale.

### FR-08.2: Final Decision
- The procurement officer SHALL make the final decision: QUALIFY, DISQUALIFY, or SEEK_CLARIFICATION.
- Every decision SHALL require a rationale entry.
- Decisions SHALL be recorded with officer identity, timestamp, and supporting evidence references.

### FR-08.3: Multi-Level Approval
- The system SHALL support configurable approval workflows (e.g., reviewer → approver → sanctioning authority).

---

## FR-09: Audit Trail

### FR-09.1: Comprehensive Logging
- The system SHALL log every significant action: document upload, AI extraction, verification call, rule evaluation, officer decision, data modification.
- Logs SHALL be append-only and tamper-evident.
- Each log entry SHALL include: timestamp, actor (user or system), action, target, before/after values (for modifications).

### FR-09.2: Audit Report Generation
- The system SHALL generate complete audit reports per tender evaluation.
- Reports SHALL include: timeline of events, decision chain, evidence summary, compliance matrix.

---

## FR-10: Reporting & Analytics

### FR-10.1: Evaluation Reports
- Per-bidder compliance report
- Per-tender evaluation summary
- Comparative bidder analysis

### FR-10.2: Analytics (Future Enhancement)
- Tender processing time analytics
- Common rejection reasons
- Verification failure rates
- AI extraction accuracy tracking
