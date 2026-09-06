# Phase 5 — Security & RBAC Architecture

## 1. Approved Security Classification Taxonomy
- `PUBLIC`
- `INTERNAL`
- `CONFIDENTIAL`
- `RESTRICTED`
- `PII`

No unapproved security classifications exist in Phase 5.

## 2. Role-Based Access Control (RBAC) Enforcements
- **Procurement Officer / Senior Reviewer / Compliance Officer / Admin**:
  - Full access to human review queue, task assignment, task resolution, officer qualification decisions, and manual overrides.
- **Auditor**:
  - Read-only access to evidence ledger, evaluation snapshots, risk profiles, officer decisions, and tamper-evident audit hash chain.
- **Bidder (`Role.BIDDER`)**:
  - Strictly forbidden from accessing officer decisions, manual overrides, risk calculations, or review task resolution (`403 Forbidden`).

## 3. Data Masking & PII Protection
Protected fields (e.g. PAN, GSTIN personal identifiers) are masked in responses according to Phase 1/8 privacy policies (e.g. `ABCDE****F`).
