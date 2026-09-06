# Phase 7 — SIH Flagship Demonstration Workflow & Presentation Guide

## 1. Executive Summary & SIH Storytelling Framework

The SIH26100 platform demonstrates how AI and deterministic verification automate bid compliance for GeM procurement (Ministry of Petroleum & Natural Gas / CPCL).

### Core Narrative Principle
> "AI extracts context, but official government sources verify facts, deterministic rules calculate compliance, evidence proves truth, and authorized human procurement officers make final decisions."

---

## 2. Step-by-Step Demonstration Walkthrough Script

### Step 1: Procurement Officer Authentication
- Navigate to `http://localhost:3000/login`.
- Highlight **MANDATORY RBAC CONTROL NOTICE**: Roles are authoritative and derived from authenticated backend identity.
- Select `Authenticate as ProcurementOfficer` (Officer identity: Rajesh Kumar).

### Step 2: Command Center Dashboard
- Navigate to `http://localhost:3000/dashboard`.
- Demonstrate live metrics: Active Tenders, Submissions, Pending Officer Tasks, Audit Chain Status.
- Highlight system axiom banner: `AI INTERPRETS → AUTHORIZED SOURCES VERIFY → RULES EVALUATE → EVIDENCE PROVES → HUMAN APPROVES`.

### Step 3: Tender Catalog & Requirement Extraction
- Navigate to `http://localhost:3000/tenders/TEN_01`.
- Display seeded tender `TEN_01`: *Supply & Installation of High-Pressure Gas Valves & Automation Control Systems*.
- Show cataloged requirements (Version v1), highlighting mandatory vs optional clauses.

### Step 4: Bidder Workspace & Document Extraction
- Navigate to `http://localhost:3000/bids/SUB_01`.
- Display Bidder `ABC Engineering Pvt Ltd` (Submission `SUB_01`).
- Switch to **Source Documents** tab to view raw uploaded PDF/DOCX files, extraction status, and normalized structured facts.

### Step 5: Government Verification Center (MOCK/DEMO Badges)
- Navigate to `http://localhost:3000/verification`.
- Display 12 integrated government registries (`GSTIN`, `Udyam`, `PAN`, `MCA`, `EPFO`, `ESIC`, `Startup India`, `NSIC`, `OEM Auth`, `Debarment List`, `GeM Profile`, `DigiLocker`).
- Point out prominent **`INTEGRATION MODE: MOCK / DEMO`** badges. Emphasize that no live government endpoints are fake-claimed.

### Step 6: Evidence & Provenance Explorer
- Navigate to `http://localhost:3000/evidence`.
- Showcase the **9 Independent Evidence Quality Dimensions**:
  1. `source_authority`
  2. `source_freshness`
  3. `completeness`
  4. `integrity_hash_validity`
  5. `identity_linkage`
  6. `document_authenticity`
  7. `temporal_applicability`
  8. `extraction_provenance`
  9. `consistency`
- View lineage graph linking raw documents -> extracted facts -> evidence records -> compliance evaluation.

### Step 7: Deterministic Compliance Matrix Evaluation
- Return to `/bids/SUB_01` -> **Compliance Matrix** tab.
- Demonstrate rule-by-rule evaluation results (`PASS`, `FAIL`, `REVIEW_REQUIRED`). Explain that rules are fully deterministic and cannot be altered by AI.

### Step 8: Advisory Risk Assessment Engine
- Navigate to `/risk`.
- Display advisory risk signals and factor breakdown. Explain that risk is strictly advisory and NEVER automatically qualifies or disqualifies a bidder.

### Step 9: Human Review & Discrepancy Resolution
- Navigate to `/human-review`.
- Show pending officer review task.
- Resolve task with rationale. Demonstrate how discrepancy reconciliation routes back into evidence record.

### Step 10: Officer Decision & Manual Override (Four-Eyes Approval)
- On `/bids/SUB_01` -> **Officer Decisions** & **Manual Overrides** tabs.
- Record final officer qualification decision (`QUALIFIED` / `DISQUALIFIED`).
- Create manual override request for rule exception with mandatory justification.
- Show that overrides exceeding policy thresholds require **Four-Eyes Approval** by Senior Reviewer.

### Step 11: Tamper-Evident SHA-256 Audit Hash Chain Explorer
- Navigate to `/audit`.
- Click **Verify Audit Chain Integrity**.
- Watch live verification of cryptographic SHA-256 block hashes across the entire event log chain.
- Confirm zero tamper detections (`Audit Chain Valid`).

---

## 3. Demonstration Resilience & Disclosure Invariants

1. **No Fake Production Claims**: All government source integrations are clearly labeled `MOCK / DEMO`.
2. **Deterministic Seed Data**: Seeded entities `TEN_01` and `SUB_01` ensure 100% repeatable demo execution without network dependencies.
3. **Transparent Fallback Support**: Built-in mock fallbacks ensure UI resilience during live judge evaluations.
