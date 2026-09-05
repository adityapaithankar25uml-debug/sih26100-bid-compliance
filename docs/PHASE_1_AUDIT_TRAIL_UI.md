# Phase 1 — Audit Trail UI Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Audit Trail UI Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Audit Explorer Scope

This specification defines the Audit Trail Explorer UI, SHA-256 hash-chain block inspector, timeline filter controls, and immutable event lineage viewer.

---

## 2. Audit Trail Explorer Interface Topology

```
+-----------------------------------------------------------------------------------+
| AUDIT TRAIL EXPLORER: Tender #CPCL/2026/894 (Hash Chain Status: VERIFIED INTACT)  |
+-----------------------------------------------------------------------------------+
| Timestamp        | Actor / Role          | Action Type        | Resource ID | SHA-256 Hash Link |
|------------------+-----------------------+--------------------+-------------+-------------------|
| 2026-09-06 14:30 | P. Officer (Officer)  | DECISION_RECORDED  | BID-409     | `block_8912` [V]  |
| 2026-09-06 14:15 | S. Reviewer (Reviewer)| OVERRIDE_APPROVED  | OVERRIDE-12 | `block_8911` [V]  |
| 2026-09-06 10:02 | System Worker (Service)| GOVT_VERIF_LIVE   | RESULT-401  | `block_8910` [V]  |
+-----------------------------------------------------------------------------------+
| SELECTED AUDIT BLOCK INSPECTOR (Block #8912)                                      |
| - Event Type: `OFFICER_DECISION_RECORDED`                                         |
| - Previous Block Hash ($H_{n-1}$): `7a912c0198...`                                |
| - Current Block Payload Digest ($H_n$): `e3901b88c4...`                           |
| - Verification Status: Tamper-evident SHA-256 hash link valid.                   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Tamper-Evident Representation

1. **Hash Chain Linkage Indicator:** Renders a green `[V]` badge confirming continuous SHA-256 block hash lineage ($H_n = \text{SHA-256}(H_{n-1} \parallel \text{Payload})$).
2. **No Digital Signature Claims:** The UI accurately describes the audit ledger as a tamper-evident SHA-256 hash chain and does **NOT** falsely claim PKI or digital signatures.
