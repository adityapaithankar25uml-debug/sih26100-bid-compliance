# Phase 1 — Rule Testing, Validation & Invariant Architecture

## Overview

The **Rule Testing, Validation & Invariant Architecture** specifies the testing frameworks, static analysis validation tools, and mathematical invariant checks that ensure all compliance rules in the **SIH26100 Bid Compliance Verification Platform** are safe, deterministic, and free from circular dependencies or logic conflicts.

---

## 1. Rule Test Suite & Governance Schema (8 Standard Profiles)

Before a `ComplianceRule` can transition through the governance lifecycle (`DRAFT` $\rightarrow$ `VALIDATION` $\rightarrow$ `TESTING` $\rightarrow$ `REVIEW` $\rightarrow$ `APPROVED` $\rightarrow$ `ACTIVE`), it must undergo appropriate validation and testing:
* **Standard Coverage Taxonomy:** The platform defines 8 standard test profile categories for rule validation: `POSITIVE`, `NEGATIVE`, `BOUNDARY`, `MISSING_DATA`, `STALE_DATA`, `CONFLICTING_DATA`, `NOT_APPLICABLE`, and `INVALID_DATA`.
* **Applicable Profile Rule:** Applicable profiles from the taxonomy must be covered for each rule. If a specific test profile is genuinely not applicable to a rule (e.g., a numeric `BOUNDARY` case for a binary enum check), the exclusion rationale must be documented in the rule test metadata.
* **Activation Gate:** Rule activation requires successful validation and sign-off against its applicable test profile suite.

```json

{
  "rule_code": "RULE-FIN-TURNOVER-GTE",
  "test_suite_version": "1.0.0",
  "test_cases": [
    {
      "test_id": "TC-01-POSITIVE",
      "category": "POSITIVE_CASE",
      "description": "Turnover ₹15 Cr exceeds ₹10 Cr threshold",
      "input_facts": { "bidder_average_annual_turnover_inr": 150000000.00 },
      "policy_parameters": { "required_annual_turnover_inr": 100000000.00 },
      "expected_status": "PASS"
    },
    {
      "test_id": "TC-02-NEGATIVE",
      "category": "NEGATIVE_CASE",
      "description": "Turnover ₹8 Cr is below ₹10 Cr threshold",
      "input_facts": { "bidder_average_annual_turnover_inr": 80000000.00 },
      "policy_parameters": { "required_annual_turnover_inr": 100000000.00 },
      "expected_status": "FAIL"
    },
    {
      "test_id": "TC-03-BOUNDARY-EXACT",
      "category": "BOUNDARY_CASE",
      "description": "Turnover exactly ₹10 Cr meets threshold",
      "input_facts": { "bidder_average_annual_turnover_inr": 100000000.00 },
      "policy_parameters": { "required_annual_turnover_inr": 100000000.00 },
      "expected_status": "PASS"
    },
    {
      "test_id": "TC-04-MISSING-DATA",
      "category": "MISSING_DATA_CASE",
      "description": "Turnover fact missing from submission",
      "input_facts": {},
      "policy_parameters": { "required_annual_turnover_inr": 100000000.00 },
      "expected_status": "MISSING_EVIDENCE"
    },
    {
      "test_id": "TC-05-STALE-DATA",
      "category": "STALE_DATA_CASE",
      "description": "Fact timestamp older than policy window",
      "input_facts": { "bidder_average_annual_turnover_inr": 150000000.00 },
      "fact_status_override": "STALE",
      "expected_status": "STALE"
    },
    {
      "test_id": "TC-06-CONFLICTING-DATA",
      "category": "CONFLICTING_DATA_CASE",
      "description": "Discrepancy between audited balance sheet and tax return",
      "fact_status_override": "CONFLICTING",
      "expected_status": "CONFLICTING"
    },
    {
      "test_id": "TC-07-NOT-APPLICABLE",
      "category": "NOT_APPLICABLE_CASE",
      "description": "Startup exempt from turnover requirement",
      "applicability_override": false,
      "expected_status": "NOT_APPLICABLE"
    },
    {
      "test_id": "TC-08-INVALID-DATA",
      "category": "INVALID_DATA_CASE",
      "description": "Turnover value passed as negative string",
      "input_facts": { "bidder_average_annual_turnover_inr": "-500" },
      "expected_status": "INVALID_FACT"
    }
  ]
}
```

---

## 2. Structural & Property-Based Engine Invariants

The Compliance Engine enforces 10 mathematical and architectural invariants:

1. **Determinism Invariant:** For any fixed tuple $(\text{Facts}, \text{RuleAST}, \text{PolicyVersion})$, evaluation yields the identical result across all executions:
   $$\text{Eval}(F, R, P)_{t_1} \equiv \text{Eval}(F, R, P)_{t_2}$$
2. **Non-Mutation of History:** An evaluation snapshot created at time $t$ is immutable and permanently locked.
3. **No Code Execution:** Rule AST nodes contain zero executable code, callables, or external references.
4. **Missing Evidence Safety:** $\text{MissingFact} \implies \text{MISSING\_EVIDENCE} \neq \text{FAIL}$.
5. **Technical Failure Safety:** $\text{TransportError} \implies \text{REQUIRES\_HUMAN\_REVIEW} \neq \text{FAIL}$.
6. **Cycle Detection Invariant:** Requirement dependency graphs must be Directed Acyclic Graphs (DAGs). Circular dependencies (e.g., $A \rightarrow B \rightarrow A$) are rejected during static analysis.
7. **Rule Conflict Isolation:** Conflicting active rules yield `RULE_CONFLICT` $\rightarrow$ `REQUIRES_HUMAN_REVIEW`.
8. **Exemption Preservation:** `NOT_APPLICABLE` requirement outcomes never reduce bidder qualification standing.
9. **Grounding Invariant:** Every `PASS`/`FAIL` evaluation trace references valid, existing `EvidenceRecord` hashes.
10. **Human Supremacy:** Engine output is a recommendation; binding legal authority rests with `OfficerDecision`.

---

## 3. Dependency Graph Cycle Detection (DAG Validation)

Before executing batch evaluations, the engine performs Tarjan's Strongly Connected Components algorithm on the requirement dependency graph:

```
[Requirement Graph Built] ──► [Tarjan's DAG Cycle Check]
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼ (No Cycles - Valid DAG)             ▼ (Cycle Detected)
       [Proceed to Batch Evaluation]              [Reject Rule Activation: CYCLE_ERROR]
```
