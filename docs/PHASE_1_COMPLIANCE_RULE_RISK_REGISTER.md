# Phase 1 — Compliance Engine Risk Register

## Overview

The **Compliance Engine Risk Register** details technical, operational, legal, and security risks associated with executing deterministic compliance rules within the **SIH26100 Bid Compliance Verification Platform**.

Each identified risk is paired with architectural mitigations and continuous operational monitoring controls.

---

## 1. Master Risk Matrix (12 Rules Engine Risks)

| Risk ID | Category | Risk Description | Likelihood | Impact | Architectural Mitigation Strategy | Monitoring & Control Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RISK-RULE-01** | Security | **Dynamic Code Execution Attack**<br>Attacker injects Python expression into rule condition attempting `eval()` execution. | Low | Critical | Strict Non-Executable AST architecture. Engine uses pure JSON-AST tree traversal with zero `eval()` or `exec()` calls. | Static AST schema validation & AST pre-parser inspection. |
| **RISK-RULE-02** | Integrity | **Un-versioned Policy Modification**<br>Policy parameters updated in-place, rewriting historical evaluation results. | Medium | High | Immutable `PolicyVersion` entity model. Evaluations permanently anchored to historical policy version snapshot. | Audit hash-chain verification & DB immutability triggers. |
| **RISK-RULE-03** | Performance | **Requirement Dependency Graph Cycle**<br>Circular requirement dependency causes evaluation loop/stack overflow. | Medium | High | Pre-evaluation Tarjan DAG cycle detection. Rejects cyclic requirement definitions during static analysis. | Graph topology validation checks during rule activation. |
| **RISK-RULE-04** | Accuracy | **Floating-Point Rounding Divergence**<br>IEEE 754 float errors cause threshold comparison miscalculations (e.g., ₹9.9999999 Cr). | High | Medium | Arbitrary-precision decimal arithmetic (Decimal type) for all currency and percentage comparisons. | Type enforcement unit tests in AST comparison evaluators. |
| **RISK-RULE-05** | Logic | **Timezone Boundary Ambiguity**<br>Submission timestamp near midnight evaluated against wrong policy window. | Medium | Medium | Canonical UTC timestamp normalization across all inputs, facts, and policy effective windows. | ISO 8601 UTC timestamp validators in Fact Factory. |
| **RISK-RULE-06** | Governance | **AI Output Bypass of Evidence**<br>AI extraction confidence score treated as authoritative compliance proof. | Medium | High | Absolute AI Boundary. Rule engine consumes only validated `NormalizedFact` objects bound to `EvidenceRecord` hashes. | Grounding verification checks in trace generator. |
| **RISK-RULE-07** | Logic | **Active Rule Conflict**<br>Two active rules yield contradictory results for the same requirement. | Low | High | Rule conflict detection engine. Conflicting outcomes transition evaluation to `RULE_CONFLICT` $\rightarrow$ `REQUIRES_HUMAN_REVIEW`. | Static rule overlap analyzer in administrative workbench. |
| **RISK-RULE-08** | Classification| **Missing Data Misclassified as Fail**<br>Missing document fact automatically sets requirement to `FAIL`. | High | High | Strict Status Separation: $\text{MissingFact} \implies \text{MISSING\_EVIDENCE} \neq \text{FAIL}$. Only verified false conditions yield `FAIL`. | Automated evaluation status assertion unit tests. |
| **RISK-RULE-09** | Governance | **Un-Audited Manual Override**<br>Procurement Officer overrides rule result without recorded rationale or proof. | Low | High | Mandatory justification rationale, attachment hash, and dual-officer co-signing for high-risk manual overrides. | CVC vigilance audit trails & hash-chain validation. |
| **RISK-RULE-10** | Performance | **Batch Evaluation Starvation**<br>Complex tender requirement evaluation blocks worker thread looper. | Medium | Medium | Celery queue isolation, worker pool limits, per-rule execution timeout bounds (e.g., 500ms max per AST). | Celery task execution duration metrics & alert counters. |
| **RISK-RULE-11** | Accuracy | **Currency Unit Mismatch**<br>Bidder turnover in Lakhs compared against threshold in Crores without normalization. | Medium | High | Mandatory `CurrencyNormalizer` transforming all financial facts to canonical INR base values prior to comparison. | Unit-aware fact schema validators in Fact Builder. |
| **RISK-RULE-12** | Integrity | **Historical Evaluation Mutation**<br>Rule engine upgrade silently alters previously completed evaluation outputs. | Medium | High | EvaluationSnapshot locking. Re-evaluations use historical snapshot AST and policy versions, preserving original outputs. | Automated regression test suite against historical snapshots. |
