# Phase 5 — Evidence Architecture & Quality Model

## 1. Executive Summary
The Phase 5 Evidence Layer provides an immutable, traceable, and quality-assessed Evidence Ledger for the SIH26100 AI-Powered Integrated Bid Compliance Verification Platform. It bridges Phase 3 AI extraction and Phase 4 Government Verification into a trustworthy evidence foundation.

## 2. Core Architectural Principles
1. **Evidence Provenance:** Every evidence item maintains strict origin tracking (`bidder_document`, `government_verification`, `ai_extraction`, `manual_officer`).
28. **Multi-Dimensional Non-Collapsing Evidence Quality Model:** Quality is evaluated across 7 explicit, independent dimensions rather than a single black-box score:
   - `source_authority`: `AUTHORITATIVE_GOVT` | `BIDDER_DOCUMENT` | `AI_EXTRACTED` | `MANUAL_OFFICER`
   - `source_freshness`: `FRESH` | `ACCEPTABLE` | `STALE` | `UNKNOWN`
   - `completeness`: `COMPLETE` | `PARTIAL` | `MISSING`
   - `integrity_hash_validity`: `VERIFIED` | `UNCHECKED` | `FAILED`
   - `identity_linkage`: `MATCHED` | `PARTIAL_MATCH` | `MISMATCH` | `UNVERIFIED`
   - `extraction_provenance`: `DIRECT` | `OCR` | `AI_PARSED` | `MANUAL`
   - `consistency`: `CONSISTENT` | `CONFLICTING` | `UNKNOWN`
   - `quality_assessment_summary`: `STRONG` | `MODERATE` | `NEEDS_REVIEW` | `INSUFFICIENT` — Presentation-level decision support summary derived from explicit policy rules.
9. **Architectural Separation:** Evidence quality remains strictly separate from AI extraction confidence, compliance evaluation status, bidder qualification outcome, and advisory risk score.
10. **Non-Authoritative AI:** AI extraction provides candidate evidence labeled `AI ADVISORY`. AI generated text is never treated as self-authenticating evidence.

## 3. Evidence Record Model (`EvidenceRecord`)
```sql
CREATE TABLE evidence_records (
    id VARCHAR(26) PRIMARY KEY,
    bid_submission_id VARCHAR(26) REFERENCES bid_submissions(id),
    compliance_evaluation_id VARCHAR(26) REFERENCES compliance_evaluations(id),
    requirement_id VARCHAR(26) REFERENCES tender_requirements(id),
    rule_id VARCHAR(26) REFERENCES compliance_rules(id),
    policy_version_id VARCHAR(26) REFERENCES policy_versions(id),
    source_document_id VARCHAR(26) REFERENCES source_documents(id),
    verification_result_id VARCHAR(26) REFERENCES government_verification_results(id),
    verification_record_id VARCHAR(26) REFERENCES government_verification_records(id),
    evidence_type VARCHAR(100) NOT NULL,
    confidence_score FLOAT NOT NULL DEFAULT 1.0,
    extraction_method VARCHAR(50),
    page_number INTEGER,
    source_text_snippet TEXT,
    bounding_box_json JSONB,
    evidence_payload JSONB,
    evidence_quality_json JSONB,
    status VARCHAR(50) NOT NULL DEFAULT 'VALID',
    security_classification VARCHAR(50) NOT NULL DEFAULT 'INTERNAL',
    provenance_metadata_json JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## 4. Security & Classification
All evidence records enforce Phase 1 security classifications: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`, `PII`. Direct access to restricted PII evidence requires appropriate RBAC privileges (`ProcurementOfficer`, `ComplianceOfficer`, `SystemAdmin`).
