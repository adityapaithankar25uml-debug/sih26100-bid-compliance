# Phase 1 — Information Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Information Architecture Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Information Hierarchy

This specification defines the information architecture (IA), page tree hierarchy, entity-to-screen mapping, and data depth model for the SIH26100 platform.

The IA is structured around a **Tender-Centric and Evidence-Centric Depth Model**, allowing procurement officers to drill down seamlessly from high-level portfolio metrics to individual document bounding boxes and SHA-256 evidence digests.

---

## 2. Platform Information Hierarchy Tree

```
Platform Root (Authenticated Shell)
├── Dashboard Tier (Level 1)
│   ├── Procurement Officer Dashboard
│   ├── Senior Reviewer Supervisory Dashboard
│   ├── Auditor System Lineage Explorer
│   └── System Admin Configuration Workbench
│
├── Tender Portfolio Tier (Level 2)
│   ├── Active Tenders List
│   └── Tender Workspace (`/tenders/{tender_id}`)
│       ├── Overview & Corrigenda History
│       ├── Requirements & Policy Matrix
│       ├── Bidders & Submissions List
│       └── Aggregated Qualification Matrix
│
├── Bid & Document Workspace Tier (Level 3)
│   ├── Bidder Submission Workspace (`/bids/{bid_id}`)
│   │   ├── Submission Summary & Metadata
│   │   ├── Document Reviewer & Viewer (`/documents/{doc_id}`)
│   │   ├── AI Extractions & Bounding Box Inspector
│   │   └── Government Verifications Workbench
│   └── Compliance Evaluation Matrix (`/evaluations/{eval_id}`)
│       ├── Requirement-by-Requirement Evidence Trace
│       ├── Fact Normalization & Rule Calculation Inspector
│       └── Risk Factor Breakdown & Advisory Signals
│
└── Action & Governance Workspace Tier (Level 4)
    ├── Human Review Queue (`/reviews/pending`)
    ├── Officer Decision Workspace (`/decisions/create`)
    ├── Conflict & Exception Resolution Workspace
    └── Audit Lineage Explorer (`/audit/ledger`)
```

---

## 3. Entity-to-Screen IA Mapping

| Domain Entity (Task 2 Baseline) | Primary UI Screen / View | Primary Actions Available |
|---|---|---|
| `Tender` / `TenderVersion` | Tender Workspace Overview | View tender requirements, select active version, track amendments |
| `TenderRequirement` | Tender Requirement UI | Inspect category, rule binding, evaluation criteria, required documents |
| `BidSubmission` | Bidder Workspace | Review submission status, inspect uploaded documents, trigger verification |
| `SourceDocument` | Document Viewer UI | View original PDF, view sanitized derivative, inspect SHA-256 hash |
| `DocumentExtraction` | Document Extraction UI | Review AI extracted fields, inspect bounding box, accept/correct field |
| `GovernmentVerificationResult` | Government Verification UI | View source status (`LIVE`/`SANDBOX`), freshness timestamp, identity match |
| `ComplianceEvaluation` | Compliance Matrix UI | Inspect rule AST determination, review calculation trace, inspect facts |
| `QualificationOutcome` | Decision Workspace | Review aggregated qualification status, record final officer decision |
| `RiskAssessmentProfile` | Risk Dashboard UI | Review advisory risk factors, inspect anomaly signals, view risk matrix |
| `OfficerDecision` | Decision Workspace | Record official decision (`QUALIFIED`/`NOT_QUALIFIED`), add rationale |
| `AuditEvent` | Audit Explorer UI | Inspect SHA-256 hash-chain block, verify timeline, export audit record |
