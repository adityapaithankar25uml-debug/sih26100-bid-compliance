# Phase 1 — Graceful Two-Phase Workflow Cancellation Specification

## Overview

The **Graceful Two-Phase Workflow Cancellation Specification** defines how running or queued workflows are safely terminated upon authorization without corrupting database state, erasing audit histories, or leaving orphan tasks within the **SIH26100 Bid Compliance Verification Platform**.

---

## 1. Two-Phase Cancellation Protocol (`CANCEL_REQUESTED` $\rightarrow$ `CANCELLED`)

To prevent race conditions where a worker commits results while a cancellation is in progress, the system enforces a mandatory **Two-Phase Cancellation Protocol**:

```
[Cancel API Command] (POST /api/v1/workflows/{id}/cancel)
          │
          ▼
[Phase 1: Transition State to CANCEL_REQUESTED]
          │ • Set workflow execution state = CANCEL_REQUESTED
          │ • Revoke queued tasks in background queue
          │ • Set cancellation flag in Redis lock store
          │
          ▼
[Workers Inspect Cancellation Flag]
          │ • Running workers check `is_cancelled()` at task checkpoints
          │ • Workers abort active processing cleanly without output commit
          │
          ▼
[Phase 2: Transition State to CANCELLED]
            • Lock execution snapshot
            • Append WORKFLOW_CANCELLED block to audit hash-chain
            • Release workflow locks
```

---

## 2. Cancellation Matrix Across Pipeline Stages

| Pipeline Stage | Active Operation | Behavior Upon `CANCEL_REQUESTED` | Artifact & Audit Handling |
| :--- | :--- | :--- | :--- |
| **Queued / Intake** | Pending worker pick-up | Revoke queue message immediately. | Record `CANCELLED` status; zero artifacts created. |
| **Document AI Extraction** | AI layout parsing in progress | Worker aborts extraction at next page boundary. | Discard transient extraction buffers; retain uploaded raw PDF in MinIO. |
| **Govt Verification** | Outbound HTTP request in progress | Local worker aborts response handler. (External HTTP connection cannot be recalled). | Ignore out-of-flight HTTP response; do not commit result to active workflow. |
| **Compliance Rule AST** | In-memory AST tree walk | Abort AST evaluation loop immediately. | Discard partial evaluation result; retain inputs. |
| **Human Review Gate** | Paused in Officer Workbench | Remove item from active officer work queue. | Mark task `CANCELLED`; retain review log with cancellation note. |

---

## 3. Cancellation Security & Non-Erasure Invariants

1. **Policy-Controlled Retention & Audit Non-Erasure:** Audit records and uploaded source documents are retained according to the applicable retention policy and lifecycle configuration (Task 2). Cancellation does not erase audit history or bypass required evidence retention.
2. **Capability Check:** Cancellation requires explicit Procurement Officer capability (`WORKFLOW_CANCEL`). Standard bidders or unauthorized roles are forbidden from cancelling active evaluation workflows.
3. **Immutability of Cancelled State:** Once a workflow transitions to `CANCELLED`, it is locked against further state machine transitions. It cannot be resumed. (A new evaluation requires instantiating a new `WorkflowInstance`).

