# Phase 1 — Risk Dashboard Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Risk Dashboard Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Advisory Risk Scope

This specification defines the advisory Risk Dashboard, risk factor breakdown matrix, and non-linear risk signal indicators.

**CRITICAL PRINCIPLE:**
The UI **MUST** maintain strict separation between advisory risk metrics and deterministic compliance evaluations:
> **"Risk scores are advisory anomaly indicators. High risk DOES NOT equal disqualification, and low risk DOES NOT equal qualification."**

---

## 2. Risk Dashboard Layout Topology

```
+-----------------------------------------------------------------------------------+
| ADVISORY RISK DASHBOARD: Tender #CPCL/2026/894 (High-Pressure Valves)             |
+-----------------------------------------------------------------------------------+
| RISK SUMMARY BY BIDDER                                                            |
| Bidder Name         | Overall Risk Level | Key Advisory Signals Detected          |
|---------------------+--------------------+----------------------------------------|
| Alpha Engineering   | LOW (0.18)         | Standard financial progression         |
| Beta Controls Inc   | MEDIUM (0.52)      | Recent incorporation (< 12 months)     |
| Gamma Heavy Engg    | HIGH (0.84)        | Sudden 400% revenue surge in FY24      |
+-----------------------------------------------------------------------------------+
| ANOMALY SIGNAL BREAKDOWN (Bidder: Gamma Heavy Engg)                               |
| Signal ID | Category       | Anomaly Description               | Severity Score |
|-----------+----------------+-----------------------------------+----------------|
| SIG-FIN-01| Financial      | Revenue jumped from 10Cr to 50Cr  | HIGH (0.88)    |
| SIG-EXP-03| Technical Exp  | Similar work order issued by shell| HIGH (0.82)    |
+-----------------------------------------------------------------------------------+
```

---

## 3. Visual Separation Safeguards

1. **Advisory Banner Warning:** Every risk UI panel displays an explicit disclaimer: `"Advisory Risk Indicators assist officer investigation and DO NOT constitute automated compliance disqualification."`
2. **Distinct Color Coding:** Advisory risk levels use amber/orange warning tones (`#D97706`) to distinguish them from deterministic rule compliance badges (`VERIFIED` emerald / `FAILED` red).
