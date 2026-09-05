# Phase 1 API Authorization Matrix Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-015  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines fine-grained Role-Based Access Control (RBAC) permission matrices, separation of duties, and authorization constraints. No FastAPI security middleware, JWT validation code, or backend scripts are created.

---

## 1. System Role Definitions & Scope

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FIVE SYSTEM RBAC ROLES                                │
├───────────────────────┬─────────────────────────────────────────────────────┤
│ 1. SUPER_ADMIN        │ Global platform administration, adapter mode toggles,│
│                       │ RBAC role assignments, & system health monitoring   │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 2. PROCUREMENT_ADMIN  │ Departmental tender setup, requirement parameterization,│
│                       │ & procurement officer team assignments               │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 3. PROCUREMENT_OFFICER│ Tender evaluation workbench access, document OCR,   │
│                       │ Govt API verification, manual override, & decision  │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 4. AUDITOR            │ Read-only vigilance access to evaluations, evidence │
│                       │ chains, officer decision rationales, & audit logs   │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 5. VIEWER             │ Read-only access to published tender notices & basic │
│                       │ summary statistics (Zero access to bidder evaluation)│
└───────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 2. Resource Action Authorization Matrix

Legend:  
- 🟢 **`ALLOW`**: Full access to perform action.  
- 🔴 **`DENY`**: Explicitly forbidden by security policy.  
- 🟡 `CONDITIONAL`: Permitted only if user belongs to the assigned tender department.

| Resource Endpoint Group | Action / Operation | SUPER_ADMIN | PROCUREMENT_ADMIN | PROCUREMENT_OFFICER | AUDITOR | VIEWER |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Auth & Sessions** | Login, Refresh, Logout | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW |
| **User Management** | Create / Update Users | 🟢 ALLOW | 🟡 CONDITIONAL | 🔴 DENY | 🔴 DENY | 🔴 DENY |
| **Tender Setup** | Import Tender / Create NIT | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🔴 DENY | 🔴 DENY |
| **Requirements** | Confirm AI Requirements | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🔴 DENY | 🔴 DENY |
| **Document Management** | Upload / Read Bidder PDF | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🔴 DENY |
| **Document Intelligence**| Trigger OCR / View Tokens| 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🔴 DENY |
| **Govt Verification** | Trigger Verification API| 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🔴 DENY | 🔴 DENY |
| **Evidence Ledger** | Read Evidence Chain | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🔴 DENY |
| **Rule Engine** | Run Evaluation Engine | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🔴 DENY | 🔴 DENY |
| **Risk Profile** | View Risk Scores & Signals| 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🟢 ALLOW | 🔴 DENY |
| **Officer Decision** | Record Qualification Decision| 🔴 DENY | 🔴 DENY | 🟢 ALLOW | 🔴 DENY | 🔴 DENY |
| **Manual Override** | Perform Status Override | 🔴 DENY | 🔴 DENY | 🟢 ALLOW | 🔴 DENY | 🔴 DENY |
| **Audit Logs** | Query Audit Events & Hashes| 🟢 ALLOW | 🔴 DENY | 🔴 DENY | 🟢 ALLOW | 🔴 DENY |
| **System Configuration** | Toggle Adapter Modes | 🟢 ALLOW | 🔴 DENY | 🔴 DENY | 🔴 DENY | 🔴 DENY |

---

## 3. Separation of Duties & Explicit System Prohibitions

1. **`VIEWER` Prohibitions:** `VIEWER` users MUST NOT record officer decisions, perform manual overrides, view bidder PII, or trigger government API lookups.
2. **`AUDITOR` Prohibitions:** `AUDITOR` users maintain read-only vigilance access. They MUST NOT mutate tenders, evaluate compliance rules, override decisions, or delete audit events.
3. **`SUPER_ADMIN` Prohibitions:** `SUPER_ADMIN` users manage platform infrastructure. To preserve separation of duties, they MUST NOT record final procurement qualification decisions or perform manual overrides on active tenders.
4. **`AI sub-system` Prohibitions:** AI components MUST NOT execute officer decisions, alter compliance rules, or call government APIs directly outside the adapter layer.
