# Phase 1 — Deterministic Compliance Engine Architecture

## Executive Summary & System Overview

The **Deterministic Compliance & Policy/Rules Engine Architecture** establishes the core evaluation subsystem for the **SIH26100 Bid Compliance Verification Platform**. Built specifically for **Ministry of Petroleum & Natural Gas (CPCL)** procurement compliance, this engine consumes structured facts derived from bidder documents, verified government integration results, policy versions, and tender requirement definitions to evaluate compliance deterministically, explainably, and reproducibly.

```
+---------------------------------------------------------------------------------------------------+
|                                 APPLICATION SERVICE LAYER                                         |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                               FACT GATHERING & PROVENANCE BINDING                                 |
|   * Document Extractions (ExtractedField)   * Government Verification Results (Verified Fields)    |
|   * Tender Metadata & TenderVersion         * PolicyVersion & Regulatory Rules                    |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                                 APPLICABILITY & DEPENDENCY ENGINE                                 |
|   * Filters Rules by Bidder Class (MSME / Startup / Local Supplier)                              |
|   * Evaluates Requirement Dependency Graph (DAG) & Detects Evaluation Cycles                      |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                            DETERMINISTIC RULE EXECUTION ENGINE (AST)                              |
|   * Executes Schema-Validated Condition Trees   * Zero eval() / Zero exec() / Zero LLM calls    |
|   * Evaluates Numeric, Threshold, Boolean, Range & Set-Membership Logic                           |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                               COMPLIANCE EVALUATION & TRACE ENGINE                                |
|   * Generates Requirement-Level ComplianceEvaluation (PASS / FAIL / PENDING / REVIEW)             |
|   * Builds Immutable Machine-Readable EvaluationTrace & Evidence Linkages                         |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                               QUALIFICATION OUTCOME AGGREGATOR                                    |
|   * Aggregates Requirement Evaluations into Submission Outcome (QUALIFIED / NOT_QUALIFIED / etc.)|
|   * Evaluates Disqualifying vs Material vs Non-Material Severity Classes                          |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                            PROCUREMENT OFFICER DECISION GATEWAY (UI)                              |
|   * Displays Deterministic Rule Traces, Evidence References, Mismatches & Manual Action Triggers |
|   * Captures Final Human Officer Decision (OfficerDecision & ManualOverride)                      |
+---------------------------------------------------------------------------------------------------+
```

---

## 1. Core Architectural Axiom & Task Ownership

### 1.1 The System Axiom
Every compliance determination in the platform adheres strictly to the foundational system axiom:

$$\text{AI Interprets} \longrightarrow \text{Authorized Sources Verify} \longrightarrow \text{Rules Evaluate} \longrightarrow \text{Evidence Proves} \longrightarrow \text{Human Approves}$$

### 1.2 Subsystem Ownership
Task 6 explicitly owns the **`RULES EVALUATE`** boundary:

```
┌───────────────────────────┐
│     AI INTERPRETS         │  (Task 4: Document Extraction, Clause Mining, Sensitivity Masking)
└───────────────────────────┘
              │
              ▼
┌───────────────────────────┐
│ AUTHORIZED SOURCES VERIFY │  (Task 5: Adapter Execution, Normalized Verification Results, Provenance)
└───────────────────────────┘
              │
              ▼
┌───────────────────────────┐
│      RULES EVALUATE       │  <=== [TASK 6 COMPLIANCE ENGINE BOUNDARY]
└───────────────────────────┘
              │
              ▼
┌───────────────────────────┐
│      EVIDENCE PROVES      │  (Tasks 2, 5 & 6: Immutable EvidenceRecords & Audit Hash-Chains)
└───────────────────────────┘
              │
              ▼
┌───────────────────────────┐
│      HUMAN APPROVES       │  (Tasks 1, 2 & 6: Procurement Officer Decision Workbench & Overrides)
└───────────────────────────┘
```

---

## 2. Absolute AI Boundary & Non-Authoritative Isolation

To prevent LLM hallucinations, non-deterministic drift, and unexplainable compliance determinations:

1. **No LLM Invocation During Rule Evaluation:** The Compliance Engine **never calls external or local LLMs** while evaluating compliance rules.
2. **No Natural Language Pass/Fail Queries:** The engine does not prompt an AI model with questions like *"Is this bidder compliant with Clause 4.2?"*.
3. **Structured Fact Pre-Condition:** AI-extracted fields (`ExtractedField`) become input facts for rules **only after** schema validation, confidence threshold verification, provenance binding, and pre-AI privacy scrubbing.
4. **Deterministic AST Execution:** Condition trees are evaluated strictly via type-safe, sandboxed abstract syntax tree (AST) evaluators.
5. **Traceability Guarantee:** Every generated `ComplianceEvaluation` references the exact `RuleVersion`, `PolicyVersion`, input `NormalizedFact` snapshot, and `EvidenceRecord` hashes.

---

## 3. Qualification Boundary & Responsibility Matrix

The architecture maintains a strict distinction between requirement evaluation, submission qualification, risk assessment, and human decision-making:

| Architectural Concept | Responsible Entity / Layer | Scope / Definition | Legal Authority |
| :--- | :--- | :--- | :--- |
| **`ComplianceEvaluation`** | Deterministic Compliance Engine | Evaluation of an individual requirement (e.g., GST Status, Turnover Threshold). | Rule-Based Fact Check |
| **`QualificationOutcome`** | Qualification Outcome Aggregator | Submission-level aggregate determination (e.g., `QUALIFIED`, `NOT_QUALIFIED`, `PENDING_REVIEW`). | Deterministic Summary |
| **`RiskAssessmentProfile`** | Risk Assessment Module | Statistical signal profiling (e.g., anomaly detection, extraction confidence flags). | Informational Risk Signal |
| **`OfficerDecision`** | Human Procurement Officer | Final binding approval, rejection, or qualification ruling on a bid submission. | Binding Legal Authority |
| **`ManualOverride`** | Human Procurement Officer | Auditable officer decision modifying a deterministic rule outcome with recorded rationale. | Auditable Human Ruling |

> [!CRITICAL]
> **RISK SCORES AND AI CONFIDENCE ARE NOT QUALIFICATION:**
> A high risk score or low AI extraction confidence does **NOT** constitute an automated compliance `FAIL` or bidder `DISQUALIFICATION`. Low confidence or anomaly flags transition the evaluation to `REQUIRES_HUMAN_REVIEW`, preserving bidder rights while prompting officer inspection.

---

## 4. Modular Monolith Component Structure

The Compliance Engine is organized as an isolated module within the backend architecture:

```
src/modules/compliance_engine/
├── orchestrator.py             # ComplianceEngineOrchestrator
├── applicability.py            # ApplicabilityEngine & Filter Handler
├── dependency_graph.py         # RequirementDependencyGraph & Cycle Detector
├── dsl/                        # Safe Rule DSL & AST Evaluator
│   ├── ast_nodes.py            # AST Node Definitions (JSON-Schema Validated)
│   ├── evaluator.py            # Deterministic AST Evaluator (Zero eval/exec)
│   └── operators.py            # Type-Safe Comparison & Logical Operators
├── facts/                      # Fact Model & Provenance Binder
│   ├── fact_builder.py         # NormalizedFact Factory
│   └── provenance.py           # Evidence-to-Fact Traceability Binder
├── evaluator.py                # Requirement & Rule Evaluation Runner
├── aggregator.py               # QualificationOutcome Aggregator
├── snapshot.py                 # EvaluationSnapshot Generator
├── test_runner.py              # Rule Test Suite & Invariant Validator
└── human_review.py             # Human Review Trigger & Override Handler
```

Direct mutation of rule evaluation states by external API clients or AI services is strictly prohibited. All compliance evaluations pass through the `ComplianceEngineOrchestrator`.
