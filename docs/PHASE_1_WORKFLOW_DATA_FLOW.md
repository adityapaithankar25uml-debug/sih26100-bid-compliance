# Phase 1 — End-to-End Workflow Data Flow & Sequence Architecture Specification

## Overview

The **End-to-End Workflow Data Flow Specification** documents the data movement, payload transformations, state persistence, and inter-subsystem data flows across all 12 stages of the **SIH26100 Bid Compliance Verification Platform**.

---

## 1. Master End-to-End Data Flow Architecture

```
[User / GeM API] ──► (POST /evaluate) ──► [API Ingress (Task 3)]
                                                   │
                                                   ▼ (Creates Job & Workflow Instance)
                                     [Workflow Orchestrator (Task 7)]
                                                   │
        ┌───────────────────┬──────────────────────┼──────────────────────┬───────────────────┐
        ▼                   ▼                      ▼                      ▼                   ▼
[Document Intake]   [AI Extraction]        [Govt Adapters]        [Rules Engine]     [Risk Scoring]
(PDFs -> MinIO)     (Fields -> JSON)       (APIs -> Verification) (Facts -> AST)    (Profile -> Score)
        │                   │                      │                      │                   │
        └───────────────────┴──────────────────────┼──────────────────────┴───────────────────┘
                                                   │
                                                   ▼
                                      [Evidence Assembly (Task 5)]
                                                   │
                                                   ▼
                                     [Human Review Gate (Task 6)]
                                                   │
                       ┌───────────────────────────┴───────────────────────────┐
                       ▼ (Escalation Triggered)                                ▼ (Direct Recommendation)
          [Officer Workbench UI (Task 6)]                            [Officer Sign-Off UI]
                       │                                                       │
                       └───────────────────────────┬───────────────────────────┘
                                                   │
                                                   ▼
                                      [Tamper-Evident Audit (Task 2)]
```

---

## 2. Comprehensive Execution Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as Procurement Officer
    participant API as REST API Gateway (Task 3)
    participant Orch as Workflow Orchestrator (Task 7)
    participant AI as AI Gateway (Task 4)
    participant Govt as Govt Verification (Task 5)
    participant Engine as Rules Engine (Task 6)
    participant Audit as Tamper-Evident Audit (Task 2)
    participant WB as Officer Workbench (Task 6)

    User->>API: POST /api/v1/submissions/SUB-901/evaluate
    API->>Orch: Dispatch Job (workflow_instance_id: WF-901)
    API-->>User: HTTP 202 Accepted (job_id: JOB-901)

    Orch->>AI: Task 1: Classify & Extract Documents (PDFs)
    AI-->>Orch: Return Extracted Fields & Canvas Bounding Boxes
    
    Orch->>Govt: Task 2: Dispatch Parallel Govt Verification (GST, Udyam, PAN, MCA)
    Govt-->>Orch: Return Normalized Results & Evidence Records

    Orch->>Engine: Task 3: Evaluate Compliance AST Rules (Facts + PolicyVersion)
    Engine-->>Orch: Return Requirement Evaluations & Qualification Outcome

    alt Escalation Trigger Met (e.g. MISSING_EVIDENCE or CONFLICTING_DATA)
        Orch->>Orch: Pause Workflow at Checkpoint -> Set State: WAITING
        Orch->>WB: Queue Task Item in Discrepancy Work Queue
        Orch->>Audit: Log WORKFLOW_PAUSED Event
        
        User->>WB: Review Evaluation Trace & Perform Manual Override
        WB->>Orch: Submit Officer Decision / Override Payload
        Orch->>Audit: Append Co-Existing ManualOverride Block
        Orch->>Orch: Resume Workflow -> Set State: RUNNING
    end

    Orch->>Audit: Append Master Execution Block to Audit Hash-Chain
    Orch->>Orch: Set Final State: SUCCEEDED
    Orch-->>API: Update Job Progress: 100% (Status: SUCCEEDED)
```

---

## 3. Five Primary Execution Paths

1. **Happy Path (Direct Pass):** All documents present $\rightarrow$ AI extraction valid $\rightarrow$ Govt verification verified $\rightarrow$ Compliance rules pass $\rightarrow$ Qualification outcome `QUALIFIED` $\rightarrow$ Direct officer approval $\rightarrow$ Completion.
2. **Missing Evidence Path:** Required document absent $\rightarrow$ Rule returns `MISSING_EVIDENCE` $\rightarrow$ Escalation trigger met $\rightarrow$ Pause at checkpoint (`WAITING`) $\rightarrow$ Officer requests document clarification $\rightarrow$ Resume execution.
3. **Transient Failure Retry Path:** Government API timeout $\rightarrow$ Tier A transient retry triggered $\rightarrow$ Backoff sleep $\rightarrow$ Retry succeeds $\rightarrow$ Workflow resumes automatically.
4. **Manual Fallback Path:** Government API max retries exhausted $\rightarrow$ Activate `MANUAL_FALLBACK` adapter $\rightarrow$ Flag `NOT_VERIFIED` $\rightarrow$ Route item to Officer Workbench for manual document verification.
5. **Two-Phase Cancellation Path:** Officer issues cancel command $\rightarrow$ State transitions to `CANCEL_REQUESTED` $\rightarrow$ Active workers check cancellation flag and abort execution $\rightarrow$ Lock state to `CANCELLED` and write snapshot.
