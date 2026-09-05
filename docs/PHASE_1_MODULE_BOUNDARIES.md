# Phase 1 Module Boundaries Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-003  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## Overview

This specification establishes strict architectural boundaries, responsibilities, input/output contracts, dependencies, data ownership, and prohibitions for all **23 required modules** of the SIH 26100 platform.

---

## 1. Authentication & Authorization Module

- **Responsibility:** Manages user authentication (MFA/JWT), session validation, password policies, and Role-Based Access Control (RBAC) permission enforcement.
- **Inputs:** Login credentials, TOTP tokens, JWT bearer tokens, resource access requests.
- **Outputs:** Authenticated User Context, Access/Refresh JWTs, Permission Granted/Denied decisions.
- **Dependencies:** User Management Module, Redis (Session Cache).
- **Data Ownership:** User Credentials, Active Sessions, Refresh Token Registry.
- **MUST NOT DO:** MUST NOT modify tender requirements, evaluate compliance rules, or override officer decisions.

---

## 2. User / Organization Management Module

- **Responsibility:** Manages CPCL organizational hierarchy, department definitions, procurement officer profiles, and role assignments.
- **Inputs:** User registration data, profile updates, department assignments, RBAC role maps.
- **Outputs:** User/Officer Domain Entities, Organization Structure Trees.
- **Dependencies:** Database Storage Engine.
- **Data Ownership:** `users`, `roles`, `departments`, `user_roles` database tables.
- **MUST NOT DO:** MUST NOT store plain-text passwords or bypass RBAC permission checks.

---

## 3. Tender Management Module

- **Responsibility:** Ingests, stores, and manages CPCL tender notices (NIT), BOQ parameters, cover definitions, and corrigenda.
- **Inputs:** Tender PDF/JSON files, corrigenda uploads, officer setup parameters.
- **Outputs:** Structured Tender Entities, Corrigendum Event Triggers.
- **Dependencies:** Document Management Module, Object Storage, Database Storage.
- **Data Ownership:** `tenders`, `tender_documents`, `corrigenda` database tables.
- **MUST NOT DO:** MUST NOT perform AI requirement extraction or evaluate bidder compliance.

---

## 4. Tender Requirement Intelligence Module

- **Responsibility:** Extracts unstructured eligibility criteria from Tender NIT text using AI, classifies categories, and formats typed requirement proposals for officer confirmation.
- **Inputs:** Raw Tender Document Text / PDF streams.
- **Outputs:** Proposed Structured Requirement Entities (Mandatory/Preferred, Thresholds, Source Clauses).
- **Dependencies:** AI Provider Abstraction Module, Tender Management Module.
- **Data Ownership:** `proposed_requirements` database table.
- **MUST NOT DO:** MUST NOT auto-confirm requirements into active tender rules without officer sign-off.

---

## 5. Document Management Module

- **Responsibility:** Handles file upload stream ingestion, file type validation (magic bytes), SHA-256 hashing, virus scanning, and encrypted object storage persistence.
- **Inputs:** File upload streams (PDF, PNG, JPEG, TIFF).
- **Outputs:** Persisted Document Metadata Objects, SHA-256 Hashes, Object Storage URIs.
- **Dependencies:** Object Storage (MinIO / S3).
- **Data Ownership:** `documents`, `document_hashes` database tables.
- **MUST NOT DO:** MUST NOT parse document text content or execute OCR extraction logic.

---

## 6. Document Intelligence Module

- **Responsibility:** Executes document layout analysis, page rendering, OCR text extraction, field extraction, and bounding-box coordinate mapping `[x0, y0, x1, y1]`.
- **Inputs:** Persisted Document Artifacts from Document Management Module.
- **Outputs:** Extracted Field Objects, Bounding-Box Overlay Artifacts, OCR Confidence Scores.
- **Dependencies:** Document Management Module, AI Provider Abstraction Module.
- **Data Ownership:** `extracted_fields`, `bounding_boxes` database tables.
- **MUST NOT DO:** MUST NOT compare extracted numbers against tender rules or compute pass/fail flags.

---

## 7. Bidder Management Module

- **Responsibility:** Manages bidder registration profiles, submitted package manifests, cover separation (Cover 1 Fee/EMD, Cover 2 Techno-Commercial), and contact details.
- **Inputs:** Bidder submission packages, basic identifiers (PAN, GSTIN, CIN, Udyam).
- **Outputs:** Bidder Entities, Cover Manifest Trees.
- **Dependencies:** Database Storage Engine, Document Management Module.
- **Data Ownership:** `bidders`, `bidder_documents`, `cover_manifests` database tables.
- **MUST NOT DO:** MUST NOT execute government verification calls or score bidder eligibility.

---

## 8. Bidder Identity / Entity Resolution Module

- **Responsibility:** Performs multi-factor cross-referencing of PAN, GSTIN, CIN, and Udyam to construct legal entity identity graphs and detect name/address mismatches.
- **Inputs:** Bidder Identifiers, Extracted Registration Metadata.
- **Outputs:** Unified Entity Profile Graph, Identity Discrepancy Alerts.
- **Dependencies:** Bidder Management Module, Government Verification Gateway.
- **Data Ownership:** `entity_graphs`, `identity_discrepancies` database tables.
- **MUST NOT DO:** MUST NOT issue debarment classifications or qualify bidders independently.

---

## 9. Government Verification Gateway Module

- **Responsibility:** Routes verification requests across external adapters, manages runtime modes (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`), enforces rate limits, and caches responses with TTL.
- **Inputs:** Domain Verification Requests (Identifier, Domain, Mode).
- **Outputs:** Standardized Verification Response Payload, Provenance Mode Label.
- **Dependencies:** Government Adapters Module, Redis Cache.
- **Data Ownership:** `verifications`, `verification_cache` database tables.
- **MUST NOT DO:** MUST NOT bypass government approval requirements or present mock responses as live API data.

---

## 10. Government Adapters Module

- **Responsibility:** Encapsulates individual integration logic for GSTN, PAN (Protean), MCA, Udyam, EPFO, ESIC, Startup India, NSIC, CPPP, DigiLocker, and BIS behind `BaseGovernmentAdapter`.
- **Inputs:** Specific Verification Parameters.
- **Outputs:** Raw & Parsed Verification Data Objects.
- **Dependencies:** External APIs (where authorized) / Local Mock Implementations.
- **Data Ownership:** None (Stateless execution layer).
- **MUST NOT DO:** MUST NOT expose internal API tokens or execute web-scraping against government portals.

---

## 11. Compliance Ontology Module

- **Responsibility:** Maintains canonical domain schemas, unit conversions (INR to Cr, days to years), severity definitions, and requirement categorization taxonomies.
- **Inputs:** Raw Metric Values, Unit Identifiers.
- **Outputs:** Normalized Metric Values, Taxonomical Categories.
- **Dependencies:** None.
- **Data Ownership:** Policy & Ontology Schema Registry.
- **MUST NOT DO:** MUST NOT store bidder state or execute rule comparisons.

---

## 12. Deterministic Rule Engine Module

- **Responsibility:** Evaluates normalized bidder metrics against active tender requirement thresholds using pure Python boolean logic and Pydantic validation models.
- **Inputs:** Verified Bidder Metrics + Confirmed Tender Requirement Schemas.
- **Outputs:** Itemized Requirement Evaluation Results (`PASS`, `FAIL`, `REVIEW`, `MISSING`, `EXPIRED`, `CONFLICT`, `NOT_VERIFIED`, `NOT_APPLICABLE`).
- **Dependencies:** Compliance Ontology Module, Tender Management Module.
- **Data Ownership:** `compliance_evaluations`, `rule_execution_traces` database tables.
- **MUST NOT DO:** MUST NOT utilize non-deterministic LLM logic for pass/fail decisions or mathematical comparisons.

---

## 13. Cross-Source Conflict Detection Module

- **Responsibility:** Analyzes data across multiple documents and government verification responses for a single bidder to identify discrepancies (e.g., GST legal name != PAN name).
- **Inputs:** Extracted Document Fields, Verified Government Data Objects.
- **Outputs:** Conflict Alert Objects (Severity: CRITICAL, HIGH, MEDIUM, LOW).
- **Dependencies:** Document Intelligence Module, Government Verification Gateway.
- **Data Ownership:** `conflict_alerts` database table.
- **MUST NOT DO:** MUST NOT auto-resolve conflicts without human officer review.

---

## 14. Risk Engine Module

- **Responsibility:** Aggregates evaluation results, conflict alerts, document expiry flags, and debarment matches into a structured Risk Profile.
- **Inputs:** Compliance Evaluation Results, Conflict Alerts, Debarment Matches.
- **Outputs:** Aggregated Risk Profile, Non-Linear Escalation Alerts.
- **Dependencies:** Deterministic Rule Engine, Cross-Source Conflict Detection Module.
- **Data Ownership:** `risk_profiles` database table.
- **MUST NOT DO:** MUST NOT collapse multi-dimensional analysis into a single percentage score.

---

## 15. Compliance Scoring Module

- **Responsibility:** Computes the Three-Dimensional Compliance Metrics: (1) Compliance Score (0–100), (2) Evidence Confidence (0–100), (3) Risk Score (0–100).
- **Inputs:** Evaluated Requirement Flags, Source Confidence Weights, Severity Matrix.
- **Outputs:** 3D Score Metric Payload.
- **Dependencies:** Deterministic Rule Engine, Risk Engine Module.
- **Data Ownership:** `scoring_metrics` database table.
- **MUST NOT DO:** MUST NOT make the compliance score auto-trigger qualification/disqualification.

---

## 16. AI Explanation / Recommendation Module

- **Responsibility:** Generates human-readable compliance summaries and evidence citations for procurement officer review.
- **Inputs:** Evaluation Trace Records, Extracted Document Snippets.
- **Outputs:** Natural Language Explanation Strings, Suggested Officer Action Cards (labeled as AI-generated).
- **Dependencies:** AI Provider Abstraction Module, Deterministic Rule Engine.
- **Data Ownership:** `ai_explanations` database table.
- **MUST NOT DO:** MUST NOT generate recommendations that contradict deterministic rule engine outputs.

---

## 17. Evidence Ledger Module

- **Responsibility:** Constructs and maintains immutable evidence links connecting every compliance evaluation result to its supporting document page, bounding-box, or API payload.
- **Inputs:** Compliance Result IDs, Document Bounding-Boxes, API Response References.
- **Outputs:** Cryptographically Bound Evidence Chains.
- **Dependencies:** Document Intelligence Module, Government Verification Gateway.
- **Data Ownership:** `evidence_ledger`, `evidence_links` database tables.
- **MUST NOT DO:** MUST NOT allow modification or deletion of evidence links once committed.

---

## 18. Audit Trail Module

- **Responsibility:** Records every system event, document ingestion, API call, rule execution, and human officer decision in an append-only log with SHA-256 hash chaining.
- **Inputs:** System Events, User Interaction Payloads.
- **Outputs:** Immutable Audit Log Entries, Hash Integrity Audit Verification Reports.
- **Dependencies:** All System Modules.
- **Data Ownership:** `audit_logs`, `audit_hash_chain` database tables.
- **MUST NOT DO:** MUST NOT support UPDATE or DELETE operations on audit log records.

---

## 19. Officer Decision Workflow Module

- **Responsibility:** Manages the human decision workbench, displays evidence side-by-side with documents, processes officer manual overrides, and records final qualification decisions (`QUALIFY`, `DISQUALIFY`, `SEEK_CLARIFICATION`).
- **Inputs:** Officer Override Actions, Mandatory Justification Rationale Text, Qualification Choice.
- **Outputs:** Sealed Officer Decision Snapshot.
- **Dependencies:** Evidence Ledger Module, Audit Trail Module, Authentication Module.
- **Data Ownership:** `officer_decisions`, `officer_overrides` database tables.
- **MUST NOT DO:** MUST NOT allow decision recording without mandatory justification rationale.

---

## 20. Reporting Module

- **Responsibility:** Compiles and exports structured evaluation summaries, CVC-compliant audit reports, and bidder compliance matrices in PDF/JSON formats.
- **Inputs:** Tender Evaluation Snapshots, Evidence Chains, Officer Decision Records.
- **Outputs:** Exported Report Artifacts (PDF/JSON).
- **Dependencies:** Officer Decision Workflow Module, Evidence Ledger Module.
- **Data Ownership:** `generated_reports` database table.
- **MUST NOT DO:** MUST NOT export reports with unverified mock data presented as live data.

---

## 21. Notification Subsystem Module

- **Responsibility:** Dispatches async notifications (email, in-app alerts) to procurement officers for pending reviews, corrigendum updates, or system alerts.
- **Inputs:** Notification Event Triggers, Recipient User IDs.
- **Outputs:** Dispatched Message Logs, In-App Alert Records.
- **Dependencies:** User Management Module, Redis Async Queue.
- **Data Ownership:** `notifications` database table.
- **MUST NOT DO:** MUST NOT alter evaluation state or bypass officer workflows.

---

## 22. System Administration Module

- **Responsibility:** Manages global platform settings, integration adapter mode toggles (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`), rate limit parameters, and system health checks.
- **Inputs:** Admin Configuration Form Actions.
- **Outputs:** Updated Global System Configuration.
- **Dependencies:** Authentication & Authorization Module.
- **Data Ownership:** `system_configurations` database table.
- **MUST NOT DO:** MUST NOT allow non-admin users to modify system integration settings.

---

## 23. Configuration / Policy Versioning Module

- **Responsibility:** Stores and versions regulatory compliance policies (Make in India Order 2017/2024 amendments, MSE exemptions, GFR rules) and tender-specific rule configurations.
- **Inputs:** Regulatory Policy Updates, Tender Configuration Schemas.
- **Outputs:** Immutable Versioned Policy Definition Objects.
- **Dependencies:** Compliance Ontology Module.
- **Data Ownership:** `policy_versions`, `tender_configurations` database tables.
- **MUST NOT DO:** MUST NOT overwrite historical policy versions used in past tender evaluations.
