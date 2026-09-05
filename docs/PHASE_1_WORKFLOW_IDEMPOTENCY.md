# Phase 1 — Workflow & Task Idempotency Architecture Specification

## Overview

The **Workflow & Task Idempotency Architecture Specification** defines how the **SIH26100 Bid Compliance Verification Platform** prevents duplicate side effects, duplicate job dispatches, and duplicate government API requests during workflow execution.

This architecture explicitly adopts **At-Least-Once Task Delivery with Idempotent Task Handlers**, ensuring that repeated execution of any workflow task yields identical database state and evidence records without duplicate side effects.

---

## 1. Idempotency Boundary & Delivery Semantics

> [!IMPORTANT]
> **AT-LEAST-ONCE DELIVERY WITH IDEMPOTENT HANDLERS:**
> Distributed queue systems cannot guarantee exactly-once network delivery across worker failures.
> Therefore, the platform implements **At-Least-Once Delivery** at the queue layer, backed by **Strict Idempotent Handlers** at the application and workflow orchestration layers.
>
> **LOGICAL OPERATION IDENTITY VS EXECUTION ATTEMPTS:**
> Logical operations are protected against duplicate side effects through durable idempotency records, uniqueness/transactional coordination, and concurrency-safe handler semantics, while each legitimate retry may create a distinct `TaskAttempt`. A retry/new `TaskAttempt` is an execution trace of a retry and is not a duplicate logical `WorkflowTask`.

```
[Client / API Gateway] ──► [HTTP Header: X-Idempotency-Key]
                                        │
                                        ▼
[Idempotency Key Lock Store] ──► [Check Existing Request Hash]
                                        │
        ┌───────────────────────────────┴───────────────────────────────┐
        ▼ (Key Found & Completed)                                       ▼ (New Idempotency Key)
[Return Cached Response / Job Reference]                [1. Coordinate Idempotency Lock]
                                                        [2. Execute Workflow Instance]
                                                        [3. Store Output + Key Hash]
```

---

## 2. Multi-Level Idempotency Keys

Idempotency is enforced across 4 distinct operational tiers:

| Operational Level | Idempotency Key Formula | Scope & Retention Period | Storage / Coordination Engine |
| :--- | :--- | :--- | :--- |
| **1. API Command Level** | `hash(X-Idempotency-Key + endpoint + client_id)` | 24 Hours | Redis / Key Cache |
| **2. Workflow Instance Level** | `hash(submission_id + tender_version_id + workflow_type)` | Submission Lifecycle | PostgreSQL `workflow_instances` |
| **3. Task Execution Level** | `hash(workflow_instance_id + task_code + task_input_hash)` | Workflow Lifecycle | PostgreSQL `workflow_tasks` |
| **4. Govt Verification Level** | `hash(source_code + entity_identifier + freshness_window_id)` | Policy Freshness Window (e.g., 30 Days) | PostgreSQL `government_verification_results` |


---

## 3. Idempotent Task Handler Execution Contract

Every workflow task handler must conform to the idempotent execution contract. Note that specific locking patterns (such as database row locks or Redis mutexes) represent implementation options rather than frozen architectural requirements:

```python
# Conceptual Idempotent Task Execution Contract (Zero side-effect duplication)
def execute_idempotent_task(task_id: ULID, context: WorkflowContext) -> TaskResult:
    # 1. Fetch task record & check if already completed
    task = db.get_task(task_id)
    if task.status == "COMPLETED":
        return TaskResult(status="SKIPPED_ALREADY_COMPLETED", output=task.output_payload)

    # 2. Acquire task execution lock (Implementation Option)
    with db.acquire_task_lock(task_id):
        # Re-check status inside lock (Double-Checked Locking Pattern)
        if task.status == "COMPLETED":
            return TaskResult(status="SKIPPED_ALREADY_COMPLETED", output=task.output_payload)

        # 3. Check downstream side-effect store (e.g. EvidenceRecord already exists?)
        existing_evidence = db.get_evidence_by_hash(task.input_hash)
        if existing_evidence:
            task.update_status("COMPLETED", output=existing_evidence.payload)
            return TaskResult(status="REUSED_EXISTING_EVIDENCE", output=existing_evidence.payload)

        # 4. Perform actual task work (e.g., call government adapter or AST evaluator)
        output = perform_task_logic(task.input_payload)

        # 5. Atomically update task output and mark COMPLETED in single DB transaction
        db.save_task_output_and_complete(task_id, output)
        return TaskResult(status="COMPLETED", output=output)
```


---

## 4. Government Verification Side-Effect Prevention

To prevent overloading government web portals and avoid duplicate verification charges or rate-limit penalties (Task 5):

1. **Cached Result Lookup:** Before dispatching an outbound request to an authorized government source (e.g. GSTN), the worker checks if a valid, unexpired `GovernmentVerificationResult` exists within the policy freshness window (e.g. `POL_FRESHNESS_GST_30D`).
2. **Result Reuse:** If a valid result exists, the task reuses the verified result payload and attaches a new `EvidenceRecord` reference without issuing a duplicate HTTP call.
3. **Concurrent Request Coalescing:** If two parallel tasks request verification for the same entity simultaneously, a distributed lock ensures only one request is dispatched while the second task waits and consumes the result.
