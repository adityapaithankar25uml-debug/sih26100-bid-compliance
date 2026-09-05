# Phase 1 API Contracts & Interface Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-013  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines technical API contracts, endpoint parameters, JSON schemas, header requirements, and provenance metadata specifications. No FastAPI routers, controllers, frontend API clients, database migrations, or backend source files are created.

---

## Resource Area Index (23 Resource Areas)

- [A. Authentication & Session Management](#a-authentication--session-management)
- [B. Users, Roles, & Organizations](#b-users-roles--organizations)
- [C. Tenders](#c-tenders)
- [D. Tender Versions](#d-tender-versions)
- [E. Tender Requirements](#e-tender-requirements)
- [F. Compliance Rules & Policy Versions](#f-compliance-rules--policy-versions)
- [G. Bidders](#g-bidders)
- [H. Bid Submissions](#h-bid-submissions)
- [I. Source Documents](#i-source-documents)
- [J. Document Extraction & Extracted Fields](#j-document-extraction--extracted-fields)
- [K. Government Verification Requests](#k-government-verification-requests)
- [L. Government Verification Attempts](#l-government-verification-attempts)
- [M. Government Verification Results](#m-government-verification-results)
- [N. Evidence Records](#n-evidence-records)
- [O. Compliance Evaluations](#o-compliance-evaluations)
- [P. Risk Assessments & Risk Factor Signals](#p-risk-assessments--risk-factor-signals)
- [Q. Qualification Outcomes](#q-qualification-outcomes)
- [R. Officer Decisions](#r-officer-decisions)
- [S. Manual Overrides](#s-manual-overrides)
- [T. Audit Events](#t-audit-events)
- [U. Audit Hash-Chain Information](#u-audit-hash-chain-information)
- [V. Reports](#v-reports)
- [W. Long-Running Jobs & Status](#w-long-running-jobs--status)

---

### A. Authentication & Session Management

#### `POST /api/v1/auth/login`
- **Purpose:** Authenticates user credentials and returns JWT bearer tokens.
- **Roles:** Anonymous (Public)
- **Headers:** `Content-Type: application/json`
- **Request Body:**
  ```json
  {
    "username": "procurement_officer_cpcl",
    "password": "<SECRET_PLAINTEXT_PASS>"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "access_token": "eyJhbGciOiJKV1QiLC...",
    "token_type": "Bearer",
    "expires_in": 1800,
    "user": {
      "user_id": "01HZX89J4K2P00000000000001",
      "username": "procurement_officer_cpcl",
      "role": "PROCUREMENT_OFFICER",
      "organization_code": "CPCL"
    }
  }
  ```
- **Audit Behavior:** Emits `USER_LOGIN_SUCCESS` or `USER_LOGIN_FAILED` audit log event.

---

### B. Users, Roles, & Organizations

#### `GET /api/v1/users`
- **Purpose:** Lists organizational users and officer profiles.
- **Roles:** `SUPER_ADMIN`, `PROCUREMENT_ADMIN`
- **Query Params:** `page=1&limit=20&role=PROCUREMENT_OFFICER`
- **Response `200 OK`:** Returns paginated array of user profile objects.

---

### C. Tenders

#### `POST /api/v1/tenders`
- **Purpose:** Ingests new GeM / CPCL tender notice notice (NIT).
- **Roles:** `PROCUREMENT_ADMIN`, `PROCUREMENT_OFFICER`
- **Headers:** `X-Idempotency-Key: <ULID_KEY>`
- **Request Body:**
  ```json
  {
    "tender_number": "CPCL/2026/NIT/0842",
    "title": "Supply and Installation of Industrial Valves",
    "organization_id": "01HZX89J4K2P00000000000010",
    "department_id": "01HZX89J4K2P00000000000011",
    "primary_portal": "GeM"
  }
  ```
- **Response `201 Created`:** Returns created tender representation with `external_id` (UUIDv4).

---

### D. Tender Versions

#### `GET /api/v1/tenders/{tender_id}/versions`
- **Purpose:** Retrieves all publication versions and corrigenda history for a tender.
- **Roles:** All Authenticated Roles

---

### E. Tender Requirements

#### `GET /api/v1/tender-versions/{version_id}/requirements`
- **Purpose:** Retrieves confirmed eligibility criteria requirements for a tender version.
- **Roles:** All Authenticated Roles

#### `POST /api/v1/tender-versions/{version_id}/requirements/confirm`
- **Purpose:** Officer manual confirmation of AI-extracted requirement proposals.
- **Roles:** `PROCUREMENT_OFFICER`
- **Request Body:**
  ```json
  {
    "confirmed_requirements": [
      {
        "requirement_code": "REQ-TURNOVER-01",
        "category": "FINANCIAL_TURNOVER",
        "description": "Average annual turnover >= INR 50 Crores over last 3 financial years",
        "is_mandatory": true,
        "applicable_bidder_type": "ALL",
        "compliance_rule_id": "01HZX89J4K2P00000000000088"
      }
    ]
  }
  ```

---

### F. Compliance Rules & Policy Versions

#### `GET /api/v1/rules`
- **Purpose:** Lists available deterministic Pydantic compliance rules and linked policy versions.
- **Roles:** All Authenticated Roles

---

### G. Bidders

#### `GET /api/v1/bidders/{bidder_id}`
- **Purpose:** Retrieves master profile for a bidding entity.
- **Roles:** All Authenticated Roles

---

### H. Bid Submissions

#### `GET /api/v1/tenders/{tender_id}/submissions`
- **Purpose:** Lists all bidder submission packages for a tender.
- **Roles:** `PROCUREMENT_OFFICER`, `AUDITOR`

---

### I. Source Documents

#### `POST /api/v1/submissions/{submission_id}/documents/upload`
- **Purpose:** Initiates encrypted document upload to MinIO.
- **Roles:** `PROCUREMENT_OFFICER`, `PROCUREMENT_ADMIN`
- **Response `202 Accepted`:** Dispatches background virus check & SHA-256 hash generation task.

---

### J. Document Extraction & Extracted Fields

#### `POST /api/v1/documents/{doc_id}/extract`
- **Purpose:** Dispatches background OCR parsing & AI field extraction job.
- **Roles:** `PROCUREMENT_OFFICER`
- **Headers:** `X-Idempotency-Key: <KEY>`
- **Response `202 Accepted`:** Returns job status URL `/api/v1/jobs/{job_id}`.

#### `GET /api/v1/extractions/{extraction_id}`
- **Purpose:** Fetches extracted field key-value pairs and bounding box coordinates `[x0, y0, x1, y1]`.
- **Response `200 OK`:**
  ```json
  {
    "extraction_id": "01HZX89J4K2P00000000000200",
    "source_document_id": "01HZX89J4K2P00000000000150",
    "ai_provider": "OLLAMA",
    "model_name": "Qwen 2.5 3B",
    "extracted_fields": [
      {
        "field_id": "01HZX89J4K2P00000000000201",
        "field_name": "annual_turnover_fy24",
        "extracted_value": "650000000",
        "confidence_score": 0.94,
        "page_number": 3,
        "bounding_box": {"x0": 12.5, "y0": 44.0, "x1": 88.0, "y1": 48.5}
      }
    ]
  }
  ```

---

### K. Government Verification Requests

#### `POST /api/v1/verifications/request`
- **Purpose:** Dispatches a verification job to a government adapter.
- **Roles:** `PROCUREMENT_OFFICER`
- **Request Body:**
  ```json
  {
    "bidder_id": "01HZX89J4K2P00000000000050",
    "source_adapter": "GSTNAdapter",
    "identifier_type": "GSTIN",
    "identifier_value": "33AAAAA0000A1Z5",
    "requested_mode": "LIVE"
  }
  ```
- **Response `202 Accepted`:** Triggers background verification lookup attempt.

---

### L. Government Verification Attempts

#### `GET /api/v1/verifications/requests/{request_id}/attempts`
- **Purpose:** Retrieves historical verification execution attempts (retries, timeouts, failures).
- **Roles:** `PROCUREMENT_OFFICER`, `AUDITOR`

---

### M. Government Verification Results

#### `GET /api/v1/verifications/results/{result_id}`
- **Purpose:** Retrieves provenance-tagged verification response payload.
- **Response `200 OK`:**
  ```json
  {
    "result_id": "01HZX89J4K2P00000000000300",
    "status": "VERIFIED",
    "provenance_tag": "[LIVE_VERIFIED]",
    "execution_mode": "LIVE",
    "source_authority": "developer.gst.gov.in (GSP API)",
    "payload_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "raw_payload": {
      "gstin": "33AAAAA0000A1Z5",
      "trade_name": "ABC CPCL SUPPLIERS PRIVATE LIMITED",
      "status": "Active"
    },
    "responded_at": "2026-09-05T23:35:00.000Z"
  }
  ```

---

### N. Evidence Records

#### `GET /api/v1/bid-submissions/{submission_id}/evidence`
- **Purpose:** Fetches first-class evidence records proving compliance.
- **Response `200 OK`:** Answers *"What evidence caused this requirement to PASS/FAIL?"*.
  ```json
  {
    "evidence_id": "01HZX89J4K2P00000000000400",
    "requirement_code": "REQ-TURNOVER-01",
    "evidence_type": "DOCUMENT_OCR",
    "provenance_tag": "[MANUAL_VERIFIED]",
    "document_reference": {
      "file_name": "CA_Turnover_Certificate.pdf",
      "page_number": 3,
      "bounding_box": {"x0": 12.5, "y0": 44.0, "x1": 88.0, "y1": 48.5}
    },
    "evidence_sha256": "4c9a72b1d... (Immutable Hash)",
    "created_at": "2026-09-05T23:36:00.000Z"
  }
  ```

---

### O. Compliance Evaluations

#### `POST /api/v1/bid-submissions/{submission_id}/evaluate`
- **Purpose:** Triggers deterministic Python rule engine evaluation run.
- **Roles:** `PROCUREMENT_OFFICER`

---

### P. Risk Assessments & Risk Factor Signals

#### `GET /api/v1/bid-submissions/{submission_id}/risk-profile`
- **Purpose:** Fetches independent analytical risk score (0.0 to 100.0) and anomaly signals.
- **Roles:** `PROCUREMENT_OFFICER`, `AUDITOR`
- **Response Note:** Risk score DOES NOT auto-qualify or auto-disqualify bidders.

---

### Q. Qualification Outcomes

#### `GET /api/v1/bid-submissions/{submission_id}/qualification-outcome`
- **Purpose:** Fetches system-suggested qualification outcome (`COMPLIANT`, `NOT COMPLIANT`, `PROVISIONAL`).
- **Roles:** `PROCUREMENT_OFFICER`, `AUDITOR`

---

### R. Officer Decisions

#### `POST /api/v1/bid-submissions/{submission_id}/decision`
- **Purpose:** Records human procurement officer final qualification decision.
- **Roles:** `PROCUREMENT_OFFICER`
- **Request Body:**
  ```json
  {
    "decision_choice": "QUALIFY",
    "justification_rationale": "All Cover 1 and Cover 2 requirements satisfied. CA Turnover Certificate verified on Page 3."
  }
  ```
- **Response `201 Created`:** Seals decision snapshot into tamper-evident audit ledger.

---

### S. Manual Overrides

#### `POST /api/v1/bid-submissions/{submission_id}/overrides`
- **Purpose:** Records itemized status override (e.g. `FAIL` → `PASS`).
- **Roles:** `PROCUREMENT_OFFICER`
- **Request Body:**
  ```json
  {
    "compliance_evaluation_id": "01HZX89J4K2P00000000000500",
    "overridden_status": "PASS",
    "override_reason": "MSE Registration Certificate uploaded under Cover 1 grants valid EMD waiver."
  }
  ```

---

### T. Audit Events

#### `GET /api/v1/audit/events`
- **Purpose:** Cursor-paginated read of application infrastructure audit logs.
- **Roles:** `AUDITOR`, `SUPER_ADMIN`

---

### U. Audit Hash-Chain Information

#### `GET /api/v1/audit/hash-chain/verify`
- **Purpose:** Returns mathematical verification status of SHA-256 tamper-evident log chain.
- **Roles:** `AUDITOR`, `SUPER_ADMIN`

---

### V. Reports

#### `POST /api/v1/reports/export`
- **Purpose:** Dispatches background job to compile CVC-compliant PDF/JSON audit report.
- **Roles:** `PROCUREMENT_OFFICER`, `AUDITOR`

---

### W. Long-Running Jobs & Status

#### `GET /api/v1/jobs/{job_id}`
- **Purpose:** Polling endpoint for background Celery jobs.
- **Roles:** All Authenticated Roles
- **Response `200 OK`:**
  ```json
  {
    "job_id": "01HZX89J4K2P00000000000001",
    "status": "COMPLETED",
    "progress_percentage": 100,
    "result_resource_url": "/api/v1/extractions/01HZX89J4K2P00000000000200",
    "completed_at": "2026-09-05T23:31:12.000Z"
  }
  ```
