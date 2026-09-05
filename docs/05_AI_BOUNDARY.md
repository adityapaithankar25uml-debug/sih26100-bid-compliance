# 05 — AI Boundary

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05

---

## Core Principle

```
AI INTERPRETS → AUTHORIZED SOURCES VERIFY → RULES EVALUATE → EVIDENCE PROVES → HUMAN APPROVES
```

This document defines the strict boundary between what AI may do and what must remain under deterministic application control or human authority.

---

## 1. AI Responsibilities (MAY)

### 1.1 Document Classification
- **AI MAY** classify uploaded documents into categories (PAN card, GST certificate, OEM authorization, etc.)
- **AI MAY** suggest classifications with confidence scores
- **CONSTRAINT:** Human must be able to correct any classification
- **CONSTRAINT:** Classification confidence below threshold → automatic REVIEW flag

### 1.2 Field Extraction
- **AI MAY** extract structured data from unstructured documents using OCR and NLP
- **AI MAY** identify key fields: names, dates, amounts, registration numbers, addresses
- **CONSTRAINT:** Every extracted value must include source location (page, region) and confidence score
- **CONSTRAINT:** Low-confidence extractions must be flagged for human review

### 1.3 Tender Requirement Extraction
- **AI MAY** parse tender documents to identify eligibility requirements
- **AI MAY** classify requirements as mandatory/preferred
- **AI MAY** identify thresholds, deadlines, and document requirements
- **CONSTRAINT:** Extracted requirements must be presented to procurement officer for confirmation
- **CONSTRAINT:** AI-extracted requirements are PROPOSALS until officer confirms

### 1.4 Inconsistency Identification
- **AI MAY** identify possible inconsistencies across data sources
- **AI MAY** flag entity name mismatches, date conflicts, identifier discrepancies
- **CONSTRAINT:** Inconsistencies are flagged as POSSIBLE — not confirmed — until human reviews

### 1.5 Evidence Summarization
- **AI MAY** summarize evidence chains for human consumption
- **AI MAY** generate natural-language compliance explanations
- **CONSTRAINT:** Every claim in a summary must cite its source evidence
- **CONSTRAINT:** Summaries must distinguish VERIFIED facts from UNVERIFIED claims

### 1.6 Recommendation Generation
- **AI MAY** generate recommendations for the procurement officer
- Examples: "Consider requesting updated financial statements", "OEM authorization certificate appears to have expired"
- **CONSTRAINT:** Recommendations are SUGGESTIONS only, clearly labelled as AI-generated
- **CONSTRAINT:** AI must NEVER directly recommend QUALIFY or DISQUALIFY

### 1.7 Anomaly Detection
- **AI MAY** identify anomalous patterns across bidders or documents
- Examples: Identical documents submitted by different bidders, statistically improbable financial figures
- **CONSTRAINT:** Anomalies are flags for human investigation, not conclusions

### 1.8 Corrigendum Impact Analysis
- **AI MAY** analyze corrigendum/amendments to identify changed requirements
- **AI MAY** highlight which bidder evaluations are affected by changes
- **CONSTRAINT:** Impact analysis must be confirmed by procurement officer

---

## 2. AI Prohibitions (MUST NOT)

### 2.1 Qualification Decisions
- **AI MUST NOT** independently qualify any bidder
- **AI MUST NOT** independently disqualify any bidder
- **RATIONALE:** CVC guidelines and procurement rules require human accountability for qualification decisions

### 2.2 Rule Modification
- **AI MUST NOT** modify, create, or delete compliance rules
- **AI MUST NOT** change thresholds, deadlines, or eligibility criteria
- **RATIONALE:** Rules must be deterministic, versioned, and auditable. AI-modified rules would undermine auditability.

### 2.3 Evidence Tampering
- **AI MUST NOT** alter, redact, or modify uploaded evidence
- **AI MUST NOT** alter verification responses from government systems
- **AI MUST NOT** modify extracted data after initial extraction without clear versioning
- **RATIONALE:** Evidence integrity is the foundation of the audit trail

### 2.4 Audit Log Manipulation
- **AI MUST NOT** delete, modify, or suppress audit log entries
- **RATIONALE:** Audit logs must be immutable for CVC/CAG compliance

### 2.5 Government Verification Fabrication
- **AI MUST NOT** fabricate or simulate government verification responses as if they were real
- **AI MUST NOT** present MOCK results as LIVE verification results
- **RATIONALE:** Government verification is an authoritative truth source; fabrication would constitute fraud

### 2.6 Unauthorized System Access
- **AI MUST NOT** call government systems without proper authorization
- **AI MUST NOT** scrape government portals
- **AI MUST NOT** bypass CAPTCHA or authentication mechanisms
- **RATIONALE:** Unauthorized access violates IT Act 2000 and government portal ToS

### 2.7 Decision Override
- **AI MUST NOT** override a procurement officer's decision
- **AI MUST NOT** escalate or alter a recorded decision
- **RATIONALE:** Human authority is supreme in procurement decisions

---

## 3. Deterministic Application Responsibilities

These functions MUST be implemented as deterministic, testable, auditable code — NOT AI:

### 3.1 Format Validation
- PAN format: `[A-Z]{3}[ABCFGHLJPT][A-Z][0-9]{4}[A-Z]`
- GSTIN format: `[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]`
- CIN format: `[UL][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}`
- Udyam format: `UDYAM-[A-Z]{2}-[0-9]{2}-[0-9]{7}`
- **RATIONALE:** These are known formats with deterministic validation rules

### 3.2 PAN-GSTIN Cross-Validation
- Characters 3–12 of GSTIN must match the PAN
- **RATIONALE:** This is a mathematical fact, not a judgment call

### 3.3 Date Calculations
- Document expiry checking
- Tender deadline checking
- Financial year calculations
- **RATIONALE:** Date arithmetic is deterministic

### 3.4 Threshold Comparisons
- Turnover ≥ required minimum
- Experience years ≥ required minimum
- Local content % ≥ required threshold
- **RATIONALE:** Numeric comparison is deterministic

### 3.5 Compliance Rule Evaluation
- Per-requirement PASS/FAIL/REVIEW/MISSING evaluation
- Rule chaining (prerequisite rules)
- Severity classification
- **RATIONALE:** Rules must be reproducible and auditable

### 3.6 Scoring Calculations
- Compliance score computation
- Evidence confidence aggregation
- Risk score calculation
- **RATIONALE:** Scoring must be reproducible

### 3.7 Workflow Enforcement
- Mandatory review steps cannot be skipped
- Decision requires rationale
- Approval chain enforcement
- **RATIONALE:** Workflow integrity is a compliance requirement

### 3.8 Evidence Chain Management
- Document hashing
- Timestamp chain
- Evidence-to-decision linking
- **RATIONALE:** Evidence integrity must be cryptographically verifiable

### 3.9 Access Control
- RBAC enforcement
- Session management
- Audit logging
- **RATIONALE:** Security is deterministic

---

## 4. Boundary Enforcement Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│    Procurement Officer / Auditor / Admin                │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              HUMAN DECISION LAYER                        │
│  • Final qualify/disqualify decision                     │
│  • Requirement confirmation                              │
│  • AI output review and correction                       │
│  • Rationale documentation                               │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│           DETERMINISTIC RULES ENGINE                     │
│  • Compliance rule evaluation                            │
│  • Format validation                                     │
│  • Threshold comparison                                  │
│  • Cross-reference validation                            │
│  • Scoring calculation                                   │
│  • Workflow enforcement                                  │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  RULES ARE: versioned, auditable, reproducible,     │ │
│  │  tamper-proof, NOT AI-generated                     │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│          GOVERNMENT VERIFICATION LAYER                   │
│  • API calls (LIVE/SANDBOX/MOCK/MANUAL)                 │
│  • Response parsing (deterministic)                      │
│  • Status mapping (deterministic)                        │
│  • Circuit breaker / retry (deterministic)               │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  RESULTS ARE: timestamped, source-attributed,       │ │
│  │  mode-labelled, cached with TTL                     │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│                AI INTERPRETATION LAYER                    │
│  • Document classification                               │
│  • Field extraction (OCR + NLP)                          │
│  • Requirement extraction                                │
│  • Inconsistency detection                               │
│  • Evidence summarization                                │
│  • Recommendation generation                             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  OUTPUTS ARE: confidence-scored, source-cited,      │ │
│  │  labelled as AI-generated, never auto-actioned      │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│              EVIDENCE MANAGEMENT LAYER                    │
│  • Document storage (encrypted, hash-verified)           │
│  • Audit trail (append-only, tamper-evident)             │
│  • Evidence chain (linked to every decision)             │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  IMMUTABLE: No component may alter stored evidence  │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 5. AI Risk Mitigations

| Risk | Mitigation |
|------|-----------|
| **Hallucination** | Ground all outputs in source documents; require evidence citations; confidence thresholds; human review |
| **Prompt Injection** | Input sanitization; output validation; sandboxed execution; no user-controlled prompts to system LLM |
| **Overconfidence** | Calibrated confidence scores; mandatory human review for decisions; "REVIEW" status for borderline cases |
| **Bias** | Monitor extraction accuracy across document types; periodic bias audits |
| **Manipulation** | AI outputs cannot auto-trigger actions; all require human confirmation |
| **Opacity** | Explainable outputs with source citations; model versioning; output audit trail |

---

## 6. AI Transparency Requirements

1. Every AI-generated output MUST be labelled as "AI-Generated" in the UI
2. Every AI extraction MUST show the source location (document, page, region)
3. Every AI confidence score MUST be visible to the procurement officer
4. Every AI recommendation MUST cite the evidence it is based on
5. The system MUST track which AI model version produced each output
6. AI outputs that fall below confidence thresholds MUST be automatically flagged for human review
7. The procurement officer MUST be able to override any AI output with documented rationale
