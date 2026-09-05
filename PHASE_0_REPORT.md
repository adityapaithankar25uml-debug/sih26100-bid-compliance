# PHASE 0 REPORT

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited  
**Category:** Software | **Theme:** Smart Automation  
**Phase:** 0 — Research & Ground Truth Complete  
**Date:** 2026-09-05

---

## Executive Summary

This Phase 0 report establishes the factual and technical ground truth for building an AI-Powered Integrated Bid Compliance Verification Platform. The platform will assist CPCL procurement officers in verifying bidder compliance against tender requirements using AI-powered document intelligence, government source verification, deterministic rule evaluation, and a complete audit trail.

**Core Principle:** AI interprets → Authorized sources verify → Rules evaluate → Evidence proves → Human approves.

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## 1. What We Know ✅

| # | Finding | Claim Classification | Source |
|---|---------|---------------------|--------|
| 1 | No suitable publicly documented/publicly accessible API was confirmed for GeM during Phase 0 research | CONFIRMED | gem.gov.in; web research |
| 2 | API Setu (apisetu.gov.in) hosts 4,200+ government APIs with OAuth 2.0 auth | OFFICIAL_DOCUMENTED | apisetu.gov.in |
| 3 | DigiLocker API requires partner onboarding (verification call + agreement) | REQUIRES_GOVERNMENT_APPROVAL | partners.apisetu.gov.in |
| 4 | GST APIs are available through GST Developer Portal but require GSP partnership | REQUIRES_GOVERNMENT_APPROVAL | developer.gst.gov.in |
| 5 | No suitable publicly documented/publicly accessible API was confirmed for MCA company verification during Phase 0 research | CONFIRMED | mca.gov.in |
| 6 | No suitable publicly documented/publicly accessible API was confirmed for Udyam/MSME verification during Phase 0 research | CONFIRMED | udyamregistration.gov.in |
| 7 | PAN verification API exists via Protean eGov but requires entity registration + DSC | REQUIRES_GOVERNMENT_APPROVAL | protean-india.com |
| 8 | No suitable publicly documented/publicly accessible APIs were confirmed for EPFO, ESIC, Startup India, or NSIC during Phase 0 research | CONFIRMED | Official portals |
| 9 | No suitable publicly documented/publicly accessible API was confirmed for CPPP, but a web-searchable Debarment List is available | CONFIRMED | eprocure.gov.in |
| 10 | No single authoritative nationwide debarment database covering all relevant procurement entities was confirmed | CONFIRMED | eprocure.gov.in; CVC guidelines |
| 11 | Make in India Order 2017 (amended July 2024) defines Class-I (≥50%), Class-II (≥20-50%), Non-Local (<20%) | OFFICIAL_DOCUMENTED | dpiit.gov.in |
| 12 | CPCL uses NIC's e-procurement platform (cpcletenders.nic.in) | OFFICIAL_DOCUMENTED | cpcletenders.nic.in |
| 13 | Most existing competitors are bidder-side (not buyer-side) | ASSUMPTION | Market research |
| 14 | No existing platform combines AI document intelligence + government verification + rule engine + evidence chain | ASSUMPTION | Competitor analysis |
| 15 | SIH judges evaluate on: novelty, problem understanding, technical depth, social impact, presentation | OFFICIAL_DOCUMENTED | SIH guidelines |

---

## 2. What We Don't Know ❓

| # | Unknown | Impact | Resolution Path |
|---|---------|--------|----------------|
| 1 | Exact API Setu APIs available for our use case | MEDIUM | Register on apisetu.gov.in; browse catalog |
| 2 | Whether GSP sandbox access can be obtained within SIH timeline | MEDIUM | Contact GSPs (MasterGST, etc.); initiate partnership |
| 3 | CPCL-specific tender requirements beyond common patterns | MEDIUM | Analyze actual CPCL tender documents from cpcletenders.nic.in |
| 4 | Exact DPDP Act implications for processing bidder PAN/GSTIN | MEDIUM | Legal consultation |
| 5 | Whether API Setu registration can be fast-tracked for SIH | LOW | Contact API Setu team |
| 6 | CPCL internal holiday/banned contractor list format | LOW | Contact CPCL procurement if possible |
| 7 | SIH 2026 final judging criteria weights | LOW | Follow SIH guidelines; check with SPOC |

---

## 3. What Requires Authorization 🔐

Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

| # | Integration | Authorization Required From | Claim Classification | Timeline Estimate |
|---|------------|---------------------------|----------------------|-------------------|
| 1 | DigiLocker API | MeitY via partners.apisetu.gov.in | REQUIRES_GOVERNMENT_APPROVAL | Weeks to months |
| 2 | GST API (production) | GSTN via licensed GSP | REQUIRES_GOVERNMENT_APPROVAL | Weeks |
| 3 | PAN API (production) | Protean eGov Technologies | REQUIRES_GOVERNMENT_APPROVAL | Weeks (registration + DSC) |
| 4 | API Setu APIs | MeitY via apisetu.gov.in | REQUIRES_GOVERNMENT_APPROVAL | Days to weeks |
| 5 | GeM integration | GeM administration | REQUIRES_GOVERNMENT_APPROVAL | Months+ (formal arrangement) |

---

## 4. What Can Be Built Immediately 🚀

| # | Component | External Dependency |
|---|-----------|-------------------|
| 1 | Tender document upload and management | None |
| 2 | AI document classification (using Gemini/GPT) | AI API key only |
| 3 | AI field extraction from documents | AI API key only |
| 4 | AI tender requirement extraction | AI API key only |
| 5 | PAN/GSTIN/CIN/Udyam format validation | None |
| 6 | PAN-GSTIN cross-validation | None |
| 7 | All mock verification adapters (PAN, GST, MCA, Udyam, Debarment) | None |
| 8 | Compliance rule engine | None |
| 9 | Make in India versioned rule engine | None (policy is public) |
| 10 | Cross-source conflict detection | None |
| 11 | Three-dimensional scoring engine | None |
| 12 | AI explanation and recommendation generation | AI API key only |
| 13 | Complete audit trail system | None |
| 14 | Officer decision workflow | None |
| 15 | Web UI for all above | None |

---

## 5. What Must Be Mocked 🎭

| # | Integration | Mock Behavior | Claim Classification |
|---|------------|--------------|----------------------|
| 1 | PAN Verification | Return pre-configured name, status (Active/Inactive) | MOCK_ONLY |
| 2 | GST Verification | Return registration status, legal name, filing status, registration date | MOCK_ONLY |
| 3 | MCA/CIN Verification | Return company status, directors, incorporation date | MOCK_ONLY |
| 4 | Udyam Verification | Return classification (Micro/Small/Medium), registration validity | MOCK_ONLY |
| 5 | Debarment Check | Return match/no-match against pre-configured list | MOCK_ONLY |

**All mock responses MUST be clearly labelled as MOCK in the UI.**

---

## 6. What Should Be MVP 🎯

| Priority | Feature | Rationale |
|----------|---------|-----------|
| MUST | Tender requirement extraction (AI) | Core AI showcase |
| MUST | Document classification & field extraction (AI) | Core AI showcase |
| MUST | 6-domain verification (PAN, GST, MCA, Udyam, MII, Debarment) | Identity triangle + policy engine + compliance gate |
| MUST | Cross-source conflict detection | Primary differentiator |
| MUST | Deterministic compliance rule engine | Core evaluation logic |
| MUST | Three-dimensional risk scoring | Analytical depth |
| MUST | Explainable compliance (AI) | AI transparency showcase |
| MUST | Officer decision workflow | Human-in-the-loop requirement |
| MUST | Complete audit trail | CVC/CAG compliance |
| SHOULD | Bidder 360 identity graph | Visual differentiator |
| NICE | Corrigendum impact analysis | Innovation showcase |
| NICE | Simple anomaly detection | Fraud detection preview |

---

## 7. What Should Be Deferred ⏸️

| # | Feature | Reason | Claim Classification |
|---|---------|--------|----------------------|
| 1 | EPFO/ESIC verification | No suitable public API confirmed; manual-only; low demo impact | MANUAL_FALLBACK |
| 2 | Startup India verification | No suitable public API confirmed; niche requirement | MANUAL_FALLBACK |
| 3 | NSIC verification | No suitable public API confirmed; niche requirement | MANUAL_FALLBACK |
| 4 | BIS verification | No suitable public API confirmed; niche requirement | MANUAL_FALLBACK |
| 5 | DigiLocker live integration | Partner onboarding timeline | REQUIRES_GOVERNMENT_APPROVAL |
| 6 | Compliance drift detection | Requires temporal data | UNVERIFIED |
| 7 | Procurement analytics | Requires historical data | UNVERIFIED |
| 8 | Multi-language support | Not core innovation | UNVERIFIED |
| 9 | Real GeM integration | No suitable public API confirmed; requires formal arrangement | REQUIRES_GOVERNMENT_APPROVAL |
| 10 | Blockchain-anchored audit | Over-engineering for MVP | ASSUMPTION |

---

## 8. Top 10 Technical Risks ⚠️

| # | Risk | Severity | Mitigation |
|---|------|----------|-----------|
| 1 | Unconfirmed or restricted government API access | CRITICAL | LIVE/SANDBOX/MOCK/MANUAL architecture |
| 2 | AI hallucination in compliance recommendations | CRITICAL | Evidence grounding; confidence thresholds; human review |
| 3 | DPDP Act compliance for PII processing | HIGH | Consent management; data minimization; legal review |
| 4 | Inaccurate OCR on poor-quality government documents | HIGH | Confidence scoring; human review for low-confidence |
| 5 | Incorrect rule implementation for complex policies | HIGH | Unit testing; policy versioning; officer override |
| 6 | Over-reliance on AI by procurement officers | HIGH | UX design requiring rationale; mandatory review steps |
| 7 | Prompt injection via malicious documents | MEDIUM | Input sanitization; output validation; sandboxing |
| 8 | False negatives (passing non-compliant bidders) | HIGH | Multi-source verification; cross-source checking |
| 9 | SIH demo environment failure | MEDIUM | Pre-computed results; rehearsal; backup plan |
| 10 | Vendor lock-in on AI provider | MEDIUM | AI abstraction layer; provider-agnostic design |

---

## 9. Top 10 Innovation Opportunities 💡

| # | Innovation | SIH Impact | Feasibility |
|---|-----------|-----------|-------------|
| 1 | Evidence-first compliance architecture | ⭐⭐⭐⭐⭐ | HIGH |
| 2 | Cross-source conflict detection | ⭐⭐⭐⭐⭐ | HIGH |
| 3 | Explainable compliance with evidence citations | ⭐⭐⭐⭐⭐ | HIGH |
| 4 | Bidder 360 identity graph visualization | ⭐⭐⭐⭐ | HIGH |
| 5 | Government integration abstraction (LIVE/SANDBOX/MOCK/MANUAL) | ⭐⭐⭐⭐ | HIGH |
| 6 | Versioned policy engine (Make in India) | ⭐⭐⭐⭐ | HIGH |
| 7 | Three-dimensional compliance scoring | ⭐⭐⭐⭐ | HIGH |
| 8 | Corrigendum impact analysis | ⭐⭐⭐⭐ | MEDIUM |
| 9 | Anomaly detection across bidders | ⭐⭐⭐ | MEDIUM |
| 10 | AI-assisted tender requirement extraction | ⭐⭐⭐⭐⭐ | HIGH |

---

## 10. Recommended Phase 1 Architecture Direction

### Architecture Pattern
- **Backend:** Python (FastAPI) — best AI ecosystem integration; async support; fast development
- **Frontend:** React/Next.js — component-based; rich UI capability
- **Database:** PostgreSQL — ACID compliance; JSON support; mature
- **AI Layer:** Google Gemini API (multimodal: vision + text) — OCR + NLP in one API
- **Integration Layer:** Adapter pattern with LIVE/SANDBOX/MOCK/MANUAL modes
- **Cache:** Redis — verification result caching; session management
- **Deployment:** Docker Compose for SIH; Kubernetes-ready for production

### Key Architectural Principles
1. **Separation of Concerns:** AI layer, verification layer, rule engine, and workflow are independent modules
2. **Adapter Pattern:** Every external integration behind a uniform interface
3. **Event Sourcing (simplified):** All state changes logged as immutable events for audit
4. **Configuration-Driven Rules:** Compliance rules configurable per tender, not hard-coded
5. **Graceful Degradation:** System continues operating when any external service is unavailable

### Phase 1 Priorities
- System architecture
- Database/ERD design
- API contract design
- Compliance ontology
- Rule-engine architecture
- Government adapter interfaces
- AI provider abstraction
- Security architecture
- Evidence/audit architecture
- Implementation backlog
- Acceptance-test strategy

---

## Documentation Index

| File | Description |
|------|------------|
| [01_PROBLEM_ANALYSIS.md](docs/01_PROBLEM_ANALYSIS.md) | Problem decomposition, stakeholder analysis, MECE categories |
| [02_FUNCTIONAL_REQUIREMENTS.md](docs/02_FUNCTIONAL_REQUIREMENTS.md) | All functional requirements (FR-01 through FR-10) |
| [03_NON_FUNCTIONAL_REQUIREMENTS.md](docs/03_NON_FUNCTIONAL_REQUIREMENTS.md) | Performance, security, scalability, compliance requirements |
| [04_GOVERNMENT_INTEGRATION_MATRIX.md](docs/04_GOVERNMENT_INTEGRATION_MATRIX.md) | 16 government integration sources researched with API availability |
| [05_AI_BOUNDARY.md](docs/05_AI_BOUNDARY.md) | What AI may/must not do; deterministic responsibilities |
| [06_SECURITY_REQUIREMENTS.md](docs/06_SECURITY_REQUIREMENTS.md) | Threat model, authentication, data protection, DPDP compliance |
| [07_COMPLIANCE_DOMAIN_MODEL.md](docs/07_COMPLIANCE_DOMAIN_MODEL.md) | Entity models, status model, scoring rationale, Make in India rules |
| [08_COMPETITOR_ANALYSIS.md](docs/08_COMPETITOR_ANALYSIS.md) | 8+ competitors analyzed with gap analysis |
| [09_MVP_SCOPE.md](docs/09_MVP_SCOPE.md) | 6 verification domains, feature set, technology recommendations |
| [10_INNOVATION_SCOPE.md](docs/10_INNOVATION_SCOPE.md) | 10 innovation features ranked by feasibility and SIH impact |
| [11_DEMO_SCENARIO.md](docs/11_DEMO_SCENARIO.md) | Complete 10-minute demo script with 4 bidder scenarios |
| [12_RISKS_AND_ASSUMPTIONS.md](docs/12_RISKS_AND_ASSUMPTIONS.md) | 20 risks + 10 assumptions with mitigations |
| [13_SOURCE_REGISTER.md](docs/13_SOURCE_REGISTER.md) | All research sources with authority levels |
| [14_PHASE_0_DECISION_LOG.md](docs/14_PHASE_0_DECISION_LOG.md) | 12 major decisions with rationale |

---

## Classification of Claims

Throughout this documentation package, every statement and finding is assigned one of the following official claim classifications:

- **CONFIRMED** — Fact verified against authoritative primary sources or empirical verification.
- **OFFICIAL_DOCUMENTED** — Directly stated in official government policy, portal guidelines, or documentation.
- **REQUIRES_GOVERNMENT_APPROVAL** — Official integration requires formal government onboarding, MoU, GSP partnership, or departmental authorization.
- **UNVERIFIED** — Secondary source claim or requirement requiring further validation before implementation.
- **ASSUMPTION** — Architectural or operational premise based on available evidence, requiring validation in Phase 1.
- **MOCK_ONLY** — Integration simulated via local mock adapters during prototype/sandbox development due to restricted live API endpoints.
- **MANUAL_FALLBACK** — Verification requiring human officer document upload, manual portal lookup, or OCR extraction when automated API access is unavailable.

---

## Status

**Phase 0 is COMPLETE.**

**DO NOT proceed to Phase 1 implementation until this report has been reviewed and approved.**

**No application code has been written. No frontend, backend, database, API integration, or Docker configuration has been created.**

**Phase 1 will begin only after team review and approval of this Phase 0 intelligence package.**
