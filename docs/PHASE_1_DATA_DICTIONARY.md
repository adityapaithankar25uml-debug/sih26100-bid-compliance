# Phase 1 Data Dictionary Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-009  
**Version:** 1.1.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines field-level data dictionary attributes, column types, nullability, constraints, data security sensitivity classifications, module ownership, and data lifecycle rules. No SQL DDL scripts, database migrations, or code models are created.

---

## Data Dictionary Table Index

1. [BC-1: organizations (CORE MVP)](#1-organizations)
2. [BC-1: departments (CORE MVP)](#2-departments)
3. [BC-1: users (CORE MVP)](#3-users)
4. [BC-1: roles & user_roles (CORE MVP)](#4-roles--user_roles)
5. [BC-2: tenders (CORE MVP)](#5-tenders)
6. [BC-2: tender_versions (CORE MVP)](#6-tender_versions)
7. [BC-2: tender_cover_definitions (CORE MVP)](#7-tender_cover_definitions)
8. [BC-3: tender_requirements (CORE MVP)](#8-tender_requirements)
9. [BC-3: requirement_rule_maps (CORE MVP)](#9-requirement_rule_maps)
10. [BC-3: compliance_rules (CORE MVP)](#10-compliance_rules)
11. [BC-3: policy_versions (CORE MVP)](#11-policy_versions)
12. [BC-4: bidders (CORE MVP)](#12-bidders)
13. [BC-4: bidder_identities (CORE MVP)](#13-bidder_identities)
14. [BC-4: bid_submissions (CORE MVP)](#14-bid_submissions)
15. [BC-4: submission_covers (CORE MVP)](#15-submission_covers)
16. [BC-5: source_documents (CORE MVP)](#16-source_documents)
17. [BC-5: document_extractions (CORE MVP)](#17-document_extractions)
18. [BC-5: extracted_fields (CORE MVP)](#18-extracted_fields)
19. [BC-5: bounding_boxes (CORE MVP)](#19-bounding_boxes)
20. [BC-6: government_verification_requests (CORE MVP)](#20-government_verification_requests)
21. [BC-6: government_verification_attempts (CORE MVP)](#21-government_verification_attempts)
22. [BC-6: government_verification_results (CORE MVP)](#22-government_verification_results)
23. [BC-7: evidence_records (CORE MVP)](#23-evidence_records)
24. [BC-8: compliance_evaluations (CORE MVP)](#24-compliance_evaluations)
25. [BC-8: qualification_outcomes (CORE MVP)](#25-qualification_outcomes)
26. [BC-8: risk_assessment_profiles (CORE MVP)](#26-risk_assessment_profiles)
27. [BC-8: risk_factor_signals (SUPPORTING MVP)](#27-risk_factor_signals)
28. [BC-9: officer_decisions (CORE MVP)](#28-officer_decisions)
29. [BC-9: manual_overrides (CORE MVP)](#29-manual_overrides)
30. [BC-10: audit_events (CORE MVP)](#30-audit_events)
31. [BC-10: audit_hash_chain_blocks (CORE MVP)](#31-audit_hash_chain_blocks)
32. [BC-11: system_configurations (SUPPORTING MVP)](#32-system_configurations)

---

### 1. `organizations`
- **MVP Classification:** `CORE MVP`
- **Description:** Stores top-level tenant organization entities (e.g., CPCL).
- **Module Owner:** MOD-002 User / Organization Management Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `external_id` | `UUID` | N | Unique | PUBLIC | System Generated | Permanent |
| `org_code` | `VARCHAR(50)` | N | Unique | PUBLIC | Admin Input | Mutable |
| `legal_name` | `VARCHAR(255)`| N | None | PUBLIC | Admin Input | Mutable |
| `created_at` | `TIMESTAMPTZ` | N | Default `NOW()`| INTERNAL | System Clock | Immutable |

---

### 2. `departments`
- **MVP Classification:** `CORE MVP`
- **Description:** Represents departmental hierarchy inside an organization (e.g., CPCL Contracts Dept).
- **Module Owner:** MOD-002 User / Organization Management Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `organization_id` | ULID (`CHAR(26)`) | N | FK `organizations.id`| INTERNAL | Admin Input | Permanent |
| `dept_name` | `VARCHAR(150)`| N | None | PUBLIC | Admin Input | Mutable |
| `dept_code` | `VARCHAR(50)` | N | Unique in Org | PUBLIC | Admin Input | Mutable |
| `created_at` | `TIMESTAMPTZ` | N | Default `NOW()`| INTERNAL | System Clock | Immutable |

---

### 3. `users`
- **MVP Classification:** `CORE MVP`
- **Description:** User profiles for procurement officers and committee auditors. Passwords are NEVER stored in plaintext or reversible encryption; slow dedicated hashing (Argon2id/bcrypt) is enforced.
- **Module Owner:** MOD-001 Authentication & Authorization Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `external_id` | `UUID` | N | Unique | PUBLIC | System Generated | Permanent |
| `username` | `VARCHAR(100)`| N | Unique | CONFIDENTIAL | User Registration | Mutable |
| `email` | `VARCHAR(255)`| N | Unique | RESTRICTED/PII | User Registration | Mutable |
| `password_hash` | `VARCHAR(255)`| N | None | RESTRICTED/PII | Argon2id/bcrypt Hashing | Mutable (Salted) |
| `full_name` | `VARCHAR(150)`| N | None | CONFIDENTIAL | User Registration | Mutable |
| `organization_id` | ULID (`CHAR(26)`) | N | FK `organizations.id`| INTERNAL | Admin Input | Mutable |
| `department_id` | ULID (`CHAR(26)`) | N | FK `departments.id` | INTERNAL | Admin Input | Mutable |
| `is_active` | `BOOLEAN` | N | Default `TRUE` | INTERNAL | Admin Input | Soft-Deletable |
| `created_at` | `TIMESTAMPTZ` | N | Default `NOW()`| INTERNAL | System Clock | Immutable |

---

### 4. `roles` & `user_roles`
- **MVP Classification:** `CORE MVP`
- **Description:** RBAC role definitions and user assignments.
- **Module Owner:** MOD-001 Authentication & Authorization Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `role_code` | `VARCHAR(50)` | N | Unique | PUBLIC | System Config | Immutable |
| `role_name` | `VARCHAR(100)`| N | None | PUBLIC | System Config | Mutable |
| `user_id` | ULID (`CHAR(26)`) | N | FK `users.id` | INTERNAL | Admin Mapping | Composite PK |
| `role_id` | ULID (`CHAR(26)`) | N | FK `roles.id` | INTERNAL | Admin Mapping | Composite PK |

---

### 5. `tenders`
- **MVP Classification:** `CORE MVP`
- **Description:** Parent tender entity representing a published procurement notice.
- **Module Owner:** MOD-003 Tender Management Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `external_id` | `UUID` | N | Unique | PUBLIC | System Generated | Permanent |
| `tender_number` | `VARCHAR(100)`| N | Unique | PUBLIC | GeM / CPCL Upload | Immutable |
| `title` | `TEXT` | N | None | PUBLIC | GeM / CPCL Upload | Mutable |
| `organization_id` | ULID (`CHAR(26)`) | N | FK `organizations.id`| INTERNAL | Officer Input | Permanent |
| `department_id` | ULID (`CHAR(26)`) | N | FK `departments.id` | INTERNAL | Officer Input | Permanent |
| `primary_portal` | `VARCHAR(50)` | N | Check (`GeM`,`NIC`) | PUBLIC | Officer Input | Immutable |
| `status` | `VARCHAR(50)` | N | Check Status Enum | PUBLIC | Workflow Engine | State Managed |
| `created_at` | `TIMESTAMPTZ` | N | Default `NOW()`| INTERNAL | System Clock | Immutable |

---

### 6. `tender_versions`
- **MVP Classification:** `CORE MVP`
- **Description:** Point-in-time versions of a tender notice created upon publication or corrigenda.
- **Module Owner:** MOD-003 Tender Management Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `tender_id` | ULID (`CHAR(26)`) | N | FK `tenders.id` | INTERNAL | System Generated | Immutable |
| `version_number` | `INTEGER` | N | Check `> 0` | PUBLIC | System Increment | Immutable |
| `corrigendum_number`| `VARCHAR(50)`| Y | None | PUBLIC | Corrigendum Upload | Immutable |
| `change_summary` | `TEXT` | Y | None | PUBLIC | Officer Input | Immutable |
| `publication_date` | `TIMESTAMPTZ` | N | None | PUBLIC | Tender NIT Stream | Immutable |
| `submission_deadline`|`TIMESTAMPTZ` | N | None | PUBLIC | Tender NIT Stream | Immutable |
| `is_active` | `BOOLEAN` | N | Default `TRUE` | PUBLIC | Version State | Mutable |

---

### 7. `tender_cover_definitions`
- **MVP Classification:** `CORE MVP`
- **Description:** Cover separation requirements (Cover 1 Fee/EMD, Cover 2 Technical, Cover 3 Financial).
- **Module Owner:** MOD-003 Tender Management Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `tender_version_id`| ULID (`CHAR(26)`) | N | FK `tender_versions.id`| INTERNAL | System Generated | Immutable |
| `cover_number` | `INTEGER` | N | Check `1..4` | PUBLIC | Tender Schema | Immutable |
| `cover_name` | `VARCHAR(100)`| N | None | PUBLIC | Tender Schema | Immutable |
| `cover_type` | `VARCHAR(50)` | N | Check (`FEE`,`TECH`,`FIN`) | PUBLIC | Tender Schema | Immutable |
| `is_mandatory` | `BOOLEAN` | N | Default `TRUE` | PUBLIC | Tender Schema | Immutable |

---

### 8. `tender_requirements`
- **MVP Classification:** `CORE MVP`
- **Description:** Eligibility criteria items defined for a tender version.
- **Module Owner:** MOD-004 Requirement Intelligence Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `tender_version_id`| ULID (`CHAR(26)`) | N | FK `tender_versions.id`| INTERNAL | System Generated | Immutable |
| `requirement_code`| `VARCHAR(100)`| N | Unique in Version | PUBLIC | Rule Extraction | Immutable |
| `category` | `VARCHAR(100)`| N | Taxonomy Enum | PUBLIC | Rule Extraction | Immutable |
| `description` | `TEXT` | N | None | PUBLIC | NIT Clause Text | Immutable |
| `is_mandatory` | `BOOLEAN` | N | Default `TRUE` | PUBLIC | NIT Clause Text | Immutable |
| `applicable_bidder_type`|`VARCHAR(50)`| N | Check (`ALL`,`MSE`,`STARTUP`) | PUBLIC | NIT Clause Text | Immutable |
| `confirmation_status`|`VARCHAR(50)`| N | Check (`PROPOSED`,`CONFIRMED`)| PUBLIC | Officer Workflow | Mutable |

---

### 9. `requirement_rule_maps`
- **MVP Classification:** `CORE MVP`
- **Description:** Junction mapping single requirement to N deterministic compliance rules with priority ordering.
- **Module Owner:** MOD-012 Deterministic Rule Engine Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `tender_requirement_id`|ULID (`CHAR(26)`)|N | FK `tender_requirements.id`| INTERNAL | Rule Mapper | Immutable |
| `compliance_rule_id`| ULID (`CHAR(26)`) | N | FK `compliance_rules.id`| INTERNAL | Rule Mapper | Immutable |
| `rule_priority_order`|`INTEGER` | N | Check `> 0` | PUBLIC | Rule Mapper | Immutable |
| `is_mandatory_for_requirement`|`BOOLEAN`|N | Default `TRUE` | PUBLIC | Rule Mapper | Immutable |

---

### 10. `compliance_rules`
- **MVP Classification:** `CORE MVP`
- **Description:** Deterministic Pydantic/Python rule evaluation specifications.
- **Module Owner:** MOD-012 Deterministic Rule Engine Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `rule_code` | `VARCHAR(100)`| N | Unique | PUBLIC | Policy Registry | Immutable |
| `rule_name` | `VARCHAR(200)`| N | None | PUBLIC | Policy Registry | Immutable |
| `rule_type` | `VARCHAR(50)` | N | Check (`NUMERIC`,`BOOLEAN`,`STRING_MATCH`)| PUBLIC | Engine Registry | Immutable |
| `rule_expression` | `JSONB` | N | Valid Rule Schema | INTERNAL | Engine Registry | Immutable |
| `policy_version_id`| ULID (`CHAR(26)`) | N | FK `policy_versions.id`| INTERNAL | Policy Registry | Immutable |
| `is_deterministic` | `BOOLEAN` | N | Default `TRUE` | INTERNAL | Engine Registry | Immutable |

---

### 11. `policy_versions`
- **MVP Classification:** `CORE MVP`
- **Description:** Immutable regulatory policy versions (e.g., Make in India Order 2017/2024).
- **Module Owner:** MOD-023 Configuration & Policy Versioning Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `policy_code` | `VARCHAR(100)`| N | Unique | PUBLIC | Official Gazette | Immutable |
| `policy_name` | `VARCHAR(255)`| N | None | PUBLIC | Official Gazette | Immutable |
| `version_identifier`|`VARCHAR(50)`| N | None | PUBLIC | Official Gazette | Immutable |
| `effective_date` | `DATE` | N | None | PUBLIC | Gazette Order | Immutable |
| `expiry_date` | `DATE` | Y | None | PUBLIC | Gazette Order | Mutable |

---

### 12. `bidders`
- **MVP Classification:** `CORE MVP`
- **Description:** Master record for bidding vendor legal entities.
- **Module Owner:** MOD-007 Bidder Management Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `external_id` | `UUID` | N | Unique | PUBLIC | System Generated | Permanent |
| `legal_name` | `VARCHAR(255)`| N | None | PUBLIC | GeM Submission | Mutable |
| `entity_type` | `VARCHAR(50)` | N | Check (`COMPANY`,`LLP`,`PARTNERSHIP`,`PROPRIETOR`)| PUBLIC | Registration | Mutable |
| `primary_email` | `VARCHAR(255)`| N | None | CONFIDENTIAL | Registration | Mutable |
| `registered_at` | `TIMESTAMPTZ` | N | Default `NOW()`| INTERNAL | System Clock | Immutable |

---

### 13. `bidder_identities`
- **MVP Classification:** `CORE MVP`
- **Description:** Child registration identifiers (PAN, GSTIN, CIN, Udyam) for a bidder.
- **Module Owner:** MOD-008 Bidder Identity Resolution Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `bidder_id` | ULID (`CHAR(26)`) | N | FK `bidders.id` | INTERNAL | Submission | Permanent |
| `identifier_type` | `VARCHAR(50)` | N | Check (`PAN`,`GSTIN`,`CIN`,`UDYAM`) | PUBLIC | Submission | Mutable |
| `identifier_value` | `VARCHAR(100)`| N | None | CONFIDENTIAL | Submission | Mutable |
| `verification_status`|`VARCHAR(50)`| N | Check (`UNVERIFIED`,`VERIFIED`,`MISMATCH`)| PUBLIC | Govt Gateway | State Managed |

---

### 14. `bid_submissions`
- **MVP Classification:** `CORE MVP`
- **Description:** Bidder's participation submission to a specific tender.
- **Module Owner:** MOD-007 Bidder Management Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `external_id` | `UUID` | N | Unique | PUBLIC | System Generated | Permanent |
| `bidder_id` | ULID (`CHAR(26)`) | N | FK `bidders.id` | INTERNAL | Submission Event | Permanent |
| `tender_id` | ULID (`CHAR(26)`) | N | FK `tenders.id` | INTERNAL | Submission Event | Permanent |
| `tender_version_id`| ULID (`CHAR(26)`) | N | FK `tender_versions.id`| INTERNAL | Submission Event | Permanent |
| `submitted_at` | `TIMESTAMPTZ` | N | Default `NOW()`| PUBLIC | GeM Portal Sync | Immutable |
| `submission_status`|`VARCHAR(50)` | N | Check (`SUBMITTED`,`UNDER_EVALUATION`,`COMPLETED`)| PUBLIC | Workflow | State Managed |

---

### 15. `submission_covers`
- **MVP Classification:** `CORE MVP`
- **Description:** Submitted document container matching tender cover definitions.
- **Module Owner:** MOD-007 Bidder Management Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `bid_submission_id`| ULID (`CHAR(26)`) | N | FK `bid_submissions.id`| INTERNAL | Submission Upload | Permanent |
| `cover_definition_id`|ULID (`CHAR(26)`) | N | FK `tender_cover_definitions.id`| INTERNAL | Submission Upload | Permanent |
| `cover_status` | `VARCHAR(50)` | N | Check (`RECEIVED`,`MISSING`,`PARTIAL`)| PUBLIC | Document Ingest | State Managed |

---

### 16. `source_documents`
- **MVP Classification:** `CORE MVP`
- **Description:** Raw file metadata uploaded by bidders or officers.
- **Module Owner:** MOD-005 Document Management Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `external_id` | `UUID` | N | Unique | PUBLIC | System Generated | Permanent |
| `submission_cover_id`|ULID (`CHAR(26)`) | N | FK `submission_covers.id`| INTERNAL | Upload Event | Permanent |
| `file_name` | `VARCHAR(255)`| N | None | CONFIDENTIAL | Upload Metadata | Immutable |
| `mime_type` | `VARCHAR(100)`| N | Magic Byte Checked | INTERNAL | Validation Engine | Immutable |
| `file_size_bytes` | `BIGINT` | N | Check `> 0` | INTERNAL | System Validation | Immutable |
| `sha256_hash` | `CHAR(64)` | N | Unique | INTERNAL | Cryptographic Hash | Immutable |
| `storage_uri` | `VARCHAR(512)`| N | Encrypted Presigned URI | RESTRICTED | MinIO Storage | Immutable |
| `page_count` | `INTEGER` | Y | None | INTERNAL | PyMuPDF Ingest | Mutable |
| `uploaded_at` | `TIMESTAMPTZ` | N | Default `NOW()`| PUBLIC | System Clock | Immutable |

---

### 17. `document_extractions`
- **MVP Classification:** `CORE MVP`
- **Description:** AI/OCR extraction run metadata for a source document.
- **Module Owner:** MOD-006 Document Intelligence Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `source_document_id`|ULID (`CHAR(26)`) | N | FK `source_documents.id`| INTERNAL | OCR Ingestion Job | Permanent |
| `ai_provider` | `VARCHAR(50)` | N | Check (`GEMINI`,`OPENAI`,`OLLAMA`)| INTERNAL | AI Provider Layer | Immutable |
| `model_name` | `VARCHAR(100)`| N | None | INTERNAL | AI Provider Layer | Immutable |
| `model_version` | `VARCHAR(50)` | N | None | INTERNAL | AI Provider Layer | Immutable |
| `prompt_schema_version`|`VARCHAR(50)`| N | None | INTERNAL | AI Provider Layer | Immutable |
| `extracted_at` | `TIMESTAMPTZ` | N | Default `NOW()`| INTERNAL | System Clock | Immutable |

---

### 18. `extracted_fields`
- **MVP Classification:** `CORE MVP`
- **Description:** Individual fields extracted from document text by OCR.
- **Module Owner:** MOD-006 Document Intelligence Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `document_extraction_id`|ULID (`CHAR(26)`) | N | FK `document_extractions.id`| INTERNAL | OCR Parser | Permanent |
| `field_name` | `VARCHAR(100)`| N | Taxonomical Field | INTERNAL | OCR Schema | Immutable |
| `extracted_value` | `TEXT` | N | None | CONFIDENTIAL | OCR Parser | Immutable |
| `confidence_score`| `FLOAT` | N | Check `0.0..1.0`| INTERNAL | OCR Model | Immutable |
| `page_number` | `INTEGER` | N | Check `>= 1` | INTERNAL | OCR Layout Engine | Immutable |
| `validation_status`|`VARCHAR(50)`| N | Check (`VALIDATED`,`REJECTED`,`UNVERIFIED`)| INTERNAL | Pydantic Schema | State Managed |

---

### 19. `bounding_boxes`
- **MVP Classification:** `CORE MVP`
- **Description:** Visual coordinate overlays `[x0, y0, x1, y1]` for extracted text tokens.
- **Module Owner:** MOD-006 Document Intelligence Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `extracted_field_id`|ULID (`CHAR(26)`) | N | FK `extracted_fields.id`| INTERNAL | OCR Layout Engine | Permanent |
| `x0` | `FLOAT` | N | Normalised `0.0..100.0` | INTERNAL | Layout Parser | Immutable |
| `y0` | `FLOAT` | N | Normalised `0.0..100.0` | INTERNAL | Layout Parser | Immutable |
| `x1` | `FLOAT` | N | Normalised `0.0..100.0` | INTERNAL | Layout Parser | Immutable |
| `y1` | `FLOAT` | N | Normalised `0.0..100.0` | INTERNAL | Layout Parser | Immutable |
| `token_text` | `TEXT` | Y | None | CONFIDENTIAL | Layout Parser | Immutable |

---

### 20. `government_verification_requests`
- **MVP Classification:** `CORE MVP`
- **Description:** Verification lookup jobs dispatched to government adapters.
- **Module Owner:** MOD-009 Government Verification Gateway.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `external_id` | `UUID` | N | Unique | PUBLIC | System Generated | Permanent |
| `bidder_id` | ULID (`CHAR(26)`) | N | FK `bidders.id` | INTERNAL | Gateway Job | Permanent |
| `source_adapter` | `VARCHAR(50)` | N | Adapter Code | INTERNAL | Gateway Router | Immutable |
| `identifier_type` | `VARCHAR(50)` | N | Check (`GSTIN`,`PAN`,`CIN`,`UDYAM`)| INTERNAL | Gateway Router | Immutable |
| `identifier_value`| `VARCHAR(100)`| N | Format Validated | CONFIDENTIAL | Gateway Router | Immutable |
| `requested_mode` | `VARCHAR(50)` | N | Check (`LIVE`,`SANDBOX`,`MOCK`,`MANUAL`)| INTERNAL | System Config | Immutable |
| `requested_at` | `TIMESTAMPTZ` | N | Default `NOW()`| PUBLIC | System Clock | Immutable |

---

### 21. `government_verification_attempts`
- **MVP Classification:** `CORE MVP`
- **Description:** Preserves historical execution attempts, retries, and timeouts for government API calls without overwriting past attempts.
- **Module Owner:** MOD-009 Government Verification Gateway.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `verification_request_id`|ULID (`CHAR(26)`)|N | FK `government_verification_requests.id`| INTERNAL | Adapter Dispatch | Permanent |
| `attempt_number` | `INTEGER` | N | Check `> 0` | PUBLIC | Gateway Counter | Immutable |
| `execution_mode` | `VARCHAR(50)` | N | Check (`LIVE`,`SANDBOX`,`MOCK`,`MANUAL`)| PUBLIC | Gateway Router | Immutable |
| `http_status_code`|`INTEGER` | Y | None | INTERNAL | Gateway Client | Immutable |
| `attempted_at` | `TIMESTAMPTZ` | N | Default `NOW()`| PUBLIC | System Clock | Immutable |
| `error_details` | `TEXT` | Y | None | INTERNAL | Gateway Client | Immutable |

---

### 22. `government_verification_results`
- **MVP Classification:** `CORE MVP`
- **Description:** Provenance-tagged response payload yielded by a successful verification attempt.
- **Module Owner:** MOD-009 Government Verification Gateway.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `attempt_id` | ULID (`CHAR(26)`) | N | FK UK `government_verification_attempts.id`| INTERNAL | Adapter Dispatch | Immutable |
| `status` | `VARCHAR(50)` | N | Check (`VERIFIED`,`NOT_VERIFIED`,`ERROR`)| PUBLIC | Govt Adapter | Immutable |
| `source_authority`|`VARCHAR(150)`| N | Authority Identifier | PUBLIC | Govt Adapter | Immutable |
| `raw_payload` | `JSONB` | N | JSON Payload | CONFIDENTIAL | Govt API / Mock | Immutable |
| `payload_hash` | `CHAR(64)` | N | SHA-256 Hash | INTERNAL | Cryptographic Hash | Immutable |
| `responded_at` | `TIMESTAMPTZ` | N | Default `NOW()`| PUBLIC | Gateway Clock | Immutable |

---

### 23. `evidence_records`
- **MVP Classification:** `CORE MVP`
- **Description:** First-class evidence objects linking requirements to extracted OCR or API payloads.
- **Module Owner:** MOD-017 Evidence Ledger Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `external_id` | `UUID` | N | Unique | PUBLIC | System Generated | Permanent |
| `tender_requirement_id`|ULID (`CHAR(26)`)|N | FK `tender_requirements.id`| INTERNAL | Evidence Generator | Immutable |
| `bid_submission_id`| ULID (`CHAR(26)`) | N | FK `bid_submissions.id` | INTERNAL | Evidence Generator | Immutable |
| `extracted_field_id`|ULID (`CHAR(26)`) | Y | FK `extracted_fields.id`| INTERNAL | Evidence Generator | Immutable |
| `verification_result_id`|ULID (`CHAR(26)`)|Y | FK `government_verification_results.id`| INTERNAL | Evidence Generator | Immutable |
| `evidence_type` | `VARCHAR(50)` | N | Check (`DOCUMENT_OCR`,`GOVT_API`,`MANUAL_PROOF`)| PUBLIC | Evidence Generator | Immutable |
| `verification_mode`|`VARCHAR(50)` | N | Check (`LIVE`,`SANDBOX`,`MOCK`,`MANUAL`)| PUBLIC | Provenance Tag | Immutable |
| `evidence_summary`| `TEXT` | N | Summary Text | PUBLIC | Evidence Generator | Immutable |
| `evidence_sha256` | `CHAR(64)` | N | Unique SHA-256 | INTERNAL | Cryptographic Hash | Immutable |
| `created_at` | `TIMESTAMPTZ` | N | Default `NOW()`| PUBLIC | System Clock | Immutable |

---

### 24. `compliance_evaluations`
- **MVP Classification:** `CORE MVP`
- **Description:** Deterministic requirement-level rule evaluation results.
- **Module Owner:** MOD-012 Deterministic Rule Engine Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `bid_submission_id`| ULID (`CHAR(26)`) | N | FK `bid_submissions.id` | INTERNAL | Rule Engine Job | Permanent |
| `tender_requirement_id`|ULID (`CHAR(26)`)|N | FK `tender_requirements.id`| INTERNAL | Rule Engine Job | Permanent |
| `evidence_record_id`|ULID (`CHAR(26)`)|N | FK `evidence_records.id` | INTERNAL | Rule Engine Job | Permanent |
| `compliance_status`|`VARCHAR(50)` | N | Check (`PASS`,`FAIL`,`REVIEW`,`MISSING`,`EXPIRED`,`CONFLICT`)| PUBLIC | Rule Engine | State Managed |
| `is_mandatory` | `BOOLEAN` | N | Default `TRUE` | PUBLIC | Requirement Schema | Immutable |
| `execution_trace` | `JSONB` | N | Trace Logs | INTERNAL | Rule Engine | Immutable |

---

### 25. `qualification_outcomes`
- **MVP Classification:** `CORE MVP`
- **Description:** Overall bidder qualification outcome summary for a submission.
- **Module Owner:** MOD-015 Compliance Scoring & Evaluation Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `bid_submission_id`| ULID (`CHAR(26)`) | N | FK UK `bid_submissions.id`| INTERNAL | Scoring Evaluator | State Managed |
| `outcome_status` | `VARCHAR(50)` | N | Check (`COMPLIANT`,`NOT_COMPLIANT`,`PROVISIONAL`)| PUBLIC | Scoring Evaluator | State Managed |
| `total_mandatory_requirements`|`INTEGER`|N| Check `>= 0` | PUBLIC | Scoring Evaluator | State Managed |
| `passed_mandatory_requirements`|`INTEGER`|N| Check `>= 0` | PUBLIC | Scoring Evaluator | State Managed |
| `failed_mandatory_requirements`|`INTEGER`|N| Check `>= 0` | PUBLIC | Scoring Evaluator | State Managed |

---

### 26. `risk_assessment_profiles`
- **MVP Classification:** `CORE MVP`
- **Description:** Independent analytical risk assessment for a bidder submission.
- **Module Owner:** MOD-014 Risk Engine Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `bid_submission_id`| ULID (`CHAR(26)`) | N | FK UK `bid_submissions.id`| INTERNAL | Risk Engine Job | State Managed |
| `overall_risk_score`|`FLOAT` | N | Check `0.0..100.0` | PUBLIC | Risk Engine Job | State Managed |
| `risk_level` | `VARCHAR(50)` | N | Check (`LOW`,`MEDIUM`,`HIGH`,`CRITICAL`)| PUBLIC | Risk Engine Job | State Managed |
| `confidence_rating`| `FLOAT` | N | Check `0.0..1.0` | PUBLIC | Risk Engine Job | State Managed |

---

### 27. `risk_factor_signals`
- **MVP Classification:** `SUPPORTING MVP`
- **Description:** Child risk breakdown signals (data conflicts, verification failures, anomalies).
- **Module Owner:** MOD-014 Risk Engine Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `risk_profile_id` | ULID (`CHAR(26)`) | N | FK `risk_assessment_profiles.id`| INTERNAL | Risk Evaluator | Permanent |
| `factor_category` | `VARCHAR(100)`| N | Factor Type Enum | PUBLIC | Conflict Detection | Immutable |
| `factor_name` | `VARCHAR(150)`| N | Signal Name | PUBLIC | Risk Evaluator | Immutable |
| `severity` | `VARCHAR(50)` | N | Check (`LOW`,`MEDIUM`,`HIGH`,`CRITICAL`)| PUBLIC | Risk Evaluator | Immutable |
| `score_contribution`|`FLOAT` | N | Check `>= 0.0` | INTERNAL | Risk Evaluator | Immutable |

---

### 28. `officer_decisions`
- **MVP Classification:** `CORE MVP`
- **Description:** Sealed final qualification decision recorded by a named procurement officer.
- **Module Owner:** MOD-019 Officer Decision Workflow Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `external_id` | `UUID` | N | Unique | PUBLIC | System Generated | Permanent |
| `bid_submission_id`| ULID (`CHAR(26)`) | N | FK `bid_submissions.id` | INTERNAL | Officer Action | Immutable |
| `officer_user_id` | ULID (`CHAR(26)`) | N | FK `users.id` | RESTRICTED | Authenticated Officer| Immutable |
| `decision_choice` | `VARCHAR(50)` | N | Check (`QUALIFY`,`DISQUALIFY`,`SEEK_CLARIFICATION`)| PUBLIC | Officer Form | Immutable |
| `justification_rationale`|`TEXT` | N | Non-Empty Rationale | PUBLIC | Officer Form | Immutable |
| `snapshot_hash` | `CHAR(64)` | N | SHA-256 Unique | INTERNAL | Cryptographic Seal | Immutable |

---

### 29. `manual_overrides`
- **MVP Classification:** `CORE MVP`
- **Description:** Itemized status overrides performed by officers during evaluation review.
- **Module Owner:** MOD-019 Officer Decision Workflow Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `officer_decision_id`|ULID (`CHAR(26)`)|N | FK `officer_decisions.id`| INTERNAL | Override Action | Immutable |
| `compliance_evaluation_id`|ULID (`CHAR(26)`)|N| FK `compliance_evaluations.id`| INTERNAL | Override Action | Immutable |
| `previous_status` | `VARCHAR(50)` | N | Status Enum | PUBLIC | System State | Immutable |
| `overridden_status`|`VARCHAR(50)` | N | Status Enum | PUBLIC | Officer Choice | Immutable |
| `override_reason` | `TEXT` | N | Mandatory Text | PUBLIC | Officer Rationale | Immutable |

---

### 30. `audit_events`
- **MVP Classification:** `CORE MVP`
- **Description:** Raw application audit events captured before hash-chain sealing.
- **Module Owner:** MOD-018 Audit Trail Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `correlation_id` | `UUID` | N | Trace Identifier | INTERNAL | Middleware Tracer | Immutable |
| `actor_user_id` | ULID (`CHAR(26)`) | Y | FK `users.id` | CONFIDENTIAL | Auth Context | Immutable |
| `action_type` | `VARCHAR(100)`| N | Event Action Code | PUBLIC | Application Event | Immutable |
| `entity_name` | `VARCHAR(100)`| N | Target Entity | PUBLIC | Application Event | Immutable |
| `entity_id` | `VARCHAR(100)`| N | Target Identifier | PUBLIC | Application Event | Immutable |
| `payload_snapshot` | `JSONB` | N | Sanitized Payload | CONFIDENTIAL | Application Event | Immutable |
| `timestamp` | `TIMESTAMPTZ` | N | Default `NOW()`| PUBLIC | System Clock | Immutable |

---

### 31. `audit_hash_chain_blocks`
- **MVP Classification:** `CORE MVP`
- **Description:** Sealed SHA-256 hash blocks forming a tamper-evident audit chain.
- **Module Owner:** MOD-018 Audit Trail Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `audit_event_id` | ULID (`CHAR(26)`) | N | FK UK `audit_events.id`| INTERNAL | Hash Sealer Job | Immutable |
| `block_sequence` | `BIGINT` | N | Unique Monotonic | PUBLIC | Hash Sealer Job | Immutable |
| `previous_block_hash`|`CHAR(64)` | N | SHA-256 Hash | INTERNAL | Previous Hash Block | Immutable |
| `current_block_hash`| `CHAR(64)` | N | Unique SHA-256 | INTERNAL | Hash Sealer Job | Immutable |
| `sealed_at` | `TIMESTAMPTZ` | N | Default `NOW()`| PUBLIC | System Clock | Immutable |

---

### 32. `system_configurations`
- **MVP Classification:** `SUPPORTING MVP`
- **Description:** System parameters and government adapter mode routing configurations.
- **Module Owner:** MOD-022 System Administration Module.

| Field Name | Data Type | Null | Constraints | Sensitivity | Data Source | Lifecycle Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | ULID (`CHAR(26)`) | N | Primary Key | INTERNAL | System Generated | Permanent |
| `config_key` | `VARCHAR(100)`| N | Unique | PUBLIC | Admin Input | Mutable |
| `config_payload` | `JSONB` | N | Configuration Schema| RESTRICTED | Admin Input | Mutable |
| `description` | `TEXT` | Y | None | PUBLIC | Admin Input | Mutable |
| `updated_at` | `TIMESTAMPTZ` | N | Default `NOW()`| PUBLIC | System Clock | Mutable |
| `updated_by_user_id`|ULID (`CHAR(26)`)|N | FK `users.id` | CONFIDENTIAL | Auth Context | Mutable |
