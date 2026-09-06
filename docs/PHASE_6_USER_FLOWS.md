# Phase 6 — User Journeys & End-to-End Procurement Flow

## 1. Primary SIH Demonstration Journey
```
LOGIN (/login)
  │
  ▼ (Select Demo Identity, e.g., ProcurementOfficer)
DASHBOARD (/dashboard)
  │
  ├──► TENDER CATALOG (/tenders) ──► TENDER WORKSPACE (/tenders/TEN_01)
  │
  └──► BID SUBMISSIONS (/bids) ──► BID WORKSPACE (/bids/SUB_01)
                                         │
                                         ├── Tab 1: OVERVIEW (Bidder 360 & Statutory Identifiers)
                                         ├── Tab 2: COMPLIANCE MATRIX (Flagship PASS/FAIL/MISSING)
                                         ├── Tab 3: DOCUMENTS & AI EXTRACTION (Bounding Box Provenance)
                                         ├── Tab 4: GOVERNMENT VERIFICATION (GST, Udyam, PAN, MCA with MOCK badges)
                                         ├── Tab 5: EVIDENCE & LINEAGE (9 Independent Quality Dimensions)
                                         ├── Tab 6: ADVISORY RISK ENGINE (Risk Score as Review Prioritizer)
                                         ├── Tab 7: HUMAN REVIEW WORKSPACE (Officer Resolution Form)
                                         ├── Tab 8: OFFICER DECISION & OVERRIDE (Four-Eyes Manual Overrides)
                                         └── Tab 9: AUDIT EXPLORER (Tamper-Evident SHA-256 Hash Chain)
```

---

## 2. Key User Flow Guidelines
- **Demo Identity Login:** Authenticates against backend `/api/v1/auth/login` to obtain real backend JWT scopes for predefined roles.
- **Compliance Matrix Inspection:** Officers review deterministic evaluation status (`PASS`, `FAIL`, `MISSING_EVIDENCE`, `UNKNOWN`, `REVIEW_REQUIRED`).
- **Four-Eyes Manual Override:** Propose override for a requirement $\rightarrow$ Requires peer approval by Senior Reviewer or Compliance Officer before updating effective compliance overlay.
- **Officer Decision Submission:** Final decision (`QUALIFIED`, `DISQUALIFIED`, `REQUIRES_CLARIFICATION`, `EVIDENCE_REQUESTED`) recorded with mandatory officer rationale and committed to the audit chain.
