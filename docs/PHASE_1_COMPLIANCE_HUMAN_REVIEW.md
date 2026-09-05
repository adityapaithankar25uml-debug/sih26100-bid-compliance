# Phase 1 — Compliance Human Review & Officer Decision Architecture

## Overview

The **Compliance Human Review & Officer Decision Architecture** defines the governance gates, escalation triggers, and override mechanisms that connect deterministic rule evaluation outputs to Procurement Officer decision workflows in the **SIH26100 Bid Compliance Verification Platform**.

---

## 1. Human Review Gate Triggers (10 Escalation Conditions)

When an evaluation cannot be resolved deterministically due to insufficient evidence, ambiguity, or escalation triggers, the Compliance Engine automatically sets `requires_human_review = True` and transitions the requirement evaluation to `REQUIRES_HUMAN_REVIEW`:

```
[Requirement Evaluation] ──► [Inspect Evaluation Status & Flags]
                                          │
        ┌─────────────────────────────────┴─────────────────────────────────┐
        ▼ (Deterministically Verified)                                      ▼ (Escalation Trigger Met)
[Status: PASS / FAIL]                                       [Status: REQUIRES_HUMAN_REVIEW]
                                                                            │
                                                                            ▼
                                                            [Escalate to Officer Workbench]
```

### 1.1 Escalation Trigger Catalog
1. **`CONFLICTING_EVIDENCE`:** Contradictory information returned across multiple government sources or bidder documents.
2. **`AMBIGUOUS_IDENTITY`:** Legal entity string comparison produces ambiguous similarity flags requiring human confirmation.
3. **`MISSING_MANDATORY_EVIDENCE`:** A required document or credential is absent from the bidder submission.
4. **`STALE_EVIDENCE`:** Evidence timestamp exceeds the allowed policy freshness window.
5. **`SOURCE_UNAVAILABLE`:** Upstream government portal outage, timeout, or circuit breaker activation.
6. **`RULE_CONFLICT`:** Two active rules produce contradictory outcomes for the same requirement.
7. **`POLICY_AMBIGUITY`:** Overlapping or ambiguous policy versions require administrative precedence interpretation.
8. **`LOW_AI_EXTRACTION_CONFIDENCE`:** AI/OCR document field extraction confidence falls below configured threshold.
9. **`MANUAL_OVERRIDE_REQUESTED`:** Procurement Officer initiates a formal challenge or override request.
10. **`EXCEPTIONAL_PROCUREMENT_CONDITION`:** Non-standard tender clause marked for mandatory officer sign-off.

### 1.2 Multi-Dimensional Source & Evaluation Quality Taxonomy
To prevent collapsing disparate operational values into a single ambiguous "confidence" metric, the platform explicitly distinguishes seven independent evaluation dimensions:
1. **Source Authority:** The formal authoritative standing of the data provider (e.g., GSTN official portal vs self-declared PDF).
2. **Verification Status:** Explicit fact states (`VERIFIED`, `UNVERIFIED`, `MISSING`, `STALE`, `CONFLICTING`, `INVALID`, `UNKNOWN`, `NOT_APPLICABLE`).
3. **Source Freshness:** Compliance of source information timestamp with policy-configured freshness windows.
4. **Evidence Quality:** Technical completeness, legibility, relevance, and cryptographic integrity of supporting document evidence.
5. **Identity Match Quality:** String match and entity mapping quality between verified external records and bidder identity.
6. **AI Extraction Confidence:** Probabilistic confidence that AI/OCR correctly parsed document fields.
7. **Rule/Factual Determination:** The deterministic AST rule evaluation result (`PASS`, `FAIL`, `MISSING_EVIDENCE`, etc.).

> [!NOTE]
> **STATUS ISOLATION:** A technical or source issue (e.g. low OCR confidence, government portal timeout) must **NEVER** automatically trigger a compliance `FAIL`. Where evidence quality or identity matching is ambiguous, the system routes the item to `REQUIRES_HUMAN_REVIEW` for officer determination according to policy.

---

## 2. Procurement Officer Decision Workflow

Procurement Officers interact with evaluations via the Procurement Officer Workbench UI:

```mermaid
sequenceDiagram
    autonumber
    participant Engine as Compliance Rule Engine
    participant WB as Officer Workbench UI
    participant Off as Procurement Officer
    participant Audit as Audit Hash-Chain Engine

    Engine->>WB: Render Evaluation Task (Status: REQUIRES_HUMAN_REVIEW)
    WB->>Off: Display Deterministic Trace, Evidence Links & Escalation Reason

    alt Officer Approves Deterministic Recommendation
        Off->>WB: Confirm Recommendation (Enter Decision Notes)
        WB->>Audit: Append OfficerDecision Block (Approved)
    else Officer Overrides Deterministic Recommendation
        Off->>WB: Initiate Manual Override (Select Override Status & Attach Proof)
        WB->>Off: Request Mandatory Justification Rationale
        Off->>WB: Submit Signed Override Request
        WB->>Audit: Append ManualOverride Block (Co-existing Override)
    end

    Audit-->>WB: Return Audit Transaction Hash
    WB-->>Engine: Update Submission Qualification Outcome
```

---

## 3. Auditable `ManualOverride` Preservation Model

To preserve legal integrity and pass CVC vigilance audits, a `ManualOverride` **never overwrites or mutates** the original deterministic `ComplianceEvaluation` record:

```
+-----------------------------------------------------------------------------------+
|                        HISTORICAL DETERMINISTIC EVALUATION                        |
|  * evaluation_id: 01J7EVAL001                                                     |
|  * original_status: REQUIRES_HUMAN_REVIEW                                         |
|  * rule_id: RULE-FIN-TURNOVER-GTE                                                 |
|  * evaluated_at: 2026-09-05T14:30:05Z (LOCKED / UNALTERED)                        |
+-----------------------------------------------------------------------------------+
                                          │
                                          │ Co-exists With
                                          ▼
+-----------------------------------------------------------------------------------+
|                            AUDITABLE MANUAL OVERRIDE                              |
|  * override_id: 01J7OVERRIDE001                                                   |
|  * evaluation_id: 01J7EVAL001                                                     |
|  * overridden_by_officer_id: USR_OFFICER_442                                      |
|  * override_status: PASS                                                          |
|  * mandatory_justification: "Bidder presented certified supplementary CA audit   |
|    statement confirming FY25 turnover of ₹12.5 Cr."                               |
|  * evidence_attachment_hash: SHA-256 (ca_supplementary_statement.pdf)             |
|  * override_timestamp: 2026-09-05T15:00:00Z                                       |
+-----------------------------------------------------------------------------------+
```

Both the original evaluation trace and the co-existing `ManualOverride` record are linked to the final `OfficerDecision` block in the tamper-evident audit hash-chain.

---

## 4. Policy-Configurable Four-Eyes Review Governance

* **Policy-Controlled Four-Eyes Review:** Four-eyes / dual-control review is policy-controlled. It may be configured as mandatory for specified high-risk actions, major threshold overrides, sensitive debarment overrides, or high-value tenders according to organizational governance policy.
* **Non-Hardcoded Governance:** Four-eyes review is **not** universally hardcoded as mandatory for every single human override.
* **Separation of Duties:** When four-eyes review is enabled by policy for a workflow, the system enforces separation of duties by requiring distinct approving and verifying Procurement Officers and recording both authentication credentials in the audit block.
* **Single-Officer Workflows:** When four-eyes review is not enabled by policy for a routine workflow, the primary authorized officer's sign-off completes the decision block in accordance with configured policy rules.

