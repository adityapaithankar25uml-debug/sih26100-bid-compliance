# Phase 4 — Deterministic Compliance Engine Implementation

## 1. Zero LLM Evaluation Invariant
The Phase 4 Compliance Engine is **100% deterministic**. LLMs and neural models are strictly prohibited from evaluating compliance rules, calculating thresholds, or deciding bidder qualification.

## 2. AST Constrained Rule Engine Security
Rules are evaluated via an AST (Abstract Syntax Tree) expression interpreter (`ConstrainedRuleEvaluator`).

### Blocked Security Operations
The AST evaluator strictly rejects unsafe nodes:
- `eval()`, `exec()`, arbitrary code injection.
- Dynamic module imports (`__import__`).
- System/subprocess execution (`os`, `sys`, `subprocess`).
- Direct file or network access.

Attempting to execute arbitrary script code raises `ASTExecutionError` and aborts evaluation.

## 3. Evaluation Taxonomies
Rule result states:
- `PASS`: Fact values satisfy AST condition with traceable evidence.
- `FAIL`: Fact values deterministically breach AST condition.
- `MISSING_EVIDENCE`: Fact is missing or unverified. (Does NOT fail bidder).
- `UNKNOWN`: Fact verification state is unknown.
- `REVIEW_REQUIRED`: Fact value requires human officer decision.

Overall submission qualification state:
- `COMPLIANT`
- `NON_COMPLIANT`
- `REQUIRES_REVIEW`
- `INCOMPLETE`
