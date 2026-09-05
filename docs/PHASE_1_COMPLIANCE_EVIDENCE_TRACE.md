# Phase 1 — Compliance Evidence Trace & Explainability Specification

## Overview

The **Compliance Evidence Trace & Explainability Architecture** specifies how the **SIH26100 Bid Compliance Verification Platform** links every compliance decision to its underlying evidence, generating machine-readable evaluation traces and grounded plain-language explanations.

This architecture ensures complete transparency for Procurement Officers, CVC vigilance auditors, and bidder grievance review committees.

---

## 1. Traceability & Explainability Axiom: Required Provenance Property

> [!IMPORTANT]
> **REQUIRED PROVENANCE DESIGN PROPERTY & DETERMINISTIC GROUNDING:**
> 1. **Required Design Property:** Material compliance evaluations must maintain traceable provenance to their supporting facts and evidence. `EvidenceRecord` references, source metadata, extraction provenance, timestamps, and relevant policy/rule versions must be preserved where applicable.
> 2. **Evaluation Blocking:** If required provenance is missing, invalid, conflicting, or insufficient for a material conclusion, the evaluation must be blocked from being treated as sufficiently evidenced and routed to the appropriate human-review state. The system must never fabricate provenance.
> 3. **Template-Grounded Explanations:** Explanations presented in Procurement Officer Workbenches or audit reports are generated directly from machine-readable `EvaluationTrace` logs using pre-approved template rendering. AI models may summarize deterministic evaluation traces for presentation readability, but **AI models are strictly forbidden from generating un-grounded, free-form explanations** that lack direct evaluation trace backing.


---

## 2. Machine-Readable `EvaluationTrace` Data Contract

Every `ComplianceEvaluation` generates a structured, immutable `EvaluationTrace` stored alongside the evaluation record:

```json
{
  "trace_id": "01J7TRACE000000000000000001",
  "evaluation_id": "01J7EVAL000000000000000001",
  "requirement_id": "01J7REQ0000000000000000001",
  "rule_id": "RULE-FIN-TURNOVER-GTE",
  "rule_version": 1,
  "policy_version_id": "POL-MII-LOCAL-CONTENT-v2026.1",
  "evaluated_at": "2026-09-05T14:30:05Z",
  "result_status": "PASS",
  "evaluation_steps": [
    {
      "step_number": 1,
      "description": "Fetch input fact 'bidder_average_annual_turnover_inr'",
      "fact_key": "bidder_average_annual_turnover_inr",
      "fact_value": 150000000.00,
      "evidence_id": "01J7A8EVIDENCE0000000000001",
      "evidence_hash": "a4f8b91c...8821a90e"
    },
    {
      "step_number": 2,
      "description": "Resolve policy parameter 'required_annual_turnover_inr'",
      "parameter_key": "required_annual_turnover_inr",
      "parameter_value": 100000000.00,
      "policy_version": "v2026.1.0"
    },
    {
      "step_number": 3,
      "description": "Execute AST Comparison GTE: 150000000.00 >= 100000000.00",
      "comparison_operator": "GTE",
      "operand_left": 150000000.00,
      "operand_right": 100000000.00,
      "step_result": true
    }
  ],
  "rendered_explanation": "Requirement PASSED: Bidder average annual turnover of ₹15.00 Crore meets or exceeds the required policy threshold of ₹10.00 Crore (Ref: Clause 4.2, Policy POL-MII-v2026.1). Evidence verified from Audited Financial Statement (Evidence ID: 01J7A8EVIDENCE0000000000001).",
  "trace_hash": "e7d1...9902"
}
```

---

## 3. End-to-End Evidence Traceability Chain

The trace links the final UI explanation back through the rule engine to raw verified documents:

```
[Procurement Officer Workbench UI]
  └─ Displayed Explanation: "Bidder turnover ₹15 Cr >= ₹10 Cr threshold"
        │
        ▼ (Renders From)
[EvaluationTrace Log] (trace_id: 01J7TRACE...)
        │
        ▼ (References)
[ComplianceEvaluation] (status: PASS)
        │
        ▼ (Evaluated Via)
[ComplianceRule] (condition_ast: GTE) + [PolicyVersion] (parameter: 10 Cr)
        │
        ▼ (Consumes)
[NormalizedFact] (value: 15 Cr, status: VERIFIED)
        │
        ▼ (Linked To)
[EvidenceRecord] (evidence_hash: a4f8...)
        │
        ▼ (Extracted From)
[ExtractedField] (document_id: 01J7DOC..., page: 4, bbox: [120, 340, 480, 380])
        │
        ▼ (Stored In)
[SourceDocument] (MinIO PDF object: audited_balance_sheet_2025.pdf)
```

---

## 4. Grounding Validation & Hallucination Prevention

Before an explanation is exported to vigilance reports or displayed in officer workbenches:

1. **Grounding Verification:** The platform checks that every evidence ID (`evidence_id`), page number, bounding box, and document reference cited in the trace exists in PostgreSQL and MinIO.
2. **Hash Check:** The trace SHA-256 hash (`trace_hash`) is verified against the signed audit hash-chain block.
3. **Rejection Control:** Any explanation missing traceable evidence or failing hash verification is rejected and replaced with structured rule facts.
