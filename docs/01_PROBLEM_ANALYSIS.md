# 01 — Problem Analysis

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas  
**Department:** Chennai Petroleum Corporation Limited (CPCL)  
**Category:** Software  
**Theme:** Smart Automation  
**Phase:** 0 — Research & Ground Truth  
**Date:** 2026-09-05

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## 1. Problem Statement Summary

CPCL, a subsidiary of Indian Oil Corporation under the Ministry of Petroleum & Natural Gas, procures goods, services, and works through the Government e-Marketplace (GeM) and its own e-procurement portal (via NIC). The current bid evaluation process for compliance verification is **largely manual, document-heavy, and time-consuming**.

Procurement officers must:

1. Read and extract requirements from tender documents (often 50–200+ pages)
2. Receive bidder submissions containing dozens of certificates, declarations, and financial documents
3. Manually verify each document against tender-specific eligibility criteria
4. Cross-reference information across multiple government portals (GST, PAN, MCA, Udyam, etc.)
5. Identify inconsistencies across documents (e.g., PAN on GST certificate vs. PAN on Udyam certificate)
6. Determine compliance with Make in India / local content requirements
7. Check debarment/blacklisting status across fragmented government sources
8. Produce an auditable compliance report
9. Make a final qualification/disqualification decision

### Core Pain Points

| # | Pain Point | Impact | Claim Classification |
|---|-----------|--------|----------------------|
| 1 | Manual extraction of tender requirements | Hours per tender; human error; missed clauses | CONFIRMED |
| 2 | Manual document review per bidder | Days per evaluation cycle; reviewer fatigue | CONFIRMED |
| 3 | No unified government verification interface | Multiple portal logins; CAPTCHA barriers; no suitable public API confirmed for most | CONFIRMED |
| 4 | Inconsistency detection across documents | Missed conflicts; fraud risk | CONFIRMED |
| 5 | Make in India compliance is complex and versioned | Incorrect classification; policy lag | OFFICIAL_DOCUMENTED |
| 6 | No single authoritative nationwide debarment database confirmed | Incomplete blacklist checks | CONFIRMED |
| 7 | Corrigendum / amendment tracking | Missed changes invalidate evaluations | CONFIRMED |
| 8 | Audit trail is paper-based or ad-hoc | Compliance risk; CVC/CAG vulnerability | CONFIRMED |
| 9 | No standardized compliance scoring | Subjective evaluations; inconsistent decisions | CONFIRMED |
| 10 | Every tender has different requirements | Cannot hard-code a single evaluation template | CONFIRMED |


---

## 2. Problem Decomposition (MECE Categories)

### A. Tender Intelligence

| Attribute | Detail |
|-----------|--------|
| **Problem** | Extract and structure requirements from unstructured tender documents (PDF, scanned images, DOCX) |
| **User** | Procurement officer |
| **Input** | Tender document (NIT, BOQ, technical specifications, general conditions, special conditions, annexures) |
| **Processing** | AI-powered document parsing, requirement extraction, clause classification, corrigendum tracking |
| **Output** | Structured requirement checklist with categories (mandatory/preferred), thresholds, and referenced clauses |
| **Failure Cases** | Scanned/image-only PDFs with poor OCR; ambiguous clause language; missed annexure requirements |
| **Security** | Tender documents may be confidential before publication |
| **AI Involvement** | HIGH — NLP extraction, classification, summarization |
| **Deterministic Logic** | Template matching for known requirement patterns; corrigendum version control |
| **Evidence Required** | Source clause reference with page/section number |

### B. Bidder Identity

| Attribute | Detail |
|-----------|--------|
| **Problem** | Establish and verify the legal identity of each bidder entity |
| **User** | Procurement officer, system |
| **Input** | PAN, GSTIN, CIN/LLPIN, Udyam number, entity name, address |
| **Processing** | Identity resolution across multiple registrations; entity name matching; director/partner linkage |
| **Output** | Verified entity profile with cross-referenced identifiers |
| **Failure Cases** | Name mismatches across registrations; merged/demerged entities; shell companies |
| **Security** | PII/business-sensitive data; must be encrypted at rest and in transit |
| **AI Involvement** | MEDIUM — Fuzzy name matching, entity resolution |
| **Deterministic Logic** | PAN format validation; GSTIN structure validation; CIN checksum |
| **Evidence Required** | Government-verified status for each identifier |

### C. Document Intelligence

| Attribute | Detail |
|-----------|--------|
| **Problem** | Process, classify, and extract fields from bidder-submitted documents |
| **User** | System (automated), procurement officer (review) |
| **Input** | Uploaded documents: certificates, balance sheets, declarations, authorization letters, etc. |
| **Processing** | Document classification (type detection), OCR, field extraction, validity checks |
| **Output** | Structured data extracted from each document with confidence scores |
| **Failure Cases** | Poor scan quality; non-standard formats; forged/altered documents; multi-page documents |
| **Security** | Documents may contain PII and trade secrets |
| **AI Involvement** | HIGH — Vision models for OCR, classification, extraction |
| **Deterministic Logic** | Date validity checks; format validation; template matching |
| **Evidence Required** | Extracted value with source location (page, bounding box) and confidence |

### D. Government Verification

| Attribute | Detail |
|-----------|--------|
| **Problem** | Verify bidder claims against authoritative government sources |
| **User** | System (automated where API available), procurement officer (manual fallback) |
| **Input** | Identifiers: PAN, GSTIN, CIN, Udyam number, DIPP number, EPFO code, ESIC code |
| **Processing** | API calls to government systems; response parsing; status interpretation |
| **Output** | Verification result: VERIFIED / NOT_VERIFIED / EXPIRED / ERROR |
| **Failure Cases** | API unavailable; rate limits; approval pending; sandbox-only access; portal changes |
| **Security** | API credentials must be vault-stored; consent may be required |
| **AI Involvement** | LOW — Primarily deterministic |
| **Deterministic Logic** | YES — Status mapping, expiry checks, active/inactive determination |
| **Evidence Required** | API response timestamp, source system, verification status |

### E. Entity Resolution

| Attribute | Detail |
|-----------|--------|
| **Problem** | Link disparate identifiers and records to a single legal entity |
| **User** | System |
| **Input** | Multiple identifiers (PAN, GSTIN, CIN, Udyam, names) from different sources |
| **Processing** | Cross-reference matching; name normalization; address matching |
| **Output** | Unified entity graph with confidence-weighted links |
| **Failure Cases** | Common names; subsidiaries vs. parent companies; consortium bids |
| **Security** | Aggregated identity data is highly sensitive |
| **AI Involvement** | MEDIUM — Fuzzy matching, disambiguation |
| **Deterministic Logic** | PAN-GSTIN linkage (PAN is embedded in GSTIN); CIN structure parsing |
| **Evidence Required** | Match rationale for each link |

### F. Compliance Rules

| Attribute | Detail |
|-----------|--------|
| **Problem** | Evaluate bidder data against tender-specific eligibility rules |
| **User** | System, procurement officer |
| **Input** | Extracted requirements (from A), verified bidder data (from B–E) |
| **Processing** | Rule engine evaluation; threshold comparison; conditional logic |
| **Output** | Per-requirement compliance result (PASS/FAIL/REVIEW/MISSING/NOT_APPLICABLE) |
| **Failure Cases** | Ambiguous rules; missing data; rules that require human judgment |
| **Security** | Rules must be tamper-proof and version-controlled |
| **AI Involvement** | LOW — Rules are deterministic; AI assists only in requirement extraction |
| **Deterministic Logic** | YES — This is the core deterministic layer |
| **Evidence Required** | Rule definition, input values, evaluation trace |

### G. Cross-Verification

| Attribute | Detail |
|-----------|--------|
| **Problem** | Detect inconsistencies across different data sources for the same bidder |
| **User** | System, procurement officer |
| **Input** | All verified and extracted data for a bidder |
| **Processing** | Cross-source comparison (PAN on GST cert vs. PAN on IT return vs. PAN on Udyam); name matching; date consistency |
| **Output** | Conflict alerts with severity classification |
| **Failure Cases** | Legitimate changes (name change after merger); data lag across portals |
| **Security** | Cross-referenced data requires aggregation controls |
| **AI Involvement** | MEDIUM — Anomaly detection, pattern matching |
| **Deterministic Logic** | YES — Exact match checks, date range validation |
| **Evidence Required** | Both conflicting values with their sources |

### H. Risk Scoring

| Attribute | Detail |
|-----------|--------|
| **Problem** | Classify overall bidder risk for procurement officer decision support |
| **User** | Procurement officer |
| **Input** | Compliance results, conflict alerts, verification statuses, evidence confidence |
| **Processing** | Weighted scoring across dimensions; risk categorization |
| **Output** | Multi-dimensional risk profile (not just a single percentage) |
| **Failure Cases** | Over-reliance on score; masking of critical single-point failures |
| **Security** | Scoring model must be transparent and auditable |
| **AI Involvement** | MEDIUM — Weight optimization, anomaly scoring |
| **Deterministic Logic** | YES — Scoring formula must be reproducible |
| **Evidence Required** | Score breakdown with contribution of each factor |

### I. AI Recommendations

| Attribute | Detail |
|-----------|--------|
| **Problem** | Generate human-readable explanations and recommendations |
| **User** | Procurement officer |
| **Input** | Complete evaluation results |
| **Processing** | LLM-powered summarization; natural language explanation generation |
| **Output** | Recommendations with confidence; explanations with evidence citations |
| **Failure Cases** | Hallucination; overconfident recommendations; missing nuance |
| **Security** | Recommendations must never be auto-actioned; must be clearly labelled as AI-generated |
| **AI Involvement** | HIGH — Core AI function |
| **Deterministic Logic** | Validation layer to ensure recommendations don't contradict rule results |
| **Evidence Required** | Citation of source data for every claim in the recommendation |

### J. Evidence Management

| Attribute | Detail |
|-----------|--------|
| **Problem** | Maintain a complete, immutable chain of evidence for every compliance decision |
| **User** | Procurement officer, auditor, management |
| **Input** | All documents, verification responses, extracted data, rule evaluations |
| **Processing** | Hashing, timestamping, linking evidence to decisions |
| **Output** | Evidence chain per bidder per requirement |
| **Failure Cases** | Storage corruption; hash collision (extremely unlikely); incomplete capture |
| **Security** | Evidence must be tamper-evident (append-only, hash-chained) |
| **AI Involvement** | NONE — Purely deterministic |
| **Deterministic Logic** | YES — Hashing, sequencing, integrity verification |
| **Evidence Required** | Self-evident (this IS the evidence system) |

### K. Auditability

| Attribute | Detail |
|-----------|--------|
| **Problem** | Enable complete audit trail for CVC/CAG/internal audit review |
| **User** | Auditor, vigilance officer, management |
| **Input** | All system actions, decisions, user interactions |
| **Processing** | Immutable logging; action attribution; timeline reconstruction |
| **Output** | Complete audit report per tender evaluation |
| **Failure Cases** | Log tampering; incomplete logging; system clock manipulation |
| **Security** | Audit logs must be immutable; segregated access control |
| **AI Involvement** | NONE |
| **Deterministic Logic** | YES |
| **Evidence Required** | Log integrity proof |

### L. Human Decision Workflow

| Attribute | Detail |
|-----------|--------|
| **Problem** | Ensure procurement officer makes the final decision with full context |
| **User** | Procurement officer, approving authority |
| **Input** | AI recommendations, compliance results, evidence, risk scores |
| **Processing** | Decision capture with rationale; multi-level approval if required |
| **Output** | Recorded decision (QUALIFY/DISQUALIFY/SEEK_CLARIFICATION) with officer's rationale |
| **Failure Cases** | Rubber-stamping AI recommendations; insufficient rationale documentation |
| **Security** | Decision must be attributed to an identified, authorized officer |
| **AI Involvement** | NONE — Decision is human-only |
| **Deterministic Logic** | Workflow enforcement (cannot skip mandatory review steps) |
| **Evidence Required** | Officer identity, timestamp, decision, rationale |

### M. Security

| Attribute | Detail |
|-----------|--------|
| **Problem** | Protect sensitive procurement, bidder, and government data |
| **User** | All system users and administrators |
| **Input** | All system data |
| **Processing** | Authentication, authorization, encryption, access control, threat detection |
| **Output** | Secured system operations |
| **Failure Cases** | Credential compromise; insider threat; API key leakage; injection attacks |
| **Security** | THIS IS the security concern |
| **AI Involvement** | LOW — Anomaly detection in access patterns |
| **Deterministic Logic** | YES — RBAC, encryption, session management |
| **Evidence Required** | Security event logs |

### N. Privacy

| Attribute | Detail |
|-----------|--------|
| **Problem** | Comply with DPDP Act 2023 and government data protection requirements |
| **User** | Data principals (bidders), data processors (system), data fiduciaries (CPCL) |
| **Input** | PII, business-sensitive data, government verification data |
| **Processing** | Consent management; data minimization; purpose limitation; retention policies |
| **Output** | Privacy-compliant data handling |
| **Failure Cases** | Consent not obtained; data used beyond stated purpose; retention violation |
| **Security** | Directly linked to security controls |
| **AI Involvement** | LOW — PII detection in documents |
| **Deterministic Logic** | YES — Consent checks, retention enforcement |
| **Evidence Required** | Consent records, processing logs |

### O. Reporting

| Attribute | Detail |
|-----------|--------|
| **Problem** | Generate comprehensive compliance and procurement analytics reports |
| **User** | Procurement officer, management, auditor |
| **Input** | Aggregated evaluation data |
| **Processing** | Report generation, visualization, trend analysis |
| **Output** | Compliance reports, evaluation summaries, analytics dashboards |
| **Failure Cases** | Inaccurate aggregation; stale data; report tampering |
| **Security** | Reports may contain sensitive procurement data |
| **AI Involvement** | LOW — Trend identification, natural language summaries |
| **Deterministic Logic** | YES — Aggregation, calculation |
| **Evidence Required** | Data lineage for reported figures |

### P. Integration Reliability

| Attribute | Detail |
|-----------|--------|
| **Problem** | Handle government API unavailability, rate limits, and changes gracefully |
| **User** | System |
| **Input** | External API responses (or lack thereof) |
| **Processing** | Circuit breaker pattern; retry with backoff; fallback to manual; health monitoring |
| **Output** | Reliable verification results with clear status indicators |
| **Failure Cases** | Cascading failures; silent failures; stale cached data presented as live |
| **Security** | Must not expose internal infrastructure details in error messages |
| **AI Involvement** | NONE |
| **Deterministic Logic** | YES — Circuit breaker, retry logic, timeout management |
| **Evidence Required** | Integration health logs, failure timestamps, fallback activation records |

### Q. Deployment

| Attribute | Detail |
|-----------|--------|
| **Problem** | Deploy the system in a manner suitable for government/PSU use |
| **User** | System administrators, CPCL IT |
| **Input** | System packages, configuration |
| **Processing** | Containerized deployment; environment configuration; scaling |
| **Output** | Running system |
| **Failure Cases** | Misconfiguration; dependency failures; network restrictions in government networks |
| **Security** | Deployment credentials; infrastructure hardening |
| **AI Involvement** | NONE |
| **Deterministic Logic** | YES |
| **Evidence Required** | Deployment logs, health checks |

### R. Monitoring

| Attribute | Detail |
|-----------|--------|
| **Problem** | Continuously monitor system health, performance, and security |
| **User** | System administrators |
| **Input** | System metrics, logs, alerts |
| **Processing** | Threshold monitoring, alerting, dashboarding |
| **Output** | Health status, alerts, performance reports |
| **Failure Cases** | Alert fatigue; monitoring system failure; blind spots |
| **Security** | Monitoring data may reveal system internals |
| **AI Involvement** | LOW — Anomaly detection in metrics |
| **Deterministic Logic** | YES — Threshold alerting |
| **Evidence Required** | Metric history, alert records |

### S. SIH Demonstration

| Attribute | Detail |
|-----------|--------|
| **Problem** | Demonstrate the system effectively in a 5–10 minute SIH demo |
| **User** | SIH judges |
| **Input** | Pre-configured demo data, synthetic tenders and bidders |
| **Processing** | End-to-end workflow demonstration |
| **Output** | Compelling demonstration of capabilities, innovation, and feasibility |
| **Failure Cases** | Demo environment failure; insufficient preparation; time overrun |
| **Security** | Demo must use synthetic/mock data only |
| **AI Involvement** | Demonstrated across multiple stages |
| **Deterministic Logic** | Demonstrated in rule evaluation, compliance scoring |
| **Evidence Required** | Working prototype with realistic scenarios |

---

## 3. Stakeholder Analysis

| Stakeholder | Role | Primary Concern |
|------------|------|-----------------|
| Procurement Officer | Primary user; makes final decisions | Efficiency, accuracy, auditability |
| Tender Committee | Reviews evaluations | Compliance, fairness, defensibility |
| CPCL Management | Oversight | Risk reduction, process improvement |
| Bidders | Submit bids | Fair evaluation, transparency |
| Vigilance/CVC | Audit | Complete audit trail, no tampering |
| CAG | Audit | Financial compliance, process adherence |
| GeM Administration | Platform | Integration compatibility |
| CPCL IT | Operations | Security, deployment, maintenance |
| SIH Judges | Evaluation | Innovation, feasibility, impact |

---

## 4. Scope Boundaries

### In Scope

- Tender requirement extraction and structuring
- Bidder document processing and AI-powered extraction
- Government verification (where APIs exist or can be mocked)
- Cross-source consistency detection
- Compliance rule evaluation engine
- Risk scoring and classification
- AI-generated recommendations with evidence
- Complete audit trail
- Human decision workflow
- SIH demonstration with synthetic data

### Out of Scope

- Bid submission functionality (GeM handles this)
- Payment processing
- Contract management post-award
- Bidder-side tools (this is a buyer-side platform)
- Physical inspection verification
- Real-time GeM integration (no suitable public API confirmed)
- Aadhaar-based biometric verification (legal restrictions)

---

## 5. Core Design Principle

```
AI INTERPRETS → AUTHORIZED SOURCES VERIFY → RULES EVALUATE → EVIDENCE PROVES → HUMAN APPROVES
```

This is a non-negotiable architectural principle. The system is a **decision support tool**, not a decision-making system.
