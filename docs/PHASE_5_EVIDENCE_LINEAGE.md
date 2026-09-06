# Phase 5 — Evidence Traceability Lineage Graph

## 1. Traceability Architecture
Phase 5 introduces end-to-end relational evidence lineage. For any tender requirement or bid submission, procurement officers can navigate the complete lineage graph:

```
Requirement (TenderRequirement)
    ↓
Compliance Rule (ComplianceRule)
    ↓
Compliance Fact (ComplianceFact)
    ↓
Evidence Record (EvidenceRecord)
    ↓
Source (SourceDocument / GovernmentVerificationRecord)
    ↓
Evaluation Snapshot (EvaluationSnapshot)
    ↓
Risk Assessment (RiskAssessmentProfile)
    ↓
Human Review Task (HumanReviewTask)
    ↓
Officer Decision (OfficerDecision / ManualOverride)
    ↓
Audit Event (AuditEvent / AuditHashChainBlock)
```

## 2. API Traceability Graph Representation
The traceability graph is exposed via `GET /api/v1/bids/{submission_id}/evidence-trace` returning structured `nodes` and `edges`:

### Nodes:
- `REQUIREMENT`
- `RULE`
- `FACT`
- `EVIDENCE`
- `SOURCE_DOC`
- `GOVT_RECORD`
- `RISK_SIGNAL`
- `HUMAN_REVIEW`
- `OFFICER_DECISION`
- `AUDIT_BLOCK`

### Relationships:
- `EVALUATES_REQUIREMENT`
- `USES_FACT`
- `VERIFIED_BY`
- `DERIVED_FROM_DOC`
- `DERIVED_FROM_GOVT`
- `HAS_RISK_PROFILE`
- `REQUIRES_REVIEW`
- `FINAL_DECISION`
- `INCLUDES_OVERRIDE`

## 3. "Why?" Explainability Panel
Deterministic compliance explainability answers:
- **WHY PASS?**: Shows exact verified facts, policy version, and calculation trace.
- **WHY FAIL?**: Displays failed threshold condition, fact source, and explanation.
- **WHY MISSING EVIDENCE?**: Shows mandatory requirement facts missing from submission documents.
- **WHY REVIEW REQUIRED?**: Highlights ambiguous, stale, or conflicting facts requiring human review.

All AI-generated summaries are visually and structurally labeled **`AI ADVISORY — NON-AUTHORITATIVE`**.
