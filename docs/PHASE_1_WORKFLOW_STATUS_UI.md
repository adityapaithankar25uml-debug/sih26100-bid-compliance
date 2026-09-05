# Phase 1 — Workflow Status UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Workflow Status UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Workflow Progress Scope

This specification defines the UI visualization components for tracking Celery workflow state machines, active DAG pipeline stages, and Task 7 execution status badges.

---

## 2. Workflow State Machine Display Topology

```
+-----------------------------------------------------------------------------------+
| WORKFLOW PIPELINE TRACKER: Bidder #BID-409 (Alpha Engineering)                     |
| Workflow Instance ID: `wf_01J891A2345` | Execution Mode: AT_LEAST_ONCE             |
+-----------------------------------------------------------------------------------+
| PIPELINE DAG STAGE TRAVERSAL                                                      |
| [ Ingest Package ] -> [ Disarm & OCR ] -> [ Govt Verifications ] -> [ Rule Engine ] -> [ Human Review ]
|    SUCCEEDED            SUCCEEDED            SUCCEEDED                  SUCCEEDED            PAUSED_CHECKPOINT
+-----------------------------------------------------------------------------------+
| WORKFLOW EXECUTION METADATA                                                       |
| - Technical Execution State: `SUCCEEDED` (DAG tasks completed cleanly)            |
| - Business Domain State: `EVALUATED`                                              |
| - Compliance Status: `VERIFIED`                                                   |
| - Checkpoint Status: `PAUSED_CHECKPOINT` (Awaiting Officer Final Decision)        |
+-----------------------------------------------------------------------------------+
```

---

## 3. Multidimensional Isolation Rules

1. **State Isolation Preservation:** UI explicitly keeps technical task execution states (`SUCCEEDED`, `RUNNING`) isolated from business qualification status (`QUALIFIED`, `NOT_QUALIFIED`).
2. **Two-Phase Cancellation Visualizer:** If a workflow cancellation is requested, UI renders `CANCEL_REQUESTED` before transitioning cleanly to `CANCELLED`.
