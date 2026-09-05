# Phase 1 — Safe Rule DSL & AST Expression Architecture

## Overview

The **Safe Rule DSL & AST Expression Architecture** specifies the non-executable, schema-validated Abstract Syntax Tree (AST) model used to represent rule conditions within the **SIH26100 Bid Compliance Verification Platform**.

This architecture guarantees that all compliance rules are evaluated in a completely sandboxed, deterministic manner.

---

## 1. Absolute Security Axiom: Non-Executable Rule AST

> [!CAUTION]
> **STRICT PROHIBITION OF DYNAMIC CODE EXECUTION:**
> The compliance engine strictly prohibits the use of Python `eval()`, `exec()`, compile functions, shell scripts, dynamic code generators, or arbitrary string evaluation engines.
> All rule conditions are encoded as static, structural JSON AST objects. The evaluator walks the tree deterministically, resolving AST nodes against validated `NormalizedFact` dictionaries using type-safe internal operators.

---

## 2. AST Operator Taxonomy

The AST evaluator supports a closed set of 15 type-safe operators:

### 2.1 Logical Operators
* `AND`: Evaluates `True` if all child nodes evaluate `True`.
* `OR`: Evaluates `True` if any child node evaluates `True`.
* `NOT`: Negates the child node evaluation result.

### 2.2 Relational & Comparison Operators
* `EQ` (Equal): Checks if `fact_value == operand`.
* `NEQ` (Not Equal): Checks if `fact_value != operand`.
* `GT` (Greater Than): Checks if numeric `fact_value > operand`.
* `GTE` (Greater Than or Equal): Checks if numeric `fact_value >= operand`.
* `LT` (Less Than): Checks if numeric `fact_value < operand`.
* `LTE` (Less Than or Equal): Checks if numeric `fact_value <= operand`.

### 2.3 Set & String Operators
* `IN`: Checks if `fact_value` is contained within an array of allowed values.
* `NOT_IN`: Checks if `fact_value` is absent from an array.
* `CONTAINS`: Checks if string `fact_value` contains a required substring.
* `REGEX_MATCH`: Validates `fact_value` against a pre-compiled, safe regular expression.

### 2.4 Chronological Operators
* `DATE_BEFORE`: Checks if ISO 8601 `fact_date < operand_date`.
* `DATE_AFTER`: Checks if ISO 8601 `fact_date > operand_date`.

---

## 3. Structural AST Schema & Concrete Examples

An AST condition node conforms to a rigid structural schema:

```json
{
  "node_type": "LOGICAL | COMPARISON",
  "operator": "AND | OR | NOT | EQ | GTE | IN | DATE_AFTER | ...",
  "fact_key": "optional_string_key_for_comparison_nodes",
  "operand": "literal_value_or_policy_parameter_reference",
  "children": [ "array_of_nested_ast_nodes_for_logical_nodes" ]
}
```

### 3.1 Example 1: GST Active Status Rule AST (`RULE-GST-ACTIVE-STATUS`)
Checks if GST status is active and legal entity match status is valid:

```json
{
  "node_type": "LOGICAL",
  "operator": "AND",
  "children": [
    {
      "node_type": "COMPARISON",
      "operator": "EQ",
      "fact_key": "gstin_status",
      "operand": "Active"
    },
    {
      "node_type": "COMPARISON",
      "operator": "IN",
      "fact_key": "legal_name_match_status",
      "operand": ["EXACT_MATCH", "NORMALIZED_MATCH", "ALIAS_MATCH"]
    }
  ]
}
```

### 3.2 Example 2: Financial Turnover Threshold Rule AST (`RULE-FIN-TURNOVER-GTE`)
Evaluates whether bidder average turnover meets or exceeds the required threshold defined in policy:

```json
{
  "node_type": "COMPARISON",
  "operator": "GTE",
  "fact_key": "bidder_average_annual_turnover_inr",
  "operand": {
    "$policy_ref": "required_annual_turnover_inr"
  }
}
```

### 3.3 Example 3: MSME EMD Exemption Rule AST (`RULE-MSME-EMD-EXEMPTION`)
Determines if an MSME bidder is eligible for EMD fee exemption:

```json
{
  "node_type": "LOGICAL",
  "operator": "AND",
  "children": [
    {
      "node_type": "COMPARISON",
      "operator": "EQ",
      "fact_key": "bidder_msme_status",
      "operand": "VERIFIED"
    },
    {
      "node_type": "COMPARISON",
      "operator": "IN",
      "fact_key": "udyam_enterprise_category",
      "operand": ["MICRO", "SMALL"]
    }
  ]
}
```

---

## 4. AST Evaluator Execution Contract

The AST Evaluator is a stateless, pure function:

```python
# Conceptual AST Evaluator Design (Zero eval/exec - pure tree traversal)
def evaluate_ast_node(node: ASTNode, facts: Dict[str, NormalizedFact]) -> EvaluationResult:
    if node.node_type == "LOGICAL":
        if node.operator == "AND":
            return all(evaluate_ast_node(child, facts).is_true for child in node.children)
        elif node.operator == "OR":
            return any(evaluate_ast_node(child, facts).is_true for child in node.children)
        elif node.operator == "NOT":
            return not evaluate_ast_node(node.children[0], facts).is_true

    elif node.node_type == "COMPARISON":
        fact = facts.get(node.fact_key)
        if not fact or fact.status != "VERIFIED":
            return EvaluationResult(is_true=False, status="MISSING_FACT")
        
        # Execute safe, typed comparison operator
        return compare_values(fact.value, node.operator, resolve_operand(node.operand))

---

## 5. Configurable Resource Limits & Extensibility Governance

### 5.1 Configurable Resource Limits (Non-Normative Defaults)
To prevent excessive computation, stack overflow, or Denial-of-Service style rule expressions, the AST evaluator enforces configurable resource boundaries during static analysis and runtime evaluation:
* **Configurable Limits:** AST maximum nesting depth, AST maximum total node count, maximum set operand elements, and per-rule execution timeouts are deployment-aware and environment-configurable parameters.
* **Non-Normative Illustrative Defaults:** Example configuration values (e.g., maximum AST depth = 10, maximum node count = 100, execution timeout = 500 ms) are provided solely as illustrative defaults for testing/benchmarking. They are **not permanent or normative architectural constants**.
* **Observability & Upper Bounds:** Resource consumption is monitored during rule compilation/validation and batch execution. Safe upper bounds are established via load benchmarking.

### 5.2 Rule Taxonomy & Operator Extensibility
* **Governed Initial Taxonomy:** The initial set of 15 operators represents the baseline controlled rule taxonomy. It does **not** form a permanently closed architectural universe.
* **Governed Extension Process:** New AST operators or rule types may be introduced through formal rule governance lifecycle changes. Adding a new operator requires schema validation, security review, property-based testing, documentation, policy review, and administrative approval.
* **Versioned Compatibility:** All rule AST definitions store their exact rule schema and operator version. Historical evaluations remain interpretable and reproducible against their stored rule version. Arbitrary code execution remains strictly prohibited across all present and future rule types.

```
