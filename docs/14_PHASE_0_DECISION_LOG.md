# 14 — Phase 0 Decision Log

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## Decision Log

Every major design decision made during Phase 0 is recorded here with rationale.

---

### D01: AI Boundary — AI Assists, Human Decides

| Attribute | Detail |
|-----------|--------|
| **Decision** | AI outputs are advisory only. The procurement officer makes all qualification/disqualification decisions. |
| **Status** | APPROVED |
| **Rationale** | CVC guidelines require human accountability for procurement decisions. AI cannot be audited the same way a named officer can. Over-automation creates liability. SIH problem statement explicitly requires final decision by procurement officer. |
| **Alternatives Considered** | (1) Full AI automation — rejected due to accountability/audit requirements; (2) AI decides with human veto — rejected as inverting the accountability model |
| **Impact** | System design, workflow, UI, audit trail |
| **Classification** | PROPOSED DESIGN |

---

### D02: Three-Dimensional Compliance Scoring

| Attribute | Detail |
|-----------|--------|
| **Decision** | Use three separate scores (Compliance Score, Evidence Confidence, Risk Score) instead of a single percentage. |
| **Status** | APPROVED |
| **Rationale** | A single score masks critical information. A bidder can be 90% compliant but have 40% evidence confidence (mostly self-declared). A bidder can have 100% compliance but 80% risk (debarment pending investigation). Three dimensions give the procurement officer actionable insight. |
| **Alternatives Considered** | (1) Single percentage — rejected as misleading; (2) Five dimensions — rejected as too complex for initial version |
| **Impact** | Compliance model, scoring engine, UI dashboard |
| **Classification** | PROPOSED DESIGN |

---

### D03: Government Integration Abstraction (LIVE/SANDBOX/MOCK/MANUAL)

| Attribute | Detail |
|-----------|--------|
| **Decision** | Every government integration implements four modes (LIVE, SANDBOX, MOCK, MANUAL) behind a uniform adapter interface. |
| **Status** | APPROVED |
| **Rationale** | Research confirms no suitable publicly documented/accessible APIs were confirmed for most government systems without authorization. The system must gracefully handle this reality. Mock mode enables SIH demo. Manual mode enables production use for systems without APIs. The adapter pattern isolates integration changes. |
| **Alternatives Considered** | (1) Only build integrations where APIs exist — rejected as too limiting; (2) Scrape government portals — rejected as illegal/unreliable; (3) Only manual verification — rejected as not leveraging available APIs |
| **Impact** | Architecture, integration layer, deployment configuration |
| **Classification** | PROPOSED DESIGN based on CONFIRMED findings (unconfirmed/restricted APIs for most systems) |

---

### D04: MVP Verification Domains — 6 Selected

| Attribute | Detail |
|-----------|--------|
| **Decision** | MVP focuses on PAN, GST, MCA, Udyam, Make in India, and Debarment as the 6 demonstration domains. |
| **Status** | APPROVED |
| **Rationale** | PAN + GST + MCA form the identity triangle enabling cross-verification (the key differentiator). Udyam demonstrates MSME compliance. Make in India showcases the versioned rule engine. Debarment is a dramatic pass/fail gate for demo impact. |
| **Alternatives Considered** | Including EPFO/ESIC — deferred due to unconfirmed public API status and low demo impact; Including DigiLocker — deferred due to partner onboarding timeline |
| **Impact** | MVP scope, mock data design, demo scenario |
| **Classification** | PROPOSED DESIGN |

---

### D05: Evidence-First Architecture

| Attribute | Detail |
|-----------|--------|
| **Decision** | Every compliance decision must be traceable to an evidence chain: document → extraction → verification → rule → decision. |
| **Status** | APPROVED |
| **Rationale** | CVC/CAG audits require defensible decisions. Without evidence chains, the system is a black box. Evidence-first design is our primary innovation differentiator. |
| **Alternatives Considered** | (1) Checkbox compliance (pass/fail without evidence) — rejected as audit-vulnerable; (2) Document-only (store documents but no extraction) — rejected as not adding value |
| **Impact** | Data model, storage, audit system, UI |
| **Classification** | PROPOSED DESIGN |

---

### D06: Deterministic Rule Engine (Not AI-Based)

| Attribute | Detail |
|-----------|--------|
| **Decision** | Compliance rules are evaluated by a deterministic rule engine, NOT by AI. AI assists in extracting data but rules themselves are code. |
| **Status** | APPROVED |
| **Rationale** | Rules must be reproducible, versioned, testable, and auditable. AI-based rule evaluation would be non-deterministic — the same input could produce different outputs. CVC requires reproducible compliance evaluation. |
| **Alternatives Considered** | (1) AI evaluates rules — rejected as non-reproducible; (2) Hybrid (AI suggests, rules confirm) — the chosen approach |
| **Impact** | Rule engine design, compliance model, AI boundary |
| **Classification** | PROPOSED DESIGN |

---

### D07: Make in India — Versioned Policy Engine

| Attribute | Detail |
|-----------|--------|
| **Decision** | Make in India compliance rules are implemented as versioned policies, not hard-coded constants. |
| **Status** | APPROVED |
| **Rationale** | The PPP-MII Order has been amended multiple times (latest: July 2024). Nodal ministries can set sector-specific thresholds. Each tender may reference a different policy version. Hard-coding would be immediately outdated. |
| **Alternatives Considered** | (1) Hard-code current thresholds — rejected as fragile; (2) External policy document parsing — too complex for MVP |
| **Impact** | Rule engine, policy management, data model |
| **Classification** | OFFICIAL_DOCUMENTED policy rules; PROPOSED DESIGN engine |

---

### D08: No Government Portal Scraping

| Attribute | Detail |
|-----------|--------|
| **Decision** | The system will NOT scrape government portals. Only official APIs and manual verification are acceptable. |
| **Status** | APPROVED |
| **Rationale** | Scraping violates government portal Terms of Service. CAPTCHAs and anti-bot measures make scraping unreliable. IT Act 2000 implications. Government portals change frequently, breaking scrapers. |
| **Alternatives Considered** | (1) Scrape where no suitable public API is confirmed — rejected; (2) Use third-party scrapers — rejected |
| **Impact** | Integration strategy, fallback design |
| **Classification** | PROPOSED DESIGN based on OFFICIAL_DOCUMENTED ToS restrictions |

---

### D09: Buyer-Side Focus (Not Bidder-Side)

| Attribute | Detail |
|-----------|--------|
| **Decision** | The platform serves procurement officers (buyer-side), not bidders (seller-side). |
| **Status** | APPROVED |
| **Rationale** | Problem statement is from CPCL (a buyer). Most existing solutions are bidder-side (see competitor analysis). Buyer-side compliance verification is an underserved niche. Our innovation is in evaluation, not bid preparation. |
| **Alternatives Considered** | (1) Both sides — rejected as scope creep; (2) Bidder-side — rejected as already served by competitors |
| **Impact** | Entire solution design, feature prioritization |
| **Classification** | PROPOSED DESIGN |

---

### D10: Synthetic/Mock Data for SIH Demo

| Attribute | Detail |
|-----------|--------|
| **Decision** | SIH demo uses entirely synthetic data — no real PAN, GSTIN, or personal data. |
| **Status** | APPROVED |
| **Rationale** | Using real government data without authorization is illegal. Real data could contain PII violating DPDP Act. Synthetic data can be crafted to showcase all four bidder scenarios perfectly. |
| **Alternatives Considered** | (1) Use real data — rejected (legal); (2) Use anonymized real data — rejected (still risky and unnecessary) |
| **Impact** | Demo data preparation, mock service design |
| **Classification** | PROPOSED DESIGN based on OFFICIAL_DOCUMENTED DPDP legal requirements |

---

### D11: Tender-Specific Requirements (Not Universal Template)

| Attribute | Detail |
|-----------|--------|
| **Decision** | Each tender defines its own requirement set. There is no universal "one-size-fits-all" evaluation template. |
| **Status** | APPROVED |
| **Rationale** | Research on CPCL tenders shows requirements vary significantly by tender type, value, and category. A rigid template would miss tender-specific requirements or apply inapplicable ones. |
| **Alternatives Considered** | (1) Universal template — rejected as too rigid; (2) Category-based templates with overrides — possible future enhancement |
| **Impact** | Data model (requirement linked to tender, not system), UI, rule engine |
| **Classification** | PROPOSED DESIGN based on CONFIRMED tender variation |

---

### D12: Cross-Source Conflict Detection as Core Feature

| Attribute | Detail |
|-----------|--------|
| **Decision** | Cross-source conflict detection (comparing data across PAN, GST, MCA, Udyam records) is a core feature, not an add-on. |
| **Status** | APPROVED |
| **Rationale** | This is our strongest differentiator — no competitor offers this. It catches real fraud/inconsistency scenarios. It demonstrates the value of multi-source verification beyond simple checkbox compliance. High demo impact. |
| **Alternatives Considered** | (1) Optional feature — rejected as underselling the innovation |
| **Impact** | Architecture, verification flow, data model, demo design |
| **Classification** | PROPOSED DESIGN |

---

## Open Decisions (Requiring Phase 1 Resolution)

| # | Decision | Options | Dependencies |
|---|----------|---------|-------------|
| OD1 | Frontend framework | Next.js / React / Vue | Team expertise |
| OD2 | Backend language | Python (FastAPI) / Node.js (Express) | Team expertise; AI ecosystem needs |
| OD3 | Database | PostgreSQL / MongoDB | Data model complexity; query patterns |
| OD4 | AI provider | Google Gemini / OpenAI GPT / Open-source | Cost, capability, availability |
| OD5 | Deployment target | Docker Compose / Kubernetes / Cloud | SIH venue infrastructure |
| OD6 | Document storage | MinIO / S3 / Local FS | Scale requirements; encryption needs |
| OD7 | Authentication approach | JWT + MFA / OAuth 2.0 / SSO | Security requirements; demo simplicity |

