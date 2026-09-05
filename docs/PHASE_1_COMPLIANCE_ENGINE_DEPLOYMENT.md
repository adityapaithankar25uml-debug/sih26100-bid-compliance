# Phase 1 — Compliance Engine Deployment Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Compliance Deployment Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the deployment environment for the Deterministic Compliance & Policy/Rules Engine (Task 6).

The non-negotiable compliance engine deployment rule is:
> **"The compliance engine executes pure, deterministic AST comparisons over schema-validated facts inside isolated worker containers. Dynamic code execution (`eval()`, `exec()`) and LLM-driven rule evaluations are strictly forbidden."**

---

## 2. Deterministic Compliance Engine Deployment Model

```mermaid
flowchart TD
    subgraph Execution_Container ["Isolated Celery Worker Task (Task 6 Engine)"]
        FactLoader["1. Load Schema-Validated NormalizedFacts"]
        PolicyBinder["2. Bind PolicyVersion & TenderVersion AST Rules"]
        ASTInterpreter["3. Execute Pure Python AST Tree Traversal (Non-Executable)"]
        SnapshotWriter["4. Generate EvaluationSnapshot & Hash Linkage"]
    end

    FactLoader --> PolicyBinder --> ASTInterpreter --> SnapshotWriter
    SnapshotWriter --> PostgreSQL[(\"PostgreSQL Primary DB\")]
```

---

## 3. Compliance Engine Runtime Controls

1. **AST Resource Limits:** AST tree evaluation execution is capped at a maximum expression depth of 10 nodes and maximum execution time of 100ms per rule evaluation.
2. **Immutable Version Binding:** Rule execution binds to an immutable `PolicyVersion` record; rule logic cannot be altered during an active evaluation pass.
3. **Status Separation Integrity:** If evidence is missing (`MISSING_EVIDENCE`), the engine strictly routes the requirement to `REQUIRES_HUMAN_REVIEW` without emitting a `FAIL` status.
