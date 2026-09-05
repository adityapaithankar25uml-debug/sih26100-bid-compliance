# 03 — Non-Functional Requirements

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05

---

## NFR-01: Performance

| Requirement | Target | Rationale |
|-------------|--------|-----------|
| Tender document processing (100-page PDF) | < 60 seconds | Officer should not wait excessively |
| Single document classification | < 5 seconds | Near-real-time feedback during upload |
| Field extraction per document | < 15 seconds | Batch processing acceptable |
| Government API verification call | < 10 seconds (with timeout at 30s) | External dependency; must handle gracefully |
| Compliance rule evaluation (all rules, one bidder) | < 5 seconds | Deterministic rules should be fast |
| Full tender evaluation report generation | < 30 seconds | Post-processing acceptable |
| Dashboard page load | < 3 seconds | Standard web performance |
| Concurrent users supported | 20+ (for SIH demo: 5) | CPCL-scale procurement office |

---

## NFR-02: Scalability

| Requirement | Detail |
|-------------|--------|
| Tenders per instance | 100+ active tenders |
| Bidders per tender | 50+ bidders |
| Documents per bidder | 30+ documents |
| Verification integrations | 15+ government sources |
| Concurrent evaluations | Multiple tenders evaluated simultaneously |

---

## NFR-03: Availability

| Requirement | Detail |
|-------------|--------|
| Target uptime | 99.5% (for production; SIH demo is best-effort) |
| Graceful degradation | System must continue operating when external APIs are unavailable |
| Offline capability | Core evaluation must work without internet (using cached/mock data) |

---

## NFR-04: Security

| Requirement | Detail |
|-------------|--------|
| Authentication | Multi-factor authentication for procurement officers |
| Authorization | Role-based access control (RBAC) with least-privilege principle |
| Data encryption at rest | AES-256 or equivalent |
| Data encryption in transit | TLS 1.2+ |
| API credential storage | Secrets vault (not environment variables or config files) |
| Session management | Secure session tokens with configurable timeout |
| Input validation | All inputs sanitized against injection attacks |
| File upload security | Malware scanning; file type validation; size limits |
| Audit log protection | Append-only; separated from application logs |
| DPDP Act 2023 compliance | Consent management; data minimization; purpose limitation |

---

## NFR-05: Reliability

| Requirement | Detail |
|-------------|--------|
| Data durability | No data loss for uploaded documents or evaluation results |
| Transaction integrity | ACID compliance for critical operations (decisions, evidence storage) |
| Error recovery | Automatic retry for transient failures; manual recovery for persistent failures |
| Backup | Regular automated backups of all persistent data |

---

## NFR-06: Usability

| Requirement | Detail |
|-------------|--------|
| Target user | Procurement officers (government employees, not necessarily tech-savvy) |
| Interface language | English (Hindi support as future enhancement) |
| Accessibility | WCAG 2.1 AA compliance (recommended) |
| Learning curve | Operable with < 2 hours training |
| Error messages | Clear, actionable, non-technical error messages |
| Help | Contextual help and tooltips for key features |

---

## NFR-07: Maintainability

| Requirement | Detail |
|-------------|--------|
| Code modularity | Separation of concerns: API layer, business logic, data access, AI services |
| Configuration | Environment-based configuration; no hard-coded values |
| Rule updates | Compliance rules updatable without code deployment |
| Policy versioning | Make in India and other policies versioned and auditable |
| Documentation | API documentation (OpenAPI/Swagger); user guide; admin guide |

---

## NFR-08: Integration

| Requirement | Detail |
|-------------|--------|
| Integration pattern | Adapter pattern for each government integration (LIVE/SANDBOX/MOCK/MANUAL) |
| API standards | RESTful APIs with JSON payloads |
| Error handling | Standardized error response format across all integrations |
| Rate limiting | Client-side rate limiting to respect government API limits |
| Circuit breaker | Automatic circuit breaking for failing integrations |
| Health check | Per-integration health status monitoring |

---

## NFR-09: Auditability

| Requirement | Detail |
|-------------|--------|
| Every action logged | No silent operations; every state change recorded |
| Log immutability | Append-only storage; hash-chaining recommended |
| Log retention | Minimum 7 years (government procurement record requirements) |
| Log searchability | Full-text search across audit logs |
| Report generation | One-click audit report per tender evaluation |

---

## NFR-10: Compliance (Regulatory)

| Requirement | Detail |
|-------------|--------|
| DPDP Act 2023 | Data processing consent; purpose limitation; data minimization |
| IT Act 2000 | Information security practices |
| GFR 2017 | General Financial Rules compliance for procurement |
| CVC Guidelines | Transparency and integrity in procurement |
| GeM GTC | General Terms & Conditions of GeM (where applicable) |
| Make in India Order 2017 (amended 2024) | Local content compliance framework |

---

## NFR-11: AI Model Requirements

| Requirement | Detail |
|-------------|--------|
| Explainability | All AI outputs must include reasoning/evidence trail |
| Confidence scoring | Every extraction and classification must have a confidence score |
| Hallucination mitigation | Grounding in source documents; cross-validation; confidence thresholds |
| Prompt injection protection | Input sanitization; output validation; sandboxed execution |
| Model versioning | Track which model version produced each output |
| Bias detection | Monitor for systematic bias in document classification or recommendations |
| Human override | All AI outputs must be reviewable and overridable by authorized officers |

---

## NFR-12: Deployment

| Requirement | Detail |
|-------------|--------|
| Containerization | Docker containers for all services |
| Orchestration | Docker Compose (SIH demo); Kubernetes (production-ready) |
| Environment parity | Dev, staging, and production environments must be consistent |
| Configuration management | Environment variables; secrets vault integration |
| Health endpoints | /health and /ready endpoints for all services |
