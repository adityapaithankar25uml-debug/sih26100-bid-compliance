# Phase 5 — Non-Linear Advisory Risk Engine Architecture

## 1. Core Principle
**RISK IS NOT QUALIFICATION OR DISQUALIFICATION.**
Risk scoring exists solely to assist procurement officers in prioritizing human review attention. A high risk score NEVER automatically disqualifies or qualifies a bidder.

## 2. 12 Controlled Risk Categories
1. `IDENTITY`: Name/PAN/GSTIN mismatch or partial match signals.
2. `DOCUMENT`: OCR extraction confidence, document formatting anomalies.
3. `GOVERNMENT_VERIFICATION`: Adapter timeouts, conflicting government data.
4. `COMPLIANCE`: Compliance rule failures or missing mandatory evidence.
5. `EVIDENCE`: Quality deficiencies, missing source documents.
6. `FRESHNESS`: Stale government verification records.
7. `FINANCIAL`: Financial turnover discrepancies or unusual ratios.
8. `POLICY`: Policy configuration changes or exceptions.
9. `TENDER_COVERAGE`: Mandatory requirement coverage gaps.
10. `OVERRIDE`: History of manual overrides on submission.
11. `WORKFLOW`: Unresolved human review items.
12. `INTEGRITY`: Document hash mismatch or security scan flags.

## 3. Versioned Risk Model Configuration (`RiskModelConfig`)
Risk weights, thresholds, and interaction rules are defined in a configurable, versioned risk model (`DEFAULT_RISK_MODEL_CONFIG`):
```
Demonstration Configuration Values (Version 1.0.0-DEMO):
  Severity Weights:
    CRITICAL : +30.0
    HIGH     : +15.0
    MEDIUM   : +8.0
    LOW      : +3.0

  Interaction Multipliers:
    ≥ 2 CRITICAL signals         : 1.30x score multiplier
    1 CRITICAL + ≥ 2 HIGH signals: 1.15x score multiplier
    ≥ 3 HIGH signals             : 1.10x score multiplier

  Risk Level Thresholds:
    80.1 - 100.0: CRITICAL
    50.1 - 80.0 : HIGH
    20.1 - 50.0 : MEDIUM
    0.0  - 20.0 : LOW
```
*Note: Severity weights and multipliers are configurable demonstration values, not statutory procurement policy. Changing the risk configuration produces a different versioned risk profile.*

## 4. Policy-Controlled Review Task Routing
Risk assessment remains advisory. Review queue task routing is governed by a policy-controlled router (`RoutingPolicy`):
```
Risk Signals -> Risk Assessment -> Policy-Controlled Review Routing -> Human Review
```
A configured routing policy determines whether a review task should be created based on configured rules (e.g., government data conflict, missing mandatory evidence, or risk signal threshold), separate from qualification/disqualification.

## 5. Determinism & Explainability
Every risk assessment is reproducible for a given evaluation snapshot and versioned risk configuration. Each risk score breaks down into explicit traceable `RiskFactorSignal` items.
