# Phase 1 AI Architecture Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-017  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines the AI pipeline architecture, 14 AI use case specifications, 4-tier responsibility boundaries, and execution pipelines. No FastAPI routers, Python AI scripts, ORM models, database migrations, frontend code, or AI SDK installations are created.

---

## 1. Core Architectural Axiom & Non-Authoritative Principle

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           NON-NEGOTIABLE OPERATIONAL PIPELINE                           │
├───────────────┬──────────────────────┬─────────────────┬────────────────┬───────────────┤
│  AI INTERPRETS│ AUTHORIZED SOURCES   │ RULES EVALUATE  │ EVIDENCE PROVES│ HUMAN APPROVES│
│  (Advisory)   │ VERIFY (Authoritative│ (Deterministic) │ (Provenance)   │ (Final)       │
└───────────────┴──────────────────────┴─────────────────┴────────────────┴───────────────┘
```

The AI architecture strictly maintains these operational guardrails:
1. **AI is non-authoritative:** AI outputs are candidate extraction proposals, semantic comparisons, anomaly alerts, or explanatory text. AI outputs NEVER independently qualify or disqualify a bidder.
2. **Deterministic Rules & Authoritative Sources Overrule AI:** Government databases (GSTN, MCA, Udyam, EPFO) and deterministic Python rule engines are the sole authoritative sources for verification and evaluation.
3. **No Direct State Mutation:** AI pipelines CANNOT create `OfficerDecision` records, update `QualificationOutcome` statuses, execute manual overrides, or invoke government verification adapters directly.
4. **Analytical Metric Isolation:** AI confidence (0.0 to 1.0) is strictly separated from Evidence Confidence, Compliance Status (`PASS`/`FAIL`), Risk Score (0.0 to 100.0), and Qualification Outcome (`QUALIFIED`/`DISQUALIFIED`).

---

## 2. 14 Core AI Use Case Specifications

The platform utilizes AI for 14 targeted bid compliance interpretation tasks:

### Use Case 1: Document Classification
- **Input:** Raw document text stream / layout tokens from uploaded PDF file.
- **Preprocessing:** MIME type magic-byte validation, ClamAV virus scanning, multi-page layout segmentation.
- **AI Operation:** Text/layout classification against standard tender document taxonomy (e.g. `CA_TURNOVER_CERT`, `GST_REGISTRATION_CERT`, `UDYAM_CERT`, `EMD_RECEIPT`, `DEBARMENT_AFFIDAVIT`, `TECHNICAL_SPEC_SHEET`).
- **Expected Structured Output:** `DocumentClassificationEnvelope` containing `predicted_doc_type`, `confidence_score`, `page_range`.
- **Validation:** Pydantic schema validation; magic-byte format matching.
- **Provenance:** Document ULID, page numbers, text chunk offset.
- **Confidence Handling:** If confidence < 0.85, flagged for human officer classification confirmation.
- **Human Confirmation Requirement:** Required for unclassified or low-confidence documents before downstream extraction.
- **Deterministic Verification:** MIME structure check & page count bounds validation.
- **Allowed Downstream Consumers:** Document Extraction Service, Indexing Engine.
- **Prohibited Downstream Actions:** Auto-rejecting a document based solely on classification failure.

### Use Case 2: OCR-Assisted Document Understanding
- **Input:** Scanned document image pages (PNG/TIFF) or image-based PDF pages.
- **Preprocessing:** Image deskewing, binarization, resolution normalization (300 DPI), layout region extraction.
- **AI Operation:** Vision-Language / Layout-aware OCR parsing for printed and handwritten tabular text in bilingual Indian context (English / Hindi).
- **Expected Structured Output:** `OCRExtractedPageSchema` containing text blocks, line tokens, table cells, and bounding boxes `[x0, y0, x1, y1]`.
- **Validation:** Bounding box coordinate sanity check (within 0–100% normalized canvas boundaries).
- **Provenance:** Document ULID, page index, bounding box array.
- **Confidence Handling:** Character-level and word-level OCR confidence metrics. Words < 0.70 confidence highlighted in visual workbench.
- **Human Confirmation Requirement:** Visual bounding box confirmation required if extraction feeds high-risk financial fields.
- **Deterministic Verification:** Regex pattern matching on standard key formats (GSTIN checksum, PAN format, IFSC syntax).
- **Allowed Downstream Consumers:** Structured Field Extraction Pipeline.
- **Prohibited Downstream Actions:** Modifying or cropping original uploaded document files.

### Use Case 3: Structured Field Extraction
- **Input:** OCR text layout streams and document classification context.
- **Preprocessing:** Field-specific prompt template formatting and JSON schema boundary constraints.
- **AI Operation:** Target key-value extraction (e.g., Turnover amounts per FY, Net Worth, GSTIN, PAN, Date of Incorporation, Udyam Registration Number).
- **Expected Structured Output:** `ExtractedFieldsEnvelope` containing array of `FieldExtractionItem` (`field_name`, `extracted_value`, `unit`, `confidence`, `page_number`, `bounding_box`).
- **Validation:** Strict Pydantic schema validation, regex syntax validation, currency/number parsing validation.
- **Provenance:** Document ULID, page number, bounding box, raw source snippet.
- **Confidence Handling:** Low confidence (< 0.80) triggers visual highlight on officer workbench.
- **Human Confirmation Requirement:** Mandatory officer confirmation for financial figures before deterministic rule evaluation if unverified by external source.
- **Deterministic Verification:** Mathematical checksum validation (e.g. GSTIN Modulus 36 check, PAN 10-char regex).
- **Allowed Downstream Consumers:** Compliance Rule Engine candidate inputs, Evidence Ledger builder.
- **Prohibited Downstream Actions:** Modifying extracted values without audit log trail.

### Use Case 4: Tender Requirement Extraction
- **Input:** Unstructured text from GeM / CPCL Tender Notice Notice (NIT) and Custom ATC (Additional Terms & Conditions) PDFs.
- **Preprocessing:** Document sectioning (Cover 1 Technical, Cover 2 Financial, Special Conditions).
- **AI Operation:** Extracts eligibility criteria clauses (Financial Turnover, Past Experience, EMD Exemption, Local Content %, ISO Certifications).
- **Expected Structured Output:** `TenderRequirementCandidateList` (`requirement_code`, `category`, `description`, `threshold_value`, `unit`, `is_mandatory`, `applicable_bidder_type`).
- **Validation:** Schema validation against domain dictionary taxonomies.
- **Provenance:** Tender Version ULID, section heading, page number, clause text.
- **Confidence Handling:** Unassessed / advisory signal; candidates presented to procurement admin.
- **Human Confirmation Requirement:** **MANDATORY.** AI-extracted tender requirements remain *candidates* until explicitly confirmed by a `PROCUREMENT_OFFICER` or `PROCUREMENT_ADMIN`.
- **Deterministic Verification:** Duplicate requirement code checks and mandatory parameter presence checks.
- **Allowed Downstream Consumers:** Tender Requirement Management Service.
- **Prohibited Downstream Actions:** Publishing a tender version with unconfirmed AI requirement proposals.

### Use Case 5: Tender Clause Classification
- **Input:** Individual clause text snippets from tender documents.
- **Preprocessing:** Clause sentence tokenization and noise stripping.
- **AI Operation:** Classifies clause into standardized procurement categories (`COMMERCIAL_ELIGIBILITY`, `TECHNICAL_CAPABILITY`, `STATUTORY_COMPLIANCE`, `DEBARMENT_DECLARATION`, `LOCAL_CONTENT_PREFERENCE`, `MSE_PREFERENCE`).
- **Expected Structured Output:** `ClauseClassificationResult` (`clause_id`, `category`, `confidence`, `is_disqualifying_condition`).
- **Validation:** Category enum validation against frozen data dictionary taxonomy.
- **Provenance:** Tender ULID, page number, clause character offset.
- **Confidence Handling:** Confidence score recorded; low confidence clauses categorized as `GENERAL_TERMS`.
- **Human Confirmation Requirement:** Required during tender setup review.
- **Deterministic Verification:** Exact keyword heuristic cross-validation (e.g., presence of "EMD", "Turnover", "Make in India").
- **Allowed Downstream Consumers:** Requirement-to-Rule Mapping Pipeline.
- **Prohibited Downstream Actions:** Auto-assigning legal liability or auto-disqualifying bidders based on clause class.

### Use Case 6: Requirement-to-Rule Candidate Mapping
- **Input:** Confirmed `TenderRequirement` object and platform Pydantic compliance rule registry.
- **Preprocessing:** Embedding generation for requirement description and registered compliance rule definitions.
- **AI Operation:** Proposes top-N candidate Python compliance rules capable of evaluating the requirement.
- **Expected Structured Output:** `RuleMappingCandidateList` (`requirement_id`, candidate array of `rule_id`, `match_score`, `mapping_rationale`).
- **Validation:** Rule ID existence check in platform rule registry.
- **Provenance:** Requirement ULID, Rule ULID, prompt/version identifier.
- **Confidence Handling:** Match score displayed as similarity metric (0.0 to 1.0).
- **Human Confirmation Requirement:** Procurement Admin/Officer confirms or selects the binding compliance rule.
- **Deterministic Verification:** Parameter compatibility check between requirement threshold and rule input parameters.
- **Allowed Downstream Consumers:** Rule Engine Configuration Workbench.
- **Prohibited Downstream Actions:** Binding an unconfirmed rule mapping to an active tender evaluation.

### Use Case 7: Semantic Comparison between Tender Requirements & Bidder Evidence
- **Input:** Target `TenderRequirement` threshold vs. extracted bidder document value or verified government payload.
- **Preprocessing:** Value normalization (e.g. converting INR Lakhs to INR Crores, parsing date ranges).
- **AI Operation:** Performs semantic comparison when values are non-numeric or technical specifications require semantic evaluation (e.g., comparing proposed valve pressure rating spec sheet vs. tender technical spec clause).
- **Expected Structured Output:** `SemanticComparisonResult` (`match_status`: `EQUIVALENT` / `NON_EQUIVALENT` / `AMBIGUOUS`, `similarity_score`, `comparison_reasoning`, `key_discrepancies`).
- **Validation:** JSON schema validation; score bounded to [0.0, 1.0].
- **Provenance:** Requirement ULID, Document ULID, Page/Bounding Box ULID, Verified Payload ULID.
- **Confidence Handling:** `AMBIGUOUS` or score < 0.85 triggers `REVIEW` status in rule engine.
- **Human Confirmation Requirement:** Procurement Officer review mandatory if semantic comparison is `NON_EQUIVALENT` or `AMBIGUOUS`.
- **Deterministic Verification:** Exact numeric threshold comparison takes precedence over semantic comparison when quantitative values exist.
- **Allowed Downstream Consumers:** Deterministic Rule Engine (as advisory input for complex technical rules).
- **Prohibited Downstream Actions:** Overriding a deterministic numeric threshold failure (`60 Cr < 80 Cr`).

### Use Case 8: Missing-Document Detection
- **Input:** Submission document inventory list vs. mandatory tender document checklist.
- **Preprocessing:** Document classification normalization across submission package.
- **AI Operation:** Detects missing required document types, expired certificates, or incomplete multi-page packages.
- **Expected Structured Output:** `MissingDocumentAnalysis` (`missing_doc_types`, `incomplete_docs`, `expiry_warnings`).
- **Validation:** Schema validation against tender requirement checklist.
- **Provenance:** Submission ULID, Tender Version ULID.
- **Confidence Handling:** High confidence required; missing documents flagged directly.
- **Human Confirmation Requirement:** Officer verifies missing document finding before issuing clarification request.
- **Deterministic Verification:** Exact set difference check between submitted document classifications and required document types.
- **Allowed Downstream Consumers:** Compliance Evaluation Engine, Clarification Notice Generator.
- **Prohibited Downstream Actions:** Auto-rejecting bid submission without officer review.

### Use Case 9: Inconsistency / Anomaly Detection
- **Input:** Multi-document extraction dataset for a single bidder submission (PAN, GSTIN, CA Cert, Udyam Cert, MCA Filings).
- **Preprocessing:** Cross-document field aggregation matrix.
- **AI Operation:** Identifies identity discrepancies, mismatched company names, date mismatches, turnover discrepancies across documents, or suspicious formatting anomalies.
- **Expected Structured Output:** `AnomalySignalList` (array of `signal_code`, `severity`: `HIGH`/`MEDIUM`/`LOW`, `discrepancy_description`, `affected_documents`).
- **Validation:** Schema validation; signal code validation against platform anomaly taxonomy.
- **Provenance:** Submission ULID, Document ULIDs, Field ULIDs.
- **Confidence Handling:** Anomaly signals are added to Risk Profile as advisory metrics (0.0 to 100.0).
- **Human Confirmation Requirement:** Officer investigates anomaly signals in workbench.
- **Deterministic Verification:** Cross-document regex value equality checks (e.g. `docA.PAN == docB.PAN`).
- **Allowed Downstream Consumers:** Risk Assessment Service, Officer Workbench.
- **Prohibited Downstream Actions:** Disqualifying a bidder based on anomaly signal score alone.

### Use Case 10: Compliance Explanation
- **Input:** Itemized deterministic compliance evaluation results, evidence records, and verified government payloads.
- **Preprocessing:** Evidence graph traversal to assemble grounding facts.
- **AI Operation:** Generates human-readable plain language compliance explanation for procurement officers and audit logs.
- **Expected Structured Output:** `ComplianceExplanationEnvelope` (`summary_explanation`, `itemized_reasons`, `grounding_evidence_ids`).
- **Validation:** Grounding verification—every fact in explanation must match an approved `EvidenceRecord` or `VerificationResult` ID.
- **Provenance:** Evaluation ULID, Evidence ULIDs, Rule Version ULID.
- **Confidence Handling:** Hallucination check filter ensures 100% evidence grounding.
- **Human Confirmation Requirement:** Officer reads explanation; officer may edit explanation for final report.
- **Deterministic Verification:** Grounding text string alignment with underlying rule output fields.
- **Allowed Downstream Consumers:** Officer Workbench UI, CVC Audit Report Generator.
- **Prohibited Downstream Actions:** Including unverified external claims or hallucinated facts in explanation.

### Use Case 11: Recommendation Generation
- **Input:** Overall evaluation summary, risk profile, missing document signals, and manual override history.
- **Preprocessing:** Context aggregation within token context limits.
- **AI Operation:** Generates advisory recommendations for procurement officer next steps (e.g. "Seek clarification regarding MSE certificate validity date", "Proceed to Cover 2 financial opening").
- **Expected Structured Output:** `RecommendationEnvelope` (`recommended_action`: `PROCEED` / `SEEK_CLARIFICATION` / `REVIEW_OVERRIDE`, `rationale`, `risk_factors`).
- **Validation:** Recommendation choice enum validation.
- **Provenance:** Submission ULID, Evaluation ULID, Risk Profile ULID.
- **Confidence Handling:** Advisory signal only.
- **Human Confirmation Requirement:** Officer decides whether to follow or reject recommendation.
- **Deterministic Verification:** State machine eligibility check (e.g. cannot recommend `PROCEED` if mandatory Cover 1 requirements are `FAIL`).
- **Allowed Downstream Consumers:** Officer Decision Modal UI.
- **Prohibited Downstream Actions:** Auto-submitting the recommended officer decision choices.

### Use Case 12: Corrigendum Impact Analysis
- **Input:** Original tender requirements, new corrigendum document PDF, updated tender deadline.
- **Preprocessing:** Corrigendum text extraction and section diffing.
- **AI Operation:** Analyzes impact of corrigendum changes on existing bidder submissions and requirement mappings.
- **Expected Structured Output:** `CorrigendumImpactAnalysis` (`affected_requirement_codes`, `requires_bidder_resubmission`, `impact_summary`).
- **Validation:** Requirement code existence check.
- **Provenance:** Corrigendum Document ULID, Tender Version ULID.
- **Confidence Handling:** High-priority alert generated for procurement admin.
- **Human Confirmation Requirement:** Procurement Admin reviews and confirms requirement revisions.
- **Deterministic Verification:** Version increment check and deadline comparison.
- **Allowed Downstream Consumers:** Tender Re-evaluation Scheduler.
- **Prohibited Downstream Actions:** Auto-modifying active tender requirement versions without admin approval.

### Use Case 13: Compliance Drift Explanation
- **Input:** Historical compliance evaluation snapshots across multiple submission revisions or tender corrigenda.
- **Preprocessing:** Evaluation result snapshot diffing.
- **AI Operation:** Explains why a bidder's compliance status drifted from `PASS` to `REVIEW` or `FAIL` across submission versions.
- **Expected Structured Output:** `ComplianceDriftExplanation` (`drift_cause`, `changed_fields`, `explanatory_narrative`).
- **Validation:** Grounded against snapshot diff entries.
- **Provenance:** Submission Revision ULIDs, Evaluation ULIDs.
- **Confidence Handling:** Advisory explanation.
- **Human Confirmation Requirement:** Auditor / Officer review.
- **Deterministic Verification:** Value inequality checks between snapshot version fields.
- **Allowed Downstream Consumers:** Audit Log Viewer, Vigilance Review Module.
- **Prohibited Downstream Actions:** Altering historical evaluation snapshots.

### Use Case 14: Natural-Language Officer Assistance
- **Input:** Natural language query from procurement officer in workbench (e.g. "Show me all bidders with turnover > 100 Cr who used MSE EMD waiver").
- **Preprocessing:** Query intent parsing and RBAC role validation.
- **AI Operation:** Translates natural language query into structured API filter parameters and SQL/Elastic query constraints.
- **Expected Structured Output:** `StructuredQueryEnvelope` (`target_resource`, `filters`, `sort_order`, `explanation`).
- **Validation:** AST validation against authorized database fields and RBAC read permissions.
- **Provenance:** User Session ULID, Query Timestamp.
- **Confidence Handling:** Parsed query displayed to officer for confirmation before execution.
- **Human Confirmation Requirement:** Officer executes or modifies parsed query.
- **Deterministic Verification:** Parameter type validation and SQL injection prevention sanitization.
- **Allowed Downstream Consumers:** Workbench Search API Gateway.
- **Prohibited Downstream Actions:** Executing arbitrary `DROP`, `UPDATE`, `DELETE`, or un-indexed database queries.

---

## 3. 4-Tier Responsibility Boundary Matrix

To enforce absolute clarity on system capabilities, all platform operations are classified into one of 4 strict responsibility tiers:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        4-TIER RESPONSIBILITY BOUNDARY MATRIX                            │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ TIER A: DETERMINISTIC BACKEND LOGIC (Python Code, PostgreSQL, Checksums, Rules)         │
│ TIER B: AI-ASSISTED INTERPRETATION (OCR, Extraction, Semantic Match, Anomaly Signals)   │
│ TIER C: AUTHORITATIVE EXTERNAL VERIFICATION (GSTN, MCA, Udyam, EPFO Government APIs)  │
│ TIER D: HUMAN DECISION (Procurement Officer / Admin Explicit Sanction)                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

| Operational Action / Task | Tier A: Deterministic | Tier B: AI-Assisted | Tier C: Govt Verified | Tier D: Human Decision | Authoritative Level |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Document Magic-Byte & Virus Check** | 🟢 PRIMARY | 🔴 NONE | 🔴 NONE | 🔴 NONE | Tier A (Deterministic) |
| **Document Classification** | 🟡 Fallback | 🟢 PRIMARY | 🔴 NONE | 🟡 Review | Tier B (AI Proposal) |
| **OCR Text & Bounding Box Parsing** | 🟡 Heuristic | 🟢 PRIMARY | 🔴 NONE | 🟡 UI Review | Tier B (AI Extraction) |
| **GSTIN Syntax Check (Regex & Mod 36)** | 🟢 PRIMARY | 🔴 NONE | 🔴 NONE | 🔴 NONE | Tier A (Deterministic) |
| **GSTIN Registration Status Query** | 🔴 NONE | 🔴 NONE | 🟢 PRIMARY | 🔴 NONE | Tier C (Authoritative Govt) |
| **Comparing Document GSTIN vs Govt GSTIN** | 🟢 PRIMARY | 🔴 NONE | 🔴 NONE | 🔴 NONE | Tier A (Deterministic Rule) |
| **Extracting Financial Turnover from PDF** | 🔴 NONE | 🟢 PRIMARY | 🔴 NONE | 🟡 UI Confirm | Tier B (AI Proposal) |
| **Tender Requirement Candidate Mining** | 🔴 NONE | 🟢 PRIMARY | 🔴 NONE | 🔴 NONE | Tier B (AI Proposal) |
| **Confirming Tender Eligibility Criteria** | 🔴 NONE | 🔴 NONE | 🔴 NONE | 🟢 PRIMARY | Tier D (Human Officer) |
| **Binding Compliance Rule Selection** | 🟡 Validated | 🟡 Suggested | 🔴 NONE | 🟢 PRIMARY | Tier D (Human Officer) |
| **Financial Turnover Requirement Eval** | 🟢 PRIMARY | 🔴 NONE | 🔴 NONE | 🔴 NONE | Tier A (Deterministic Rule) |
| **Technical Spec Sheet Semantic Comparison**| 🟡 Threshold | 🟢 PRIMARY | 🔴 NONE | 🟡 Review | Tier B (Advisory Metric) |
| **Anomaly Signal Detection** | 🟡 Cross-Check | 🟢 PRIMARY | 🔴 NONE | 🟡 Review | Tier B (Advisory Signal) |
| **Risk Score Calculation (0.0 - 100.0)** | 🟢 PRIMARY | 🟡 Inputs | 🟡 Inputs | 🔴 NONE | Tier A (Analytical Metric)|
| **Compliance Explanation Generation** | 🔴 NONE | 🟢 PRIMARY | 🔴 NONE | 🟡 Edit/Review| Tier B (Advisory Summary) |
| **Itemized Status Override (FAIL -> PASS)** | 🔴 State Mech | 🔴 NONE | 🔴 NONE | 🟢 PRIMARY | Tier D (Human Officer) |
| **Final Qualification / Disqualification** | 🔴 State Mech | 🔴 PROHIBITED | 🔴 PROHIBITED| 🟢 PRIMARY | Tier D (Human Officer) |
| **Audit Hash-Chain Event Verification** | 🟢 PRIMARY | 🔴 PROHIBITED | 🔴 NONE | 🔴 NONE | Tier A (Deterministic Cryptography) |

---

## 4. End-to-End Execution Pipelines

### 4.1 Document Processing Pipeline (15 Steps)

```
[Upload PDF] ──> (1. Magic Byte Check) ──> (2. Virus Scan) ──> (3. File Type Validation)
                     │
                     ▼
[MinIO Storage] <── (4. Compute SHA-256) ──> (5. Emit AUDIT_EVENT)
                     │
                     ▼
(6. Render Page Images @ 300 DPI) ──> (7. Layout Parsing & OCR) ──> (8. Bounding Box Extraction)
                                                                            │
                                                                            ▼
(11. Bounding Box Linkage) <── (10. Pydantic Schema Validation) <── (9. AI Structured Field Extraction)
          │
          ▼
(12. Confidence Score Check) ──> [If < 0.80] ──> (13. Flag for Human Officer Workbench UI)
          │
          ▼ [If >= 0.80 or Confirmed]
(14. Normalize Extracted Values) ──> (15. Store in ExtractedFields & Emit Evidence Proposals)
```

### 4.2 Tender Understanding Pipeline (10 Steps)

1. **Tender Notice Ingestion:** Upload NIT and ATC PDF files for new tender creation.
2. **Document Segmentation:** Partition document into Cover 1 (Technical), Cover 2 (Financial), and General ATC sections.
3. **AI Candidate Extraction:** Model extracts requirement candidates (`TenderRequirementCandidateList`).
4. **Category & Parameter Extraction:** Classify criteria into categories (Turnover, Experience, EMD, Local Content).
5. **Rule Mapping Recommendation:** AI gateway suggests registered Pydantic compliance rules for each candidate.
6. **Officer Verification Workbench:** Present extracted candidate requirements and suggested rule mappings to `PROCUREMENT_OFFICER` / `PROCUREMENT_ADMIN`.
7. **Human Confirmation & Parameter Adjustment:** Officer confirms requirement parameters, thresholds, and binding rule selections.
8. **Entity Persistence:** Create immutable `TenderRequirement` and `TenderRequirementRuleMap` records.
9. **Tender Version Locking:** Freeze `TenderVersion` snapshot for evaluation readiness.
10. **Corrigenda Monitoring:** On corrigendum upload, trigger diff analysis and re-evaluation alerts.

### 4.3 Bidder Document Pipeline & Entity Resolution

1. **Submission Package Receipt:** Ingest bidder document package under Cover 1 / Cover 2.
2. **Document Inventory & Classification:** AI classifies uploaded files into document taxonomy.
3. **Identity Field Extraction:** Extract PAN, GSTIN, Udyam Registration Number, MCA CIN, Legal Entity Name.
4. **Cross-Document Entity Resolution:**
   - Verify `docA.PAN == docB.PAN`.
   - Verify `docA.GSTIN[2:12] == docA.PAN`.
   - Verify Legal Entity Name consistency across certificates.
5. **Government Verification Dispatch:** Trigger external verification adapters (`GSTNAdapter`, `MCAAdapter`, `UdyamAdapter`) for authoritative live/sandbox lookups.
6. **Evidence Ledger Builder:** Assemble `EvidenceRecord` objects linking document bounding boxes, verified government payloads, and requirement codes.
7. **Deterministic Rule Engine Execution:** Python rule engine evaluates requirements against evidence records.

### 4.4 RAG / Knowledge Architecture Specification

Retrieval-Augmented Generation (RAG) is utilized strictly for **knowledge-assistance use cases** (officer policy lookups, procurement manual Q&A, compliance explanation grounding).

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              RAG KNOWLEDGE ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ KNOWLEDGE SOURCES: CVC Guidelines, GeM GTC/STC, CPCL Procurement Manual, Tender ATC     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Ingestion: Document PDF text extraction & structural sectioning                       │
│ 2. Chunking: Recursive character splitting (500 tokens chunk size, 50 token overlap)    │
│ 3. Metadata Tagging: Document ULID, Policy Version, CVC Clause ID, Effective Date       │
│ 4. Embeddings: Dedicated local embedding model (e.g. BGE-Large-EN-v1.5 / intfloat-e5)  │
│ 5. Vector Store: PostgreSQL pgvector extension (Cosine Distance / HNSW index)           │
│ 6. Retrieval: Top-K (K=5) hybrid dense-sparse retrieval filtered by active Policy Version│
│ 7. Guardrails: RAG outputs MUST cite exact Document ULID, Clause ID, & Page Number.      │
│    RAG MUST NOT override authoritative government verification or deterministic rules. │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

> **Critical Guardrail:** Policy documents in vector storage MUST be versioned. If a policy source is deprecated, its chunks are filtered out of active retrieval pipelines. RAG responses are strictly advisory and CANNOT alter rule evaluation statuses.
