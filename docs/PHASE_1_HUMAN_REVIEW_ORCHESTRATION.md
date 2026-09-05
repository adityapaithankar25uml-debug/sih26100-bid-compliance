# Phase 1 — Human Review Orchestration & Checkpoint Pause/Resume Specification

## Overview

The **Human Review Orchestration Specification** defines how the workflow engine pauses execution at review checkpoints, queues tasks in the Procurement Officer Workbench UI, handles non-mutating manual overrides, and safely resumes workflow execution within the **SIH26100 Bid Compliance Verification Platform**.

This architecture integrates the Human-in-the-Loop gates defined in Task 4 (AI), Task 5 (Government Integrations), and Task 6 (Rules Engine).

---

## 1. Checkpoint Pause Architecture & Trigger Inventory

When a workflow evaluation encounters any of the 10 formal escalation conditions, the orchestrator triggers a **Checkpoint Pause**:

```
[Active Task Execution] ──► [Inspect Escalation Triggers]
                                      │
         ┌────────────────────────────┴────────────────────────────┐
         ▼ (No Escalation Trigger)                                 ▼ (Escalation Trigger Met)
[Proceed to Next Task Node]                                [1. Persist Checkpoint Payload]
                                                           [2. Transition State: WAITING]
                                                           [3. Queue Item in Officer Workbench]
                                                           [4. Emit WORKFLOW_PAUSED Event]
```

### 1.1 Escalation Trigger Inventory & Checkpoint Routing

| Trigger Code | Trigger Category | Originating Subsystem | Checkpoint Routing & Work Queue |
| :--- | :--- | :--- | :--- |
| **`CONFLICTING_EVIDENCE`** | Multi-Source Contradiction | Fact Normalization (Task 5/6) | Route to `DISCREPANCY_QUEUE` |
| **`AMBIGUOUS_IDENTITY`** | Name/Identity String Mismatch | Govt Adapters (Task 5) | Route to `IDENTITY_VERIFICATION_QUEUE` |
| **`MISSING_MANDATORY_EVIDENCE`**| Missing Document / Credential | Compliance Engine (Task 6) | Route to `EVIDENCE_CLARIFICATION_QUEUE` |
| **`STALE_EVIDENCE`** | Expired Freshness Window | Govt Source Registry (Task 5) | Route to `FRESHNESS_REVIEW_QUEUE` |
| **`SOURCE_UNAVAILABLE`** | Govt Outage / Max Retries | Govt Adapters (Task 5) | Route to `MANUAL_FALLBACK_QUEUE` |
| **`RULE_CONFLICT`** | Contradictory Rule Outcomes | Compliance Engine (Task 6) | Route to `POLICY_REVIEW_QUEUE` |
| **`POLICY_AMBIGUITY`** | Overlapping Policy Versions | Policy Engine (Task 6) | Route to `POLICY_REVIEW_QUEUE` |
| **`LOW_AI_CONFIDENCE`** | OCR / Extraction Uncertainty | AI Gateway (Task 4) | Route to `EXTRACTION_VERIFICATION_QUEUE` |
| **`MANUAL_OVERRIDE_REQ`** | Officer Challenge Initiated | Officer Workbench (Task 6) | Route to `OVERRIDE_REVIEW_QUEUE` |
| **`EXCEPTIONAL_CLAUSE`** | Mandatory Sign-off Clause | Tender Manager (Task 2) | Route to `OFFICER_SIGN_OFF_QUEUE` |

---

## 2. Checkpoint Resume Architecture & Non-Mutating Overrides

```mermaid
sequenceDiagram
    autonumber
    participant WB as Officer Workbench UI
    participant Off as Procurement Officer
    participant Orch as Workflow Orchestrator
    participant Engine as Compliance Engine (Task 6)
    participant Audit as Audit Hash-Chain Engine

    Orch->>WB: Render Task Item (Status: WAITING, Queue: DISCREPANCY_QUEUE)
    WB->>Off: Display Deterministic Trace, Evidence Citations & Escalation Reason

    alt Case 1: Officer Approves Machine Recommendation
        Off->>WB: Confirm Recommendation (Enter Decision Rationale)
        WB->>Orch: Submit Officer Action -> `ACTION_CONFIRM_RECOMMENDATION`
        Orch->>Audit: Append OfficerDecision Event Block
    else Case 2: Officer Executes Manual Override
        Off->>WB: Submit Manual Override (Status: PASS/FAIL + Mandatory Justification + Proof)
        WB->>Orch: Submit Officer Action -> `ACTION_MANUAL_OVERRIDE`
        Orch->>Audit: Append Co-Existing ManualOverride Block
    end

    Orch->>Engine: Re-evaluate Aggregated Submission Qualification Outcome
    Orch->>Orch: Load Preserved Checkpoint -> Transition State: RUNNING
    Orch->>Audit: Emit WORKFLOW_RESUMED Event
    Orch->>Orch: Dispatch Next Downstream DAG Task Node
```

---

## 3. Policy-Controlled Four-Eyes Review Governance

In accordance with Task 5 and Task 6 architecture, four-eyes / dual-control review is **policy-controlled**:

* **Policy-Configurable Requirement:** Governance policy (`PolicyVersion`) specifies whether four-eyes dual-control is mandatory for specific high-risk actions (e.g., overriding a debarment signal or waiving major financial turnover criteria).
* **Single-Officer Action:** For routine workflows where four-eyes is not mandated by policy, sign-off by the primary authorized Procurement Officer resumes the workflow immediately.
* **Dual-Officer Workflow:** Where four-eyes is mandated by policy, the initial officer action transitions the task to `PENDING_SECOND_OFFICER_APPROVAL`. The workflow resumes only after a secondary authorized officer authenticates and approves the decision.

---

## 4. Preservation of Machine History Invariant

> [!CAUTION]
> **IMMUTABILITY OF MACHINE EVALUATIONS:**
> Officer decision submission or manual override **NEVER** mutates or overwrites historical `ComplianceEvaluation` records or `EvaluationTrace` logs.
> The original machine trace remains permanently locked. The officer's action co-exists as an auditable `ManualOverride` or `OfficerDecision` block linked in the tamper-evident audit hash-chain.
