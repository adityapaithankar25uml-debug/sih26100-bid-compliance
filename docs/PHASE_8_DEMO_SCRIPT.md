# Phase 8 — SIH Judge Demonstration Script (7–10 Minutes)

## Overview & Demo Goal

This script provides a step-by-step presentation flow for demonstrating the **SIH26100 AI-Powered Integrated Bid Compliance Verification Platform** to SIH judges in 7 to 10 minutes.

- **Demo URL:** `http://localhost:3000`
- **Backend API:** `http://localhost:8000/api/v1`
- **Seeded Demo Identity:** Procurement Officer (`officer@cpcl.gov.in`)
- **Seeded Tender:** `TENDER-CPCL-2026-001` (Industrial Pumps & Valves Supply Procurement)
- **Seeded Bid Submission:** `SUB-2026-CPCL-001` (Apex Engineering Solutions Pvt Ltd)

> **Mandatory Prototype Disclosure for Presenters:**  
> *"For this SIH prototype, government registry responses are simulated through normalized integration adapters. The architecture is designed for authorized production connections, but no live government credentials or live government verification access are being claimed in this prototype."*

---

## Detailed Step-by-Step Walkthrough

### Step 0: Problem Introduction (00:00 – 00:45)
- **What to Say:**
  > "Honorable Judges, public procurement verification on platforms like GeM currently requires procurement officers to manually inspect hundreds of pages of technical and financial documents for every bid. This manual process causes significant evaluation delays, increases risk of missed compliance flaws, and creates auditing bottlenecks.
  > Our solution, **SIH26100**, is an AI-Powered Integrated Bid Compliance Verification Platform built specifically for CPCL and the Ministry of Petroleum & Natural Gas to automate verification while preserving strict legal accountability and audit integrity."
- **Key Technical Principle:** Manual procurement complexity solved via smart automation.

---

### Step 1: Solution Overview & Architecture Principle (00:45 – 01:30)
- **What to Say:**
  > "Our system operates on a fundamental architectural principle:
  > **AI extraction is advisory. Deterministic compliance rules evaluate structured facts. Evidence and provenance support the evaluation. The authorized human officer retains final procurement decision authority.**
  > Let me also state clearly: for this SIH prototype, government registry responses are simulated through normalized integration adapters. The architecture is designed for authorized production connections, but no live government credentials or live government verification access are being claimed in this prototype. Let's walk through the live system."
- **Key Technical Principle:** AI is advisory; deterministic rules evaluate; human officers retain final decision authority.

---

### Step 2: Officer Authentication & Executive Dashboard (01:30 – 02:15)
- **What to Click:**
  1. Navigate to `http://localhost:3000/login`.
  2. Click **"Authenticate as ProcurementOfficer (Rajesh Kumar)"**.
  3. Land on `/dashboard`.
- **What Judge Sees:**
  - Executive Command Center with metrics: Active Tenders (`1`), Bid Submissions (`1`), Pending Reviews (`1`), Audit Chain Verification Status (`Intact`).
  - Top System Axiom Banner highlighting the 7-stage pipeline.
  - Authorized officer profile badge: `Rajesh Kumar (Procurement Officer)`.
- **What to Say:**
  > "We log in using backend-authoritative RBAC as Procurement Officer Rajesh Kumar. The Command Center provides metrics across active tenders, submitted bids, pending human review queues, and instant SHA-256 audit chain integrity status."

---

### Step 3: Tender Catalog & Requirement Inspection (02:15 – 03:00)
- **What to Click:**
  1. Click **"Tenders"** in top navbar or click **"TENDER-CPCL-2026-001"**.
- **What Judge Sees:**
  - Tender detail page (`/tenders/TEN_01`) showing tender title, CPCL organization, active status, and specification version history (Version 1).
  - Categorized requirement specs: Financial Turnover (₹5.0 Cr), Local Content (50% MII), GST, MSME/Udyam, EPF/ESIC, Debarment check.
- **What to Say:**
  > "Here in the Tender Specification Workspace, procurement requirements are cataloged with strict versioning. Corrigendums or spec revisions create new version baselines to ensure bids are evaluated against the exact policy active at submission time."

---

### Step 4: Bidder 360 & Document Intelligence (03:00 – 03:45)
- **What to Click:**
  1. Navigate to `/bids/SUB_01`.
  2. Click tab **"Documents & AI Extraction"**.
- **What Judge Sees:**
  - Bidder identity summary: Apex Engineering Solutions Pvt Ltd (GSTIN: `33AAACA1234A1Z5`, Udyam: `UDYAM-TN-01-0012345`).
  - Document extraction table showing uploaded PDF certificates, extraction status, confidence scores (e.g. 98.5%), and bounding box text snippet citations.
- **What to Say:**
  > "In the Bid Workspace, our Document Intelligence Pipeline processes uploaded bid PDFs. It extracts key fields like turnover numbers, registration IDs, and Make-in-India declarations into structured facts. Every extracted value retains confidence scores and text snippet provenance."

---

### Step 5: Government Verification Center & MOCK Disclosures (03:45 – 04:30)
- **What to Click:**
  1. Click **"Govt Registries"** in top navbar (`/verification`).
- **What Judge Sees:**
  - Grid of 12 statutory government registries (GST, Udyam, PAN, MCA, EPFO, ESIC, Startup India, NSIC, OEM Auth, DigiLocker, Central Debarment List, GeM Profile).
  - Prominent **"INTEGRATION MODE: MOCK / DEMO"** badges on every registry card.
  - Notice explaining transport failure safety: API timeouts generate human review tasks.
- **What to Say:**
  > "Our platform features a normalized Government Adapter Layer supporting 12 statutory registries. As highlighted by these MOCK badges, government responses are simulated for this prototype. Furthermore, technical transport failures never reject a bidder automatically—they generate human review tasks."

---

### Step 6: Evidence Explorer & 9 Quality Dimensions (04:30 – 05:15)
- **What to Click:**
  1. Click **"Evidence Explorer"** in top navbar (`/evidence`).
- **What Judge Sees:**
  - Summary card highlighting **"9 INDEPENDENT EVIDENCE QUALITY DIMENSIONS"**:
    1. `source_authority`, 2. `source_freshness`, 3. `completeness`, 4. `integrity_hash_validity`, 5. `identity_linkage`, 6. `document_authenticity`, 7. `temporal_applicability`, 8. `extraction_provenance`, 9. `consistency`.
  - Detailed evidence lineage table linking facts to source documents.
- **What to Say:**
  > "Our Evidence Engine evaluates 9 independent quality dimensions—including source authority, freshness, hash integrity, and identity linkage—ensuring that qualification evaluations are backed by verifiable evidence."

---

### Step 7: Deterministic Compliance Matrix Evaluation (05:15 – 06:00)
- **What to Click:**
  1. Return to `/bids/SUB_01` and click tab **"Compliance Matrix"**.
- **What Judge Sees:**
  - Deterministic evaluation table showing requirement codes, rule descriptions, evaluated status (`PASS`, `FAIL`, `NEEDS_REVIEW`), and calculation traces.
  - Clear separation between automated rule checks and officer review items.
- **What to Say:**
  > "This is our Deterministic Compliance Matrix. Every tender requirement is evaluated using boolean code against structured facts. For example, comparing the verified turnover of ₹8.5 Cr against the required ₹5.0 Cr yields a deterministic PASS result."

---

### Step 8: Advisory Risk Engine (06:00 – 06:45)
- **What to Click:**
  1. Click **"Risk Engine"** in top navbar (`/risk`).
- **What Judge Sees:**
  - Advisory Risk Engine panel displaying overall risk level (`LOW`), risk score (`15/100`), and active risk signals.
  - Prominent banner: **"RISK ENGINE ADVISORY CONTROL RULE: Risk scores are strictly advisory for prioritization and cannot automatically qualify or disqualify a bidder."**
- **What to Say:**
  > "The Advisory Risk Engine aggregates anomaly signals across identity, financial data, and debarment registries to calculate a risk score. Risk scores are strictly advisory to help officers prioritize high-risk bids—they can never automatically disqualify a bidder."

---

### Step 9: Human Review Queue & Officer Decision (06:45 – 07:30)
- **What to Click:**
  1. Click **"Human Review"** in top navbar (`/human-review`).
  2. View pending task `REV-001` (Make in India Local Content Declaration Verification).
  3. Return to `/bids/SUB_01` and click tab **"Decision & Override"**.
- **What Judge Sees:**
  - Human review task queue with priority levels, review reasons, and assigned officer.
  - Formal Officer Decision form offering options: `QUALIFIED`, `DISQUALIFIED`, `REQUIRES_CLARIFICATION`, `EVIDENCE_REQUESTED`.
- **What to Say:**
  > "When an item requires human judgment, it enters the Human Review Queue. The Procurement Officer inspects the evidence and records a formal decision—such as QUALIFIED or REQUIRES_CLARIFICATION—with written rationale."

---

### Step 10: Non-Destructive Manual Override & Four-Eyes Policy (07:30 – 08:15)
- **What to Click:**
  1. On `/bids/SUB_01` under **"Decision & Override"**, view the **"Four-Eyes Manual Rule Overrides"** section.
- **What Judge Sees:**
  - Manual override table showing previous status, overridden status, override reason code, and four-eyes review status (`PENDING_FOUR_EYES` or `APPROVED`).
  - Notice explaining point-in-time snapshot preservation.
- **What to Say:**
  > "If an officer manually overrides a rule result, our system creates a point-in-time Evaluation Snapshot before saving the override. The original rule result is preserved untouched. If the override triggers our Four-Eyes Policy threshold, a second senior reviewer must approve it before final qualification."

---

### Step 11: Tamper-Evident SHA-256 Audit Hash Chain (08:15 – 08:45)
- **What to Click:**
  1. Click **"Audit Log"** in top navbar (`/audit`).
  2. Click button **"Verify Audit Chain Integrity"**.
- **What Judge Sees:**
  - Status banner displays: **"Audit Hash Chain Verified Intact — Verified Blocks: 110 / 110"**.
  - Canonical event table listing timestamped actor, action, resource ID, correlation ID, and SHA-256 payload hashes.
- **What to Say:**
  > "Every action taken on our platform is logged as a canonical JSON event into a SHA-256 linked hash chain. By clicking 'Verify Audit Chain Integrity', the system re-calculates hashes block-by-block to verify that no audit event has been modified or tampered with."

---

### Step 12: Impact & Closing (08:45 – 09:30)
- **What to Say:**
  > "In summary, the platform is designed to reduce manual verification effort through document extraction, verification orchestration, deterministic rule evaluation, evidence compilation, and review prioritization. Actual production reduction should be measured during an authorized pilot.
  > Thank you, and we welcome your questions!"

---

## Quick Reference Summary Table for Presenters

| Time | Demo Stage | Key Screen / Action | Key Point to Highlight |
|---|---|---|---|
| **00:00** | Intro | Title / Problem Statement | Manual procurement bottleneck at GeM / CPCL |
| **00:45** | Axiom & Disclosures | System Principles | AI extraction advisory; rules evaluate; MOCK disclosure |
| **01:30** | Dashboard | `/dashboard` | Executive command center & role-aware RBAC |
| **02:15** | Tenders | `/tenders/TEN_01` | Policy versioning & specification baseline |
| **03:00** | Bidder 360 | `/bids/SUB_01` (Docs tab) | AI extractions with confidence & provenance |
| **03:45** | Registries | `/verification` | 12 statutory sources & explicit MOCK disclosures |
| **04:30** | Evidence | `/evidence` | 9 independent evidence quality dimensions |
| **05:15** | Compliance | `/bids/SUB_01` (Matrix tab) | Deterministic boolean rule matrix evaluation |
| **06:00** | Risk Engine | `/risk` | Advisory risk score (cannot auto-disqualify) |
| **06:45** | Human Review| `/human-review` | Officer review queue & formal decision authority |
| **07:30** | Overrides | `/bids/SUB_01` (Decision tab)| Non-destructive overrides & four-eyes policy |
| **08:15** | Audit Chain | `/audit` (Verify button) | Tamper-Evident SHA-256 Audit Hash Chain verification |
| **08:45** | Conclusion | Summary / Q&A | Pilot measurement objective & Q&A readiness |
