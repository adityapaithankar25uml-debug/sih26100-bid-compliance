# Phase 1 — Evidence Explorer Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Evidence Explorer Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Evidence Explorer Scope

This specification defines the Evidence Explorer UI, evidence package inspector, SHA-256 integrity verifier, and document provenance tree views.

---

## 2. Evidence Explorer Interface Topology

```
+-----------------------------------------------------------------------------------+
| EVIDENCE EXPLORER: Tender #CPCL/2026/894 | Bidder #BID-409 (Alpha Engineering)     |
+-----------------------------------------------------------------------------------+
| EVIDENCE RECORD TREE                                                              |
| [v] Evidence Package #EV-8912 (Created: 2026-08-25 15:30:10 IST)                  |
|     ├── [Doc] Financial_Statements.pdf (SHA-256: 8a9f2...c01)                     |
|     │    └── [Fact] FY24 Turnover = Rs. 68.0 Cr (Bounding Box: p.4 rect [120,340])|
|     ├── [Govt] GSTN Registry API Match (Result ID: #GST-4091, Status: LIVE)     |
|     └── [Rule] Evaluation #EVAL-901 (AST Result: VERIFIED)                       |
+-----------------------------------------------------------------------------------+
| INTEGRITY & PROVENANCE METADATA                                                   |
| - Primary Payload Hash: `8a9f23b7e41109a28c1109bc4891276a109a89f...`              |
| - Storage Location: `sih26100-evidence-ledger/2026/CPCL_894/BID_409/EV_8912.json`  |
| - Legal Hold Status: ACTIVE (Legal hold override enabled)                         |
+-----------------------------------------------------------------------------------+
```

---

## 3. Interaction Standards

1. **One-Click Hash Verification:** Officers or auditors can click "Verify SHA-256 Digest" to trigger a backend recalculation check verifying evidence payload integrity.
2. **Exportable Evidence Snapshot:** Export complete evidence packages as tamper-evident JSON bundles.
