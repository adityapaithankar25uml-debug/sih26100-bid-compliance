# Phase 6 — Frontend Architecture & Component Architecture

## 1. System Overview
Phase 6 delivers a GeM-inspired, enterprise-grade Government Procurement Command Center built on Next.js 14 (App Router), TypeScript, TailwindCSS, and Lucide Icons.

The architecture enforces the fundamental system axiom:
> **"AI interprets. Authorized sources verify. Rules evaluate. Evidence proves. Risk prioritizes. Human decides. Audit remembers."**

---

## 2. Security & RBAC Scoping
- **Authoritative Identity:** User identity and authorization scopes are derived exclusively from cryptographically signed backend JWT tokens returned by `/api/v1/auth/login`.
- **No Client Privilege Escalation:** Arbitrary frontend role-switcher dropdowns are forbidden. Demo login is managed via a **Demo Account Selector** that authenticates predefined seeded demo accounts against the backend API.
- **Role-Aware UI:** Navigation items, action buttons (such as issuing officer decisions or proposing overrides), and audit triggers adapt dynamically to the authenticated role (`ProcurementOfficer`, `SeniorReviewer`, `ComplianceOfficer`, `SystemAdmin`, `Auditor`, `Bidder`, `ServiceWorker`).

---

## 3. Top-Level Route Map vs Workspace Tab Map

### Top-Level Route Map (12 Routes)
1. `/login`: Demo Account Auth Portal (Backend-authenticated role selector)
2. `/dashboard`: Procurement Workload Command Center
3. `/tenders`: Tender Catalog & Search
4. `/tenders/[id]`: Tender Workspace & Version Amendment History
5. `/bids`: Bid Submissions Registry
6. `/verification`: Government Verification Center (Adapter Registry & Mode status)
7. `/human-review`: Procurement Officer Human Review Task Queue
8. `/risk`: Advisory Risk Engine Panel
9. `/evidence`: Evidence & Provenance Explorer (9 Quality Dimensions)
10. `/documents/upload`: Document Ingestion Interface (Quarantine malware scan & metadata)
11. `/documents/[id]`: Document Detail & Extracted Bounding Box Provenance
12. `/audit`: Tamper-Evident SHA-256 Audit Hash Chain Explorer

### Bid Workspace Tab Map (`/bids/[id]`)
1. **Overview:** Bidder 360, PAN/GSTIN/Udyam statutory identity linkage.
2. **Compliance Matrix:** Flagship evaluation table with PASS, FAIL, MISSING_EVIDENCE, UNKNOWN, REVIEW_REQUIRED status distinction.
3. **Documents & AI Extraction:** Extracted field confidence, page/bounding box provenance, advisory AI labels.
4. **Government Verification:** GST, Udyam, PAN, MCA, EPFO, ESIC, Startup India, Debarment with explicit `MOCK / DEMO` badges.
5. **Evidence & Lineage:** Interactive trace graph and 9 independent quality dimensions.
6. **Risk Assessment:** Non-linear risk score and advisory notices.
7. **Human Review:** Submission-scoped discrepancy queue and officer resolution form.
8. **Officer Decision & Manual Override:** Statutory decision submission & four-eyes manual override workflow.
9. **Audit Explorer:** Submission-scoped SHA-256 event log & chain verification trigger.

---

## 4. Key Architectural Safeguards
- **AI Non-Authoritative:** AI field extractions are explicitly labeled as advisory candidates.
- **Risk Does Not Disqualify:** Advisory risk scores prioritize officer review attention; risk does not decide qualification.
- **Missing Evidence $\neq$ FAIL:** Missing evidence is rendered distinctly as `MISSING_EVIDENCE (NON-FATAL)`.
- **Technical Timeout $\neq$ FAIL:** Government API transport timeouts trigger human review and manual verification fallback.
- **Human Authority Final:** Final procurement decisions belong exclusively to authorized human officers.
- **Audit Integrity:** Terminology strictly uses **"Verify Tamper-Evident SHA-256 Audit Hash Chain"** and **"Verify Audit Chain Integrity"**.
