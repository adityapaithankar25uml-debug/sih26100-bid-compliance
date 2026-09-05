# Phase 1 End-to-End Architectural Traceability Matrix

**Project:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
**Organization:** Ministry of Petroleum & Natural Gas / CPCL
**Phase:** Phase 1 — Architecture & Design
**Task:** Task 12 — Final Architecture Integration, Consistency, Traceability & Implementation Readiness Review
**Document Status:** DESIGN DRAFT / READ-ONLY VALIDATION READY

---

## 1. Executive Summary & Traceability Governance

This document establishes the end-to-end architectural traceability matrix for the SIH26100 platform. It maps the 18 core platform capabilities across every architectural layer established in Tasks 1–11:
1. **Business & Functional Requirement ID**
2. **Authoritative Architecture Task Specification**
3. **Core Architectural Component & Service**
4. **Authoritative Data Model Entity & Tables**
5. **REST / Event Interface & API Endpoints**
6. **Async Workflow DAG & Job Execution State**
7. **Procurement Officer & Admin UI Component**
8. **Security Boundary & AuthZ Control**
9. **Observability Telemetry & Audit Lineage**

The matrix ensures that no requirement is orphaned without concrete architectural representation, and that no architectural component exists without direct requirement traceability.

---

## 2. Global Architectural Axiom Verification

Every trace across this matrix upholds the core architectural axiom:

$$\text{AI INTERPRETS} \longrightarrow \text{AUTHORIZED SOURCES VERIFY} \longrightarrow \text{RULES EVALUATE} \longrightarrow \text{EVIDENCE PROVES} \longrightarrow \text{HUMAN APPROVES}$$

- **AI Interprets:** Generates advisory facts with confidence scores and page/bbox coordinates.
- **Authorized Sources Verify:** Integrates with official government APIs (GSTN, MCA21, CPPP, UDIN, MSME Udyam) to validate credentials.
- **Rules Evaluate:** Executes deterministic Python AST policy rules to evaluate compliance against strict parameters.
- **Evidence Proves:** Bundles facts, verification tokens, and AST calculation traces into immutable, hash-linked `EvidenceRecord` items.
- **Human Approves:** Sole authority granted to Procurement Officers to finalize qualification decisions.

---

## 3. End-to-End Requirements Traceability Matrix

### 3.1 Trace 1: Tender Ingestion & Initialization
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Ingest GeM/CPCL tender document (PDF/NIT) and initialize tender record with metadata. |
| **Architecture Task** | Task 1 (System Arch §3.1), Task 2 (Data Model §4.1), Task 3 (API Contracts §5.1) |
| **Component** | `TenderIngestionService`, `DocumentParsingEngine` |
| **Data Entity** | `Tender`, `TenderVersion`, `SourceDocument` (Type: `TENDER_NIT`) |
| **API / Interface** | `POST /api/v1/tenders/ingest`, `GET /api/v1/tenders/{tender_id}` |
| **Workflow DAG** | `tender_ingestion_dag` (`ingest_nit_pdf` -> `extract_tender_metadata`) |
| **UI Screen** | Tender Ingestion Hub (`/tenders/ingest`), Tender Detail View (`/tenders/{id}`) |
| **Security Control** | RBAC (`TENDER_CREATE`), TLS 1.3 in transit, KMS envelope encryption at rest |
| **Audit & Obs** | `AuditEvent` (`TENDER_INGESTED`), Metric: `gem_tender_ingestion_total` |

---

### 3.2 Trace 2: Tender Requirement Extraction & Structural Mapping
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Parse tender NIT/ATC to extract eligibility criteria, technical requirements, and commercial rules. |
| **Architecture Task** | Task 4 (AI Pipeline §3.2), Task 6 (Rules Engine §4.1), Task 7 (Workflow §5.2) |
| **Component** | `AIRequirementExtractor`, `RequirementNormalizer`, `PolicyCompiler` |
| **Data Entity** | `TenderRequirement`, `RequirementRuleMap`, `ComplianceRule` |
| **API / Interface** | `POST /api/v1/tenders/{id}/extract-requirements`, `GET /api/v1/tenders/{id}/requirements` |
| **Workflow DAG** | `tender_requirement_extraction_dag` (`parse_sections` -> `ai_extract_clauses` -> `compile_ast_rules`) |
| **UI Screen** | Requirement Structuring Workspace (`/tenders/{id}/requirements`) |
| **Security Control** | AI Gateway output validation, strict PII scrubbing, schema enforced via Pydantic |
| **Audit & Obs** | `AuditEvent` (`REQUIREMENTS_EXTRACTED`), Span: `ai_gateway.requirement_extraction` |

---

### 3.3 Trace 3: Tender Versioning & Addendum Management
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Maintain immutability of published tender requirements and support versioned addenda. |
| **Architecture Task** | Task 2 (Data Model §4.2), Task 6 (Rules Engine §7.1), Task 11 (UX Architecture §4.3) |
| **Component** | `TenderVersionManager`, `PolicyVersionController` |
| **Data Entity** | `TenderVersion`, `PolicyVersion`, `TenderRequirementHistory` |
| **API / Interface** | `POST /api/v1/tenders/{id}/versions`, `GET /api/v1/tenders/{id}/versions/{version_id}` |
| **Workflow DAG** | `tender_addendum_processing_dag` (`diff_requirements` -> `freeze_new_policy_version`) |
| **UI Screen** | Tender Version Comparison Matrix (`/tenders/{id}/versions`) |
| **Security Control** | Immutable version semantics; published versions cannot be updated or deleted (`READ_ONLY`) |
| **Audit & Obs** | `AuditEvent` (`TENDER_VERSION_CREATED`), Metric: `tender_version_count` |

---

### 3.4 Trace 4: Bid Submission Package Ingestion
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Receive, register, and store multi-document bidder submission packages submitted via GeM portal. |
| **Architecture Task** | Task 1 (System Arch §3.2), Task 2 (Data Model §5.1), Task 3 (API Contracts §6.1) |
| **Component** | `BidSubmissionIngestionService`, `ObjectStorageGateway` |
| **Data Entity** | `BidSubmission`, `SourceDocument` (Type: `BIDDER_DOCUMENT`), `Bidder` |
| **API / Interface** | `POST /api/v1/bids/submit`, `GET /api/v1/bids/{bid_id}` |
| **Workflow DAG** | `bid_ingestion_dag` (`receive_payload` -> `virus_scan` -> `store_raw_documents`) |
| **UI Screen** | Bid Ingestion Console (`/bids/ingestion`), Bidder Submission List (`/tenders/{id}/bids`) |
| **Security Control** | RBAC (`BID_SUBMIT`), Antivirus scan (`ClamAV`), strict MIME-type validation |
| **Audit & Obs** | `AuditEvent` (`BID_SUBMITTED`), Log: `Bid submission registered with hash SHA256` |

---

### 3.5 Trace 5: Document Ingestion, Parsing & OCR Processing
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Parse uploaded bidder PDFs, apply OCR for scanned documents, extract layout structure and text. |
| **Architecture Task** | Task 4 (AI Pipeline §4.1), Task 7 (Workflow §5.3), Task 8 (Security §6.1) |
| **Component** | `DocumentExtractionPipeline`, `OCREngineAdapter`, `LayoutParser` |
| **Data Entity** | `DocumentExtraction`, `ExtractedFact`, `DocumentPage` |
| **API / Interface** | `POST /api/v1/documents/{id}/process`, `GET /api/v1/documents/{id}/extraction` |
| **Workflow DAG** | `document_processing_dag` (`ocr_pdf` -> `extract_layout` -> `extract_text_blocks`) |
| **UI Screen** | Document Viewer with Bounding Boxes (`/documents/{id}/view`) |
| **Security Control** | Isolated sandbox container parsing; file size limits (100MB max per file) |
| **Audit & Obs** | `AuditEvent` (`DOCUMENT_PROCESSED`), Metric: `document_ocr_duration_seconds` |

---

### 3.6 Trace 6: Document Security, Classification & Sanitization
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Enforce security classification, quarantine suspicious files, produce sanitized derivative documents. |
| **Architecture Task** | Task 8 (Security Architecture §6.2), Task 2 (Data Model §5.3) |
| **Component** | `DocumentSecuritySanitizer`, `PIIRedactor`, `ClassificationEngine` |
| **Data Entity** | `SourceDocument` (`classification_level`, `is_quarantined`), `SanitizedDerivative` |
| **API / Interface** | `GET /api/v1/documents/{id}/sanitized`, `POST /api/v1/documents/{id}/classify` |
| **Workflow DAG** | `document_security_dag` (`scan_malware` -> `scrub_metadata` -> `redact_pii`) |
| **UI Screen** | Document Security & Metadata Panel (`/documents/{id}/security`) |
| **Security Control** | Zero-trust execution, original document isolation, immutable raw storage |
| **Audit & Obs** | `AuditEvent` (`DOCUMENT_SANITIZED`), Log: `PII redacted from document derivative` |

---

### 3.7 Trace 7: AI Information Extraction & Fact Generation
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Use LLM/VLM pipelines to extract structured facts (Turnover, EMD, UDIN, Experience) with provenance. |
| **Architecture Task** | Task 4 (AI Pipeline §5.1), Task 2 (Data Model §6.1), Task 3 (API Contracts §7.1) |
| **Component** | `AIFactExtractor`, `AIGateway`, `SchemaValidator` |
| **Data Entity** | `ExtractedFact` (`fact_type`, `fact_value`, `confidence_score`, `provenance_bbox`) |
| **API / Interface** | `POST /api/v1/bids/{id}/extract-facts`, `GET /api/v1/bids/{id}/facts` |
| **Workflow DAG** | `ai_fact_extraction_dag` (`chunk_document` -> `query_llm_gateway` -> `validate_pydantic_schema`) |
| **UI Screen** | Fact Extraction & Provenance Inspector (`/bids/{id}/facts`) |
| **Security Control** | AI output strictly non-authoritative (`is_authoritative=False`), prompt injection validation |
| **Audit & Obs** | `AuditEvent` (`FACTS_EXTRACTED`), Span: `llm_inference_latency` |

---

### 3.8 Trace 8: External Government API Verification
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Verify extracted facts (GSTIN, CIN, UDIN, Udyam) against live official government databases. |
| **Architecture Task** | Task 5 (Government Integrations §3.1-§3.5), Task 7 (Workflow §6.1) |
| **Component** | `GovIntegrationAdapterFactory`, `GSTNClient`, `MCA21Client`, `UDINClient` |
| **Data Entity** | `GovernmentVerificationRecord` (`verification_status`, `raw_response_hash`) |
| **API / Interface** | `POST /api/v1/verification/verify-fact`, `GET /api/v1/verification/status/{id}` |
| **Workflow DAG** | `government_verification_dag` (`route_adapter` -> `call_gov_api` -> `cache_result`) |
| **UI Screen** | Government Verification Dashboard (`/verification/dashboard`) |
| **Security Control** | Outbound mTLS with Govt Gateways, AES-256 encrypted API keys in vault, circuit breakers |
| **Audit & Obs** | `AuditEvent` (`GOVT_VERIFICATION_COMPLETED`), Metric: `gov_api_response_time_seconds` |

---

### 3.9 Trace 9: Identity Matching & Entity Resolution
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Match bidder legal name, PAN, and GSTIN across submitted documents and government registers. |
| **Architecture Task** | Task 5 (Gov Integrations §5.1), Task 6 (Compliance Engine §5.2) |
| **Component** | `IdentityResolutionEngine`, `FuzzyMatcher`, `NormalizedFactBuilder` |
| **Data Entity** | `NormalizedFact` (`normalized_type`, `normalized_value`, `match_confidence`) |
| **API / Interface** | `POST /api/v1/bids/{id}/resolve-identity`, `GET /api/v1/bids/{id}/identity-status` |
| **Workflow DAG** | `identity_matching_dag` (`fetch_facts` -> `fuzzy_match_legal_name` -> `cross_verify_pan_gstn`) |
| **UI Screen** | Bidder Identity Consistency Matrix (`/bids/{id}/identity`) |
| **Security Control** | Deterministic matching for tax identifiers; fuzzy matching strictly highlighted for officer review |
| **Audit & Obs** | `AuditEvent` (`IDENTITY_MATCHED`), Log: `Identity match score calculated` |

---

### 3.10 Trace 10: Immutable Evidence Record Bundling
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Combine extracted facts, government verification outputs, and document locations into an Evidence Record. |
| **Architecture Task** | Task 2 (Data Model §7.1), Task 6 (Compliance Engine §6.1), Task 8 (Security §7.2) |
| **Component** | `EvidenceRecordBuilder`, `CryptoHashChain` |
| **Data Entity** | `EvidenceRecord` (`evidence_hash`, `source_type`, `verification_status`) |
| **API / Interface** | `GET /api/v1/bids/{id}/evidence`, `GET /api/v1/evidence/{evidence_id}` |
| **Workflow DAG** | `evidence_bundling_dag` (`collect_facts` -> `verify_provenance` -> `compute_sha256_chain`) |
| **UI Screen** | Evidence Provenance Inspector (`/bids/{id}/evidence/{evidence_id}`) |
| **Security Control** | SHA-256 hash chaining of evidence payload; read-only access for evaluation engine |
| **Audit & Obs** | `AuditEvent` (`EVIDENCE_RECORD_BOUND`), Metric: `evidence_records_created_total` |

---

### 3.11 Trace 11: Deterministic Compliance & Policy Rule Evaluation
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Evaluate bidder evidence records against versioned Python AST policy rules to determine rule compliance. |
| **Architecture Task** | Task 6 (Rules Engine §3.1-§6.3), Task 3 (API Contracts §8.1) |
| **Component** | `ComplianceEvaluationEngine`, `ASTRuleExecutor`, `ASTSafetyValidator` |
| **Data Entity** | `ComplianceEvaluation`, `RuleEvaluationDetail` (`status`, `calculation_trace`) |
| **API / Interface** | `POST /api/v1/bids/{id}/evaluate`, `GET /api/v1/bids/{id}/compliance` |
| **Workflow DAG** | `compliance_evaluation_dag` (`load_policy` -> `execute_ast_rules` -> `aggregate_outcomes`) |
| **UI Screen** | Compliance Rule Evaluation Matrix (`/bids/{id}/compliance`) |
| **Security Control** | Restricted Python AST execution environment (no built-in imports, isolated namespace) |
| **Audit & Obs** | `AuditEvent` (`COMPLIANCE_EVALUATED`), Span: `compliance_engine.eval_duration` |

---

### 3.12 Trace 12: Multidimensional Risk Assessment & Scoring
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Compute financial, technical, and red-flag risk scores without overriding deterministic rule outcomes. |
| **Architecture Task** | Task 4 (AI Pipeline §6.2), Task 6 (Rules Engine §8.1), Task 11 (UX Architecture §5.2) |
| **Component** | `RiskAssessmentEngine`, `AnomalyDetector`, `RedFlagEvaluator` |
| **Data Entity** | `RiskAssessment` (`composite_risk_score`, `financial_risk`, `technical_risk`, `flags`) |
| **API / Interface** | `GET /api/v1/bids/{id}/risk`, `POST /api/v1/bids/{id}/recalculate-risk` |
| **Workflow DAG** | `risk_assessment_dag` (`calculate_financial_ratios` -> `scan_blacklists` -> `compute_composite_score`) |
| **UI Screen** | Multidimensional Risk Overview Panel (`/bids/{id}/risk`) |
| **Security Control** | Advisory classification: Risk score MUST NOT independently disqualify a bidder |
| **Audit & Obs** | `AuditEvent` (`RISK_ASSESSED`), Metric: `bid_risk_score_distribution` |

---

### 3.13 Trace 13: Human Review Workspace & Override Governance
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Allow Procurement Officers to inspect evidence, review flags, and register non-destructive rule overrides. |
| **Architecture Task** | Task 11 (UX Architecture §4.1-§4.6), Task 6 (Rules Engine §9.1), Task 2 (Data Model §8.1) |
| **Component** | `HumanReviewWorkspaceManager`, `OverrideGovernanceService` |
| **Data Entity** | `RuleOverrideRecord` (`original_status`, `overridden_status`, `justification_text`) |
| **API / Interface** | `POST /api/v1/bids/{id}/override-rule`, `GET /api/v1/bids/{id}/human-review` |
| **Workflow DAG** | `human_review_workflow` (`flag_for_review` -> `await_officer_input` -> `apply_override`) |
| **UI Screen** | Procurement Officer Human Review Workspace (`/bids/{id}/review`) |
| **Security Control** | Mandatory mandatory text justification (>=50 chars), Dual-control approval for critical rules |
| **Audit & Obs** | `AuditEvent` (`RULE_OVERRIDDEN`), Log: `Officer overridden rule with justification` |

---

### 3.14 Trace 14: Procurement Officer Qualification Decision
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Capture final authoritative Procurement Officer qualification decision (QUALIFIED / DISQUALIFIED / REJECTED). |
| **Architecture Task** | Task 1 (System Arch §4.2), Task 2 (Data Model §8.2), Task 3 (API Contracts §9.1) |
| **Component** | `QualificationDecisionService`, `DecisionSigner` |
| **Data Entity** | `QualificationOutcome`, `OfficerDecision` (`decision`, `remarks`, `signed_timestamp`) |
| **API / Interface** | `POST /api/v1/bids/{id}/finalize-decision`, `GET /api/v1/bids/{id}/decision` |
| **Workflow DAG** | `decision_finalization_dag` (`validate_checklist` -> `record_decision` -> `lock_bid_evaluation`) |
| **UI Screen** | Decision Confirmation & Sign-off Modal (`/bids/{id}/decision/sign`) |
| **Security Control** | RBAC (`PROCUREMENT_OFFICER_DECISION`), Session re-authentication, irreversible state lock |
| **Audit & Obs** | `AuditEvent` (`OFFICER_DECISION_SUBMITTED`), Metric: `officer_decisions_total` |

---

### 3.15 Trace 15: Tamper-Evident Audit Event Logging & Hash Chaining
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Record all system activities in a SHA-256 hash-chained tamper-evident audit log. |
| **Architecture Task** | Task 8 (Security Architecture §7.1), Task 9 (Observability §4.1) |
| **Component** | `AuditEventLogger`, `HashChainCalculator`, `AuditVerifier` |
| **Data Entity** | `AuditEvent` (`sequence_id`, `prev_hash`, `current_hash`, `payload_json`) |
| **API / Interface** | `GET /api/v1/audit/logs`, `POST /api/v1/audit/verify-chain` |
| **Workflow DAG** | Sync interceptor on all write APIs + async background verification worker |
| **UI Screen** | Audit Explorer & Hash Verification Console (`/admin/audit`) |
| **Security Control** | Append-only storage permissions, cryptographic hash verification, zero update/delete routes |
| **Audit & Obs** | System self-audit; Metric: `audit_hash_chain_integrity_status` |

---

### 3.16 Trace 16: Asynchronous Notifications & Alert Dispatch
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Notify officers and administrators of critical workflow state changes, SLA breaches, and high-risk flags. |
| **Architecture Task** | Task 7 (Workflow Orchestration §7.1), Task 9 (Observability §6.1) |
| **Component** | `NotificationDispatcher`, `EmailAdapter`, `WebSocketNotifier` |
| **Data Entity** | `NotificationRecord`, `UserNotificationPreference` |
| **API / Interface** | `GET /api/v1/notifications`, `POST /api/v1/notifications/mark-read`, `WS /api/v1/ws/notifications` |
| **Workflow DAG** | Triggered by Celery event signals (`task_failed`, `sla_warning`, `review_required`) |
| **UI Screen** | Global Header Notification Bell & Real-time Alert Banner |
| **Security Control** | Rate-limited notification queues; sanitization of sensitive content in email body |
| **Audit & Obs** | `AuditEvent` (`NOTIFICATION_SENT`), Metric: `notifications_dispatched_total` |

---

### 3.17 Trace 17: Disaster Recovery & Database Backup Governance
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Guarantee point-in-time recovery (PITR) for PostgreSQL database and cross-region S3 document replication. |
| **Architecture Task** | Task 10 (Deployment & DevOps §8.1-§8.4) |
| **Component** | `AWS RDS Backup Automation`, `S3 Cross-Region Replication Engine` |
| **Data Entity** | All persistent DB tables (`Tender`, `BidSubmission`, `AuditEvent`, `EvidenceRecord`) and S3 objects |
| **API / Interface** | CloudWatch Alarms & AWS Backup Management Consoles |
| **Workflow DAG** | Automated AWS RDS backup job (15-min WAL archiving) + S3 bucket replication policy |
| **UI Screen** | DevOps System Health & DR Monitoring Dashboard (`/admin/system/dr`) |
| **Security Control** | KMS CMK encrypted backups; immutability locks (S3 Object Lock) on backup buckets |
| **Audit & Obs** | Metric: `dr_rpo_lag_seconds`, `dr_rto_estimate_seconds` |

---

### 3.18 Trace 18: Security Event Monitoring & Threat Response
| Trace Dimension | Architectural Mapping |
| :--- | :--- |
| **Requirement** | Monitor failed logins, unauthorized access attempts, prompt injection attacks, and API abuse in real time. |
| **Architecture Task** | Task 8 (Security Architecture §9.1), Task 9 (Observability §5.1) |
| **Component** | `SecurityEventCollector`, `RateLimiter`, `WAFRulesEngine` |
| **Data Entity** | `SecurityEventLog` (SIEM format), `BlockedIPRegistry` |
| **API / Interface** | `GET /api/v1/admin/security-events` |
| **Workflow DAG** | Real-time log streaming from FastAPI middleware -> Prometheus Security Exporter |
| **UI Screen** | Security Operations Dashboard (`/admin/security`) |
| **Security Control** | Automated IP throttling, JWT token revocation, Cloudflare WAF rule triggering |
| **Audit & Obs** | `AuditEvent` (`SECURITY_ALERT_TRIGGERED`), Metric: `security_events_severity_count` |

---

## 4. Traceability Verification & Gap Assessment

1. **Coverage Complete:** All 18 core functional requirements trace directly from high-level architecture tasks down to database entities, API endpoints, Celery DAGs, UI screens, security controls, and telemetry metrics.
2. **Zero Orphan Components:** No Task 1–11 component exists without explicit mapping to a business capability and audit trail.
3. **Axiomatic Consistency:** Every trace maintains strict separation between AI fact extraction, government API verification, AST rule evaluation, evidence record bundling, and human officer decision-making.
