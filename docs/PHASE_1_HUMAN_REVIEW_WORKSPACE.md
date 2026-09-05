# Phase 1 — Human Review Workspace Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Human Review Workspace Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Human Review Scope

This specification defines the dedicated Human Review Workspace for handling evaluation exceptions, low-confidence extractions, missing evidence, and manual overrides.

---

## 2. Human Review Task Queue Topology

```
+-----------------------------------------------------------------------------------+
| HUMAN REVIEW WORKSPACE: Pending Evaluation Exceptions Queue                       |
+-----------------------------------------------------------------------------------+
| Task ID  | Tender ID    | Bidder Name        | Exception Reason      | Action     |
|----------+--------------+--------------------+-----------------------+------------|
| REV-101  | CPCL/2026/01 | Beta Controls Inc  | Missing GST Cert      | [Review]   |
| REV-102  | CPCL/2026/01 | Gamma Heavy Engg   | Low AI UDIN (74%)     | [Review]   |
| REV-103  | CPCL/2026/04 | Delta Systems Ltd  | Govt Timeout (MCA21)  | [Review]   |
+-----------------------------------------------------------------------------------+
| TASK RESOLUTION PANEL (Task #REV-101 Selected)                                    |
| Issue: Bidder omitted GST Certificate in main upload; submitted MSE Udyam Cert.   |
| Officer Resolution Action:                                                        |
| (o) Issue Shortfall Notice to Bidder (Request GST Document via GeM Portal)        |
| ( ) Mark Requirement as Non-Compliant                                             |
| ( ) Grant Special Policy Exemption (Requires Senior Reviewer Concurrence)         |
| Officer Justification Notes: [ GST Certificate missing; 48hr shortfall notice sent] |
| [ Record Resolution ]  [ Escalate to Senior Reviewer ]                            |
+-----------------------------------------------------------------------------------+
```

---

## 3. Non-Destructive Override Governance

1. **Immutable Snapshot Preservation:** Manual overrides create linked `ManualOverride` and `OfficerDecision` records. They **DO NOT** modify historical evaluation snapshot records (`ComplianceEvaluation`).
2. **Four-Eyes Policy Trigger:** Policy-sensitive overrides or high-value tender exceptions automatically enforce a `SENIOR_REVIEWER` concurrence checkpoint before finalization.
