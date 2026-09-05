# 12 — Risks and Assumptions

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## 1. Risk Register

### R01: Government API Unavailability

| Attribute | Detail |
|-----------|--------|
| **Description** | No suitable publicly documented/publicly accessible APIs were confirmed for most government verification sources during Phase 0 research (see Integration Matrix). |
| **Probability** | CERTAIN (for SIH) |
| **Impact** | HIGH — Core feature (government verification) is limited |
| **Mitigation** | Architecture supports LIVE/SANDBOX/MOCK/MANUAL modes; mock adapters clearly labelled; graceful degradation |
| **Fallback** | MOCK for demo; MANUAL for production where no suitable public API is confirmed |
| **Status** | ACCEPTED — This is a known constraint, not a surprise |

### R02: API Approval Delays

| Attribute | Detail |
|-----------|--------|
| **Description** | Even where APIs exist (DigiLocker, GST via GSP, PAN via Protean), the registration/approval process takes weeks to months. |
| **Probability** | HIGH |
| **Impact** | MEDIUM — Demo works with mock; production integration delayed |
| **Mitigation** | Begin registration early; design for mock-first; document approval requirements clearly |
| **Fallback** | Mock adapters for SIH; initiate approval process in parallel |
| **Status** | PLANNED |

### R03: Government Portal Changes

| Attribute | Detail |
|-----------|--------|
| **Description** | Government portals (GST, MCA, EPFO, etc.) frequently change their UI, add CAPTCHAs, or modify data formats. |
| **Probability** | MEDIUM |
| **Impact** | LOW (if we use APIs) to HIGH (if we relied on scraping — we do NOT) |
| **Mitigation** | Use official APIs only; adapter pattern isolates changes; never scrape government portals |
| **Fallback** | Adapter pattern means changes affect only one module |
| **Status** | MITIGATED BY DESIGN |

### R04: Inaccurate OCR/Extraction

| Attribute | Detail |
|-----------|--------|
| **Description** | AI-powered OCR may produce inaccurate extractions from poor-quality scans, handwritten documents, or unusual formats. |
| **Probability** | HIGH — Government documents vary wildly in quality |
| **Impact** | HIGH — Incorrect extractions could lead to wrong compliance decisions |
| **Mitigation** | Confidence scoring; low-confidence flagging for human review; human override capability; multiple extraction passes |
| **Fallback** | Manual entry as ultimate fallback |
| **Status** | MITIGATED |

### R05: AI Hallucination

| Attribute | Detail |
|-----------|--------|
| **Description** | LLMs may generate plausible but incorrect information, fabricate compliance explanations, or misinterpret documents. |
| **Probability** | MEDIUM |
| **Impact** | CRITICAL — Fabricated compliance data could lead to wrong procurement decisions |
| **Mitigation** | Ground all outputs in source documents; require evidence citations; confidence thresholds; human review for all AI outputs; AI outputs never auto-actioned |
| **Fallback** | AI outputs are always suggestions; deterministic rules make the actual compliance decision |
| **Status** | MITIGATED BY AI BOUNDARY DESIGN |

### R06: Prompt Injection

| Attribute | Detail |
|-----------|--------|
| **Description** | Malicious content in uploaded documents could manipulate AI behavior (e.g., embedded instructions in a PDF). |
| **Probability** | LOW-MEDIUM |
| **Impact** | HIGH — Could corrupt extraction results |
| **Mitigation** | Input sanitization; output validation; sandboxed AI execution; prompt hardening; AI outputs validated against expected schemas |
| **Fallback** | Human review catches anomalous AI outputs |
| **Status** | PLANNED |

### R07: Malicious Document Upload

| Attribute | Detail |
|-----------|--------|
| **Description** | Bidders could upload malware-laden files, oversized files, or crafted files to exploit vulnerabilities. |
| **Probability** | LOW |
| **Impact** | HIGH — System compromise |
| **Mitigation** | File type validation (magic bytes); size limits; malware scanning; sandboxed processing; content disarm and reconstruction (CDR) |
| **Fallback** | Reject suspicious files; manual processing |
| **Status** | PLANNED |

### R08: Incorrect Rule Interpretation

| Attribute | Detail |
|-----------|--------|
| **Description** | The rule engine may incorrectly implement procurement rules, especially complex Make in India calculations. |
| **Probability** | MEDIUM |
| **Impact** | HIGH — Incorrect compliance decisions |
| **Mitigation** | Rule unit testing; policy versioning; rule review by domain experts; human override capability |
| **Fallback** | Procurement officer can override any rule result with documented rationale |
| **Status** | MITIGATED BY DESIGN |

### R09: Stale Government Data

| Attribute | Detail |
|-----------|--------|
| **Description** | Cached verification results may become stale (e.g., GST registration cancelled after verification). |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM — Decisions based on outdated information |
| **Mitigation** | Configurable cache TTL; re-verification capability; timestamp visible on all verification results |
| **Fallback** | Manual re-verification before final decision |
| **Status** | MITIGATED |

### R10: Identity Mismatch / Entity Resolution Failure

| Attribute | Detail |
|-----------|--------|
| **Description** | The system may fail to correctly link or distinguish entities with similar names, merged/demerged companies, or name changes. |
| **Probability** | MEDIUM |
| **Impact** | HIGH — Wrong entity verified; wrong debarment match |
| **Mitigation** | Multi-factor entity resolution (PAN + GSTIN + CIN); fuzzy matching with confidence; cross-source validation; human review for uncertain matches |
| **Fallback** | Flag uncertain matches for human review |
| **Status** | MITIGATED |

### R11: Privacy / DPDP Act Violation

| Attribute | Detail |
|-----------|--------|
| **Description** | Processing bidder PII (PAN, directors, financial data) without proper consent or purpose limitation could violate DPDP Act 2023. |
| **Probability** | LOW (if properly designed) |
| **Impact** | CRITICAL — Legal liability, project shutdown |
| **Mitigation** | Consent management; purpose limitation; data minimization; retention policies; encryption; access controls |
| **Fallback** | Bidder consent obtained as part of bid submission process |
| **Status** | PLANNED — Requires legal review |

### R12: Authentication / Authorization Failure

| Attribute | Detail |
|-----------|--------|
| **Description** | Unauthorized access to the system could enable data theft or decision manipulation. |
| **Probability** | LOW (if properly implemented) |
| **Impact** | CRITICAL — Procurement integrity compromised |
| **Mitigation** | MFA; RBAC; session management; audit logging; credential vault; regular security review |
| **Fallback** | Incident response plan; session invalidation |
| **Status** | PLANNED |

### R13: Audit Log Tampering

| Attribute | Detail |
|-----------|--------|
| **Description** | A compromised insider could attempt to modify or delete audit logs to cover tracks. |
| **Probability** | LOW |
| **Impact** | CRITICAL — Destroys evidence integrity |
| **Mitigation** | Append-only storage; hash chaining; separate access controls; log integrity verification; external backup |
| **Fallback** | External audit log replication; blockchain anchoring (future enhancement) |
| **Status** | MITIGATED BY DESIGN |

### R14: Vendor Lock-in (AI Provider)

| Attribute | Detail |
|-----------|--------|
| **Description** | Deep dependency on a single AI provider (e.g., Gemini, OpenAI) could create switching costs and availability risks. |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM — AI functionality degraded if provider changes pricing/availability |
| **Mitigation** | AI abstraction layer; provider-agnostic prompt design; multi-provider support architecture |
| **Fallback** | Switch to alternative provider; open-source model fallback |
| **Status** | PLANNED |

### R15: API Rate Limits

| Attribute | Detail |
|-----------|--------|
| **Description** | Government APIs (where they exist) and AI APIs have rate limits that could throttle operations. |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM — Slower processing; queued verifications |
| **Mitigation** | Client-side rate limiting; request queuing; result caching; batch processing |
| **Fallback** | Graceful degradation; manual verification fallback |
| **Status** | PLANNED |

### R16: Network Failures

| Attribute | Detail |
|-----------|--------|
| **Description** | Network issues could prevent API calls to government systems or AI providers. |
| **Probability** | MEDIUM |
| **Impact** | MEDIUM — Verification blocked; AI features unavailable |
| **Mitigation** | Circuit breaker pattern; retry with backoff; offline capability for deterministic functions; cached results |
| **Fallback** | Manual verification; pre-computed AI results |
| **Status** | PLANNED |

### R17: False Positives (Incorrect FAIL)

| Attribute | Detail |
|-----------|--------|
| **Description** | The system incorrectly fails a compliant bidder due to extraction errors, rule misinterpretation, or stale data. |
| **Probability** | MEDIUM |
| **Impact** | HIGH — Unfair exclusion of qualified bidder; legal challenge |
| **Mitigation** | Human review of all FAIL decisions; officer override capability; mandatory rationale; appeal process |
| **Fallback** | Procurement officer final authority; can override system decision |
| **Status** | MITIGATED BY DESIGN — Human approval is mandatory |

### R18: False Negatives (Incorrect PASS)

| Attribute | Detail |
|-----------|--------|
| **Description** | The system incorrectly passes a non-compliant bidder due to missed documents, undetected fraud, or incomplete verification. |
| **Probability** | MEDIUM |
| **Impact** | HIGH — Unqualified bidder awarded contract; CVC scrutiny |
| **Mitigation** | Multi-source verification; cross-source conflict detection; comprehensive rule evaluation; evidence confidence scoring |
| **Fallback** | Low evidence confidence triggers REVIEW status; officer manually reviews before qualifying |
| **Status** | MITIGATED |

### R19: Over-Reliance on AI

| Attribute | Detail |
|-----------|--------|
| **Description** | Procurement officers may rubber-stamp AI recommendations without independent review. |
| **Probability** | MEDIUM |
| **Impact** | HIGH — Defeats the purpose of human-in-the-loop design |
| **Mitigation** | Mandatory rationale for decisions; UI design that encourages review (not just "approve all"); randomized audit of decisions; training for officers |
| **Fallback** | Management oversight; random audit sampling |
| **Status** | MITIGATED BY DESIGN (UI/UX) |

### R20: SIH Demo Failure

| Attribute | Detail |
|-----------|--------|
| **Description** | Demo environment fails during SIH presentation (API timeout, network issue, rendering bug). |
| **Probability** | LOW-MEDIUM |
| **Impact** | HIGH — Fails to demonstrate the solution |
| **Mitigation** | Pre-computed results available; local mock services; offline fallback; rehearsal; backup laptop; recorded video backup |
| **Fallback** | Pre-recorded video demo as last resort |
| **Status** | PLANNED |

---

## 2. Risk Matrix Summary

| Risk | Probability | Impact | Priority |
|------|------------|--------|----------|
| R01: No Gov APIs | CERTAIN | HIGH | P1 — Architectural decision |
| R05: Hallucination | MEDIUM | CRITICAL | P1 — AI boundary design |
| R11: DPDP Violation | LOW | CRITICAL | P1 — Legal compliance |
| R04: Bad OCR | HIGH | HIGH | P2 — Confidence scoring |
| R08: Rule Errors | MEDIUM | HIGH | P2 — Testing |
| R17: False Positives | MEDIUM | HIGH | P2 — Human override |
| R18: False Negatives | MEDIUM | HIGH | P2 — Multi-source verification |
| R19: Rubber-stamping | MEDIUM | HIGH | P2 — UX design |
| R02: Approval Delays | HIGH | MEDIUM | P3 — Parallel track |
| R06: Prompt Injection | LOW-MEDIUM | HIGH | P3 — Security |
| R20: Demo Failure | LOW-MEDIUM | HIGH | P3 — Preparation |
| R10: Entity Mismatch | MEDIUM | HIGH | P3 — Algorithm design |
| R13: Log Tampering | LOW | CRITICAL | P3 — Architecture |
| R14: Vendor Lock-in | MEDIUM | MEDIUM | P4 — Architecture |
| R09: Stale Data | MEDIUM | MEDIUM | P4 — Cache policy |

---

## 3. Assumptions

| # | Assumption | Confidence | Impact if Wrong | Claim Classification |
|---|-----------|-----------|----------------|----------------------|
| A1 | SIH judges will accept clearly-labelled MOCK integrations | HIGH | Demo perceived as incomplete | ASSUMPTION |
| A2 | Google Gemini API will be available during SIH demo | HIGH | Switch to OpenAI or pre-computed results | ASSUMPTION |
| A3 | CPCL tender documents follow generally standard PSU procurement formats | MEDIUM | May need to handle more document formats | ASSUMPTION |
| A4 | Procurement officers will provide genuine rationale for decisions (not rubber-stamp) | MEDIUM | Over-reliance on AI; auditability weakened | ASSUMPTION |
| A5 | Make in India Order 2017 (amended July 2024) is the currently applicable version | HIGH | Rules may need updating | OFFICIAL_DOCUMENTED |
| A6 | No single authoritative nationwide debarment database covering all relevant procurement entities was confirmed | HIGH | Would simplify debarment checking | CONFIRMED |
| A7 | DigiLocker partner onboarding cannot be completed within SIH timeline | HIGH | Would enable live document verification | ASSUMPTION |
| A8 | GSP sandbox access can potentially be obtained within weeks | MEDIUM | GST verification would be MOCK-only | ASSUMPTION |
| A9 | The team has access to Python/Node.js development environment | HIGH | Would need alternative stack | ASSUMPTION |
| A10 | SIH demo will have internet access for AI API calls | HIGH | Need offline fallback | ASSUMPTION |

