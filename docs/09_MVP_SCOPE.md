# 09 — MVP Scope

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## 1. MVP Philosophy

The SIH MVP must demonstrate the **core value proposition** of the platform in a 5–10 minute demo while being technically honest about what is real, what is sandboxed, and what is mocked.

**Principles:**
1. **Depth over breadth** — Better to deeply demonstrate 5 verification domains than superficially touch 15
2. **Honest labelling** — MOCK integrations clearly labelled; no pretending mock is live
3. **End-to-end flow** — Complete workflow from tender → evaluation → decision → audit
4. **AI showcase** — Visible AI at work (extraction, classification, explanation)
5. **Deterministic rigor** — Rule engine visibly evaluating with evidence
6. **Audit credibility** — Complete evidence chain for every decision

---

## 2. Recommended MVP Verification Domains (6 Domains)

### Selection Criteria

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Common in CPCL tenders | HIGH | Directly relevant to problem statement |
| Demonstrable with mock/synthetic data | HIGH | Must work for SIH demo |
| Showcases AI capabilities | HIGH | SIH judges value AI innovation |
| Showcases cross-verification | MEDIUM | Key differentiator |
| Government API potentially accessible | LOW | Nice-to-have but not blocking |

### Selected Domains

| # | Domain | Mode | Why Selected |
|---|--------|------|-------------|
| 1 | **PAN Verification** | MOCK | Universal requirement; enables cross-verification with GST; simple identifier validation |
| 2 | **GST Verification** | MOCK (SANDBOX if GSP available) | Universal requirement; rich data (status, filings, legal name); cross-verification with PAN |
| 3 | **MCA / Company Verification** | MOCK | Required for company bidders; director info; company status; cross-verification with PAN/GST |
| 4 | **Udyam / MSME Verification** | MOCK | Critical for MSME benefits; classification (Micro/Small/Medium); cross-verification |
| 5 | **Make in India / Local Content** | RULE ENGINE | Policy-based; demonstrates versioned rule engine; directly addresses a complex compliance area |
| 6 | **Debarment / Blacklisting** | MOCK (list-based) | Critical compliance gate; demonstrates multi-source aggregation; high-impact finding |

### Why These 6?

1. **PAN + GST + MCA** form the core **identity triangle** — cross-referencing these catches the most impactful inconsistencies (name mismatches, inactive registrations, shell companies)
2. **Udyam** demonstrates MSME verification — critical for public procurement preference rules
3. **Make in India** showcases our policy rule engine — complex, versioned, high-value for judges
4. **Debarment** is a pass/fail gate — dramatic impact in demo; demonstrates multi-source checking

### Deferred Domains (Phase 2+)

| Domain | Reason for Deferral | Claim Classification |
|--------|-------------------|----------------------|
| EPFO / ESIC | No suitable public API confirmed; manual-only; lower demo impact | MANUAL_FALLBACK |
| Startup India | Niche requirement; no suitable public API confirmed | MANUAL_FALLBACK |
| NSIC | Niche requirement; no suitable public API confirmed | MANUAL_FALLBACK |
| DigiLocker | Requires partner onboarding; consent flow complex for demo | REQUIRES_GOVERNMENT_APPROVAL |
| BIS | Niche requirement; no suitable public API confirmed | MANUAL_FALLBACK |
| Income Tax (beyond PAN) | No suitable public API confirmed for returns; PAN covers basic verification | MANUAL_FALLBACK |


---

## 3. MVP Feature Set

### 3.1 Tender Management (MVP)
- [ ] Upload tender document (PDF)
- [ ] AI extracts requirements from tender
- [ ] Officer confirms/modifies extracted requirements
- [ ] Display structured requirement checklist

### 3.2 Bidder Management (MVP)
- [ ] Add bidder with basic identifiers (PAN, GSTIN, CIN, Udyam, name)
- [ ] Format validation on identifiers
- [ ] PAN-GSTIN cross-validation (deterministic)

### 3.3 Document Processing (MVP)
- [ ] Upload bidder documents (PDF, images)
- [ ] AI classifies documents into categories
- [ ] AI extracts key fields with confidence scores
- [ ] Low-confidence extractions flagged for review

### 3.4 Government Verification (MVP)
- [ ] PAN verification (MOCK)
- [ ] GST verification (MOCK)
- [ ] MCA company verification (MOCK)
- [ ] Udyam verification (MOCK)
- [ ] Debarment check (MOCK list)
- [ ] Clear mode labels (MOCK/LIVE indicator)

### 3.5 Compliance Evaluation (MVP)
- [ ] Per-requirement evaluation (PASS/FAIL/REVIEW/MISSING/EXPIRED/CONFLICT/NOT_VERIFIED/NOT_APPLICABLE)
- [ ] Make in India classification rule engine
- [ ] Cross-source conflict detection (PAN name vs GST name vs MCA name)
- [ ] Compliance score + Evidence confidence + Risk score

### 3.6 AI Features (MVP)
- [ ] Document classification
- [ ] Field extraction
- [ ] Tender requirement extraction
- [ ] Compliance explanation generation
- [ ] Recommendation generation (with evidence citations)
- [ ] Conflict/inconsistency flagging

### 3.7 Human Decision (MVP)
- [ ] Evaluation dashboard per bidder
- [ ] Officer reviews all results
- [ ] QUALIFY / DISQUALIFY / SEEK_CLARIFICATION decision
- [ ] Mandatory rationale entry
- [ ] Decision recorded with timestamp and officer identity

### 3.8 Audit Trail (MVP)
- [ ] Action logging for all significant events
- [ ] Evidence chain per bidder per requirement
- [ ] Audit report generation

---

## 4. MVP Architecture Overview

```
┌─────────────────────────────────────────────────┐
│              FRONTEND (Web UI)                   │
│  React/Next.js or similar                        │
│  • Tender dashboard                              │
│  • Bidder evaluation view                        │
│  • Document viewer                               │
│  • Compliance matrix                             │
│  • Decision interface                            │
│  • Audit report viewer                           │
└──────────────────────┬──────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────┐
│              BACKEND API                         │
│  Python (FastAPI) or Node.js                     │
│  • Tender management                             │
│  • Bidder management                             │
│  • Document management                           │
│  • Compliance engine                             │
│  • Workflow management                           │
│  • Audit trail                                   │
└───┬──────────┬───────────┬──────────────────────┘
    │          │           │
    ▼          ▼           ▼
┌────────┐ ┌────────┐ ┌──────────────────────────┐
│   DB   │ │ AI SVC │ │ VERIFICATION ADAPTERS     │
│        │ │        │ │  ┌─────┐ ┌─────┐ ┌─────┐ │
│ Tender │ │ OCR    │ │  │MOCK │ │SBOX │ │LIVE │ │
│ Bidder │ │ NLP    │ │  │     │ │     │ │     │ │
│ Docs   │ │ LLM    │ │  │ PAN │ │ GST │ │ ... │ │
│ Rules  │ │        │ │  │ GST │ │     │ │     │ │
│ Audit  │ │        │ │  │ MCA │ │     │ │     │ │
│        │ │        │ │  │Udyam│ │     │ │     │ │
│        │ │        │ │  │Debar│ │     │ │     │ │
└────────┘ └────────┘ │  └─────┘ └─────┘ └─────┘ │
                      └──────────────────────────┘
```

---

## 5. Demo Data Requirements

### 5.1 Synthetic Tender
- CPCL-style tender document (realistic but synthetic)
- ~10 requirements covering: PAN, GST, MCA, Udyam, turnover, experience, local content, OEM, debarment, integrity pact
- At least one corrigendum modifying a requirement

### 5.2 Synthetic Bidders (4 scenarios)
See `11_DEMO_SCENARIO.md` for detailed scenarios.

### 5.3 Mock Government Data
- Pre-configured mock responses for PAN, GST, MCA, Udyam, Debarment
- Designed to produce the 4 bidder scenarios
- Clearly labelled as MOCK in all UI elements

---

## 6. What Can Be Built Immediately

| Component | Dependency | Status |
|-----------|-----------|--------|
| Tender document upload & management | None | ✅ Can build now |
| AI document classification | AI model API (Gemini/GPT) | ✅ Can build now |
| AI field extraction | AI model API | ✅ Can build now |
| AI requirement extraction | AI model API | ✅ Can build now |
| PAN/GSTIN format validation | None | ✅ Can build now |
| PAN-GSTIN cross-validation | None | ✅ Can build now |
| Mock verification adapters | None | ✅ Can build now |
| Compliance rule engine | None | ✅ Can build now |
| Make in India rule engine | Policy documents (public) | ✅ Can build now |
| Cross-source conflict detection | None | ✅ Can build now |
| Scoring engine | None | ✅ Can build now |
| AI explanation generation | AI model API | ✅ Can build now |
| Audit trail system | None | ✅ Can build now |
| Officer decision workflow | None | ✅ Can build now |
| Web UI | None | ✅ Can build now |

### What Requires External Authorization

| Component | Dependency | Lead Time |
|-----------|-----------|-----------|
| DigiLocker integration | Partner onboarding | Weeks to months |
| GST sandbox | GSP partnership | Weeks |
| PAN API (Protean) | Entity registration + DSC | Weeks to months |
| API Setu access | Organization registration + approval | Weeks |
| Real GeM integration | GeM administration arrangement | Months+ |

---

## 7. Technology Recommendations (Phase 1 Direction)

| Layer | Recommendation | Rationale |
|-------|---------------|-----------|
| **Frontend** | Next.js / React | Rich UI; component ecosystem; SSR for SEO |
| **Backend API** | Python (FastAPI) | AI ecosystem (Python ML libraries); fast development; async support |
| **Database** | PostgreSQL | ACID compliance; JSON support; mature; free |
| **Document Storage** | S3-compatible (MinIO for dev) | Scalable; encrypted; cost-effective |
| **AI Platform** | Google Gemini API | Vision (OCR) + Text (NLP) in one API; competitive pricing; multimodal |
| **Rule Engine** | Custom (Python) | Government procurement rules are unique; generic rule engines add complexity |
| **Cache** | Redis | Verification result caching; session management |
| **Container** | Docker + Docker Compose | SIH demo simplicity; Kubernetes for production |
| **Secrets** | HashiCorp Vault (or env vars for SIH) | Production-grade secrets management |

**PROPOSED DESIGN:** These are recommendations. Final technology selection should be made in Phase 1 based on team expertise and constraints.
