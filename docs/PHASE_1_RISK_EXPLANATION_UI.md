# Phase 1 — Risk Explanation UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Risk Explanation UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Anomaly Explanation Scope

This specification defines the UI views explaining advisory risk factors, non-linear risk signal contributions, and anomaly evidence context.

---

## 2. Risk Signal Explanation Panel Topology

```
+-----------------------------------------------------------------------------------+
| RISK SIGNAL EXPLANATION: Signal #SIG-FIN-01 (Sudden Revenue Surge)                 |
| Target Bidder: Gamma Heavy Engg | Advisory Severity: HIGH (0.88)                  |
+-----------------------------------------------------------------------------------+
| 1. ANOMALY DETECTION CRITERIA                                                     |
| Evaluated Rule: `turnover_growth_rate = (FY24_turnover - FY23_turnover) / FY23`    |
| Baseline Threshold: Growth rate > 200% flags anomaly signal                       |
| Observed Values: FY23 = Rs. 10.0 Cr | FY24 = Rs. 50.0 Cr (Growth Rate = +400%)   |
|                                                                                   |
| 2. CONTEXTUAL EVIDENCE & ADVISORY GUIDANCE                                        |
| System Guidance for Officer: "Verify audited balance sheet notes and GST Returns  |
| for FY 2023-24 to confirm genuine business expansion."                            |
| Action Options: [ View FY24 Financial PDF ]  [ Add Officer Investigation Note ]    |
+-----------------------------------------------------------------------------------+
```

---

## 3. Non-Linear Risk Representation

1. **Multi-Factor Weighting Trace:** Explains how individual risk factors contribute to the aggregated non-linear risk profile.
2. **Explicit Non-Disqualification Disclaimer:** Emphasizes that high financial growth rate is a valid business scenario and requires human verification, not automatic penalty.
