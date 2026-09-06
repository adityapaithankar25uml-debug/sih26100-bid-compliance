# Phase 4 — Policy Versioning Implementation

## 1. Policy Versioning Principles
Evaluation rules and threshold parameters are bound to immutable, versioned `PolicyVersion` records. Overwriting historical policy rules is strictly prohibited.

## 2. Seeded Policy Configuration
- `policy_code`: `POL_GEM_COMPLIANCE_2026`
- `version`: `1.0`
- `title`: GeM General Financial & Statutory Procurement Policy 2026
- `policy_hash`: SHA-256 hash of policy rules configuration
- `rules_config_json`:
  ```json
  {
    "make_in_india_class1_min_percentage": 50.0
  }
  ```
