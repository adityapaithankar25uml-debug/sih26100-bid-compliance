# Phase 1 — Core User Journeys Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Core User Journeys Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Journey Architecture

This specification defines the 24 primary end-to-end user journeys (Journeys A through X) for authorized platform users, specifying UI entry points, interaction steps, decision gates, audit events, and exception recovery paths.

---

## 2. Core User Journey Specifications (Journeys A – X)

### Journey A: Officer Authentication & Session Initialization
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Officer accesses portal login page $\rightarrow$ Authenticates via SSO / OIDC with Multi-Factor Authentication $\rightarrow$ System verifies RBAC scope $\rightarrow$ Redirected to Procurement Officer Dashboard.
- **Audit Event:** `AUTH_LOGIN_SUCCESS` (User ID, IP, Session Token ID).

### Journey B: Officer Views Assigned Tenders
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Dashboard loads assigned active tenders $\rightarrow$ Filter by priority, closing date, or evaluation stage $\rightarrow$ Select target tender to open Tender Workspace.

### Journey C: Officer Opens Tender Workspace
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Selects Tender ID $\rightarrow$ Workspace loads `TenderVersion` summary, corrigenda history, requirement checklist, and submitted bidder list.

### Journey D: Tender Requirement Review
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Officer reviews requirement tree (Technical, Financial, Commercial, Local Content) $\rightarrow$ Inspects bound deterministic rules and policy versions.

### Journey E: Bid Submission Ingestion & Overview
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Ingestion API triggers async processing $\rightarrow$ UI displays submission metadata, document manifest, and processing status badges (`EXTRACTING`, `READY`).

### Journey F: Document Security & Disarming Review
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Open Document Viewer $\rightarrow$ System displays sanitized disarmed PDF alongside original submission SHA-256 digest hash $\rightarrow$ Verify malware scan clearance.

### Journey G: AI Document Extraction Review
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Inspect extracted fields (e.g., Turnover, Work Order Values) $\rightarrow$ Bounding box highlights source text on PDF $\rightarrow$ Officer confirms or edits field value.
- **Audit Event:** `HUMAN_FIELD_CORRECTION` (Original AI Value, Officer Corrected Value, Page Ref).

### Journey H: Government Registry Verification Review
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Review automated government adapter status (PAN, GSTN, MCA21, Udyam) $\rightarrow$ Inspect verification freshness, source status badge (`LIVE`/`SANDBOX`), and identity match indicators.

### Journey I: Deterministic Compliance Evaluation Review
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Open Compliance Matrix UI $\rightarrow$ Inspect rule evaluation determinations (`VERIFIED`, `UNVERIFIED`, `MISSING_EVIDENCE`) $\rightarrow$ View AST calculation trace.

### Journey J: Backward Evidence Trace Inspection
- **Actor:** `PROCUREMENT_OFFICER` / `AUDITOR`
- **Flow:** Click non-compliant or unverified status badge $\rightarrow$ UI expands evidence trace chain: Rule $\rightarrow$ Fact $\rightarrow$ Government Verification Result / Document Bounding Box.

### Journey K: Advisory Risk Review
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Inspect Risk Dashboard $\rightarrow$ Review advisory risk factor signals (e.g., sudden financial jump, recent incorporation) $\rightarrow$ Note: Risk score is advisory and distinct from compliance rules.

### Journey L: Evidence Conflict Resolution
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** System flags conflicting evidence (e.g., Turnover in Audited Financials vs GST Return) $\rightarrow$ Officer routes item to Human Review Workspace $\rightarrow$ Enters resolution notes and selects authoritative evidence source.

### Journey M: Human Review Workspace Execution
- **Actor:** `PROCUREMENT_OFFICER` / `SENIOR_REVIEWER`
- **Flow:** Access Human Review Queue $\rightarrow$ Inspect review reason (`LOW_CONFIDENCE`, `MISSING_EVIDENCE`, `GOVT_FAILURE`) $\rightarrow$ Record manual resolution.

### Journey N: Officer Qualification Decision Recording
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Officer reviews aggregated compliance summary $\rightarrow$ Selects official decision (`QUALIFIED` / `NOT_QUALIFIED` / `PENDING_REVIEW`) $\rightarrow$ Enters mandatory justification rationale $\rightarrow$ Signs decision submission.
- **Audit Event:** `OFFICER_DECISION_RECORDED` (Tender ID, Bidder ID, Decision, Rationale, Timestamp).

### Journey O: Senior Reviewer Supervisory Approval
- **Actor:** `SENIOR_REVIEWER`
- **Flow:** High-value tender decision queued for four-eyes review $\rightarrow$ Senior Reviewer inspects compliance matrix, risk profile, and officer notes $\rightarrow$ Concurs or requests revision.

### Journey P: Independent Audit Inspection
- **Actor:** `AUDITOR`
- **Flow:** Auditor opens Audit Explorer $\rightarrow$ Filters by Tender ID $\rightarrow$ Inspects SHA-256 hash-chain continuity $\rightarrow$ Traces decision timeline from initial upload to final decision.

### Journey Q: Re-Opening Historical Evidence & Evaluations
- **Actor:** `AUDITOR` / `SENIOR_REVIEWER`
- **Flow:** Select historical evaluation snapshot ID $\rightarrow$ System loads exact immutable state of requirements, rules, facts, and documents at evaluation timestamp.

### Journey R: Handling Incomplete or Missing Evidence
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Requirement displays `MISSING_EVIDENCE` $\rightarrow$ System routes status to `REQUIRES_HUMAN_REVIEW` (Does **NOT** auto-disqualify) $\rightarrow$ Officer requests clarification or issues shortfall notice.

### Journey S: Handling Stale Verification Results
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Government verification result exceeds freshness threshold $\rightarrow$ UI flags status as `STALE` $\rightarrow$ Officer clicks "Re-verify" to trigger fresh adapter query.

### Journey T: Handling Government API Technical Failure
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Government API returns `504 Gateway Timeout` $\rightarrow$ UI displays `MANUAL_FALLBACK_REQUIRED` badge (does **NOT** show bidder failure) $\rightarrow$ Officer executes manual verification workflow.

### Journey U: Handling Low-Confidence AI Extraction
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** AI extraction confidence $< 80\%$ $\rightarrow$ UI highlights field in yellow warning banner $\rightarrow$ Officer manually inspects document page and inputs verified value.

### Journey V: Handling Conflicting Document Evidence
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** System detects discrepancy between document pages $\rightarrow$ Highlights conflicting fields in side-by-side viewer $\rightarrow$ Officer determines authoritative document.

### Journey W: Handling Corrigendum / Tender Version Change
- **Actor:** `PROCUREMENT_OFFICER`
- **Flow:** Corrigendum issued updating tender requirement $\rightarrow$ System creates `TenderVersion v2` $\rightarrow$ UI highlights changed rules and prompts evaluation re-run against new version.

### Journey X: Handling Compliance Drift Monitoring
- **Actor:** `SENIOR_REVIEWER` / `AUDITOR`
- **Flow:** System detects statistical drift in compliance pass rates across tender categories $\rightarrow$ UI displays drift alert $\rightarrow$ Reviewer inspects rule version consistency.
