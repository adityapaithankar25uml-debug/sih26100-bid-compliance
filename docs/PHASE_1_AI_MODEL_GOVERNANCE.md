# Phase 1 AI Model Governance Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-019  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines model lifecycle management, prompt/template versioning, schema governance, failure state machines, and Human-in-the-Loop (HITL) checkpoints. No FastAPI routers, Python scripts, ORM models, database migrations, or AI code files are created.

---

## 1. Model Lifecycle Management

All AI models integrated into the platform transition through a strict governance lifecycle:

```
┌──────────────┐     ┌──────────────┐     ┌───────────────────┐     ┌────────────┐     ┌──────────┐
│ 1. EVALUATION│ ──> │ 2. ONBOARDING│ ──> │ 3. PROD_ACTIVE    │ ──> │ 4.DEPRECATE│ ──> │5.ARCHIVED│
│ (Benchmarking│     │ (Security &  │     │ (Active Ingestion)│     │ (Read-Only)│     │ (Legacy) │
└──────────────┘     └──────────────┘     └───────────────────┘     └────────────┘     └──────────┘
```

1. **Evaluation Phase:** Candidate models are benchmarked against frozen platform test suites (`PHASE_1_AI_EVALUATION_FRAMEWORK.md`). Must pass safety, prompt injection, and extraction accuracy thresholds.
2. **Onboarding Phase:** Model registered in AI Gateway configuration with data sensitivity rating and fallback priority.
3. **Production Active Phase:** Active model handling production task workloads. All calls logged with execution metadata.
4. **Deprecated Phase:** Model replaced by upgraded version. No new tasks dispatched to model; existing historical tasks remain queryable.
5. **Archived Phase:** Model configuration archived. Metadata preserved for audit reproducibility.

> **Model Change Control Rule:** A model upgrade MUST NOT silently overwrite or invalidate historical AI-derived extraction results. Historical evaluations preserve their original model ID, model version, and prompt version metadata.

---

## 2. Prompt & Template Governance

### 2.1 Prompt Naming & Versioning Taxonomy
System prompts, task prompts, extraction templates, and explanation prompts are stored as version-controlled Markdown/YAML files in a dedicated prompt registry.
- **Naming Convention:** `SP-{CATEGORY}-{TASK}-v{MAJOR}.{MINOR}` (System Prompts) and `TP-{CATEGORY}-{TASK}-v{MAJOR}.{MINOR}` (Task Prompts).
- **Examples:**
  - `SP-EXTRACTION-FINANCIAL-v1.2`
  - `TP-TENDER-CLAUSE_MINING-v2.0`
  - `TP-EXPLANATION-COMPLIANCE-v1.0`

### 2.2 Change Control & Approval Workflow
1. **Pull Request Review:** Any prompt modification requires a pull request containing baseline evaluation metrics showing no accuracy degradation.
2. **Mandatory Approvals:** Prompt changes require approval from both the **Lead AI Architect** and **Procurement Compliance Admin**.
3. **Immutability in Production:** Once deployed to production, a prompt version is immutable. Edits spawn a new minor/major version string.

---

## 3. Schema Governance & Audit Reproducibility

1. **Schema Version Tagging:** All JSON Schemas used for structured AI output enforcement carry an explicit `$id` version string (e.g. `https://schemas.bidcompliance.cpcl.gov.in/v1/ExtractedFieldsEnvelope.json`).
2. **Reproducibility Metadata Envelope:** Every AI-derived payload stored in the database or returned via API MUST contain:
   - `provider_id` & `model_identifier`
   - `model_version`
   - `system_prompt_version` & `user_prompt_template_version`
   - `schema_version`
   - `input_document_hash` (SHA-256)
   - `processing_timestamp`
   - `raw_output_sha256_hash`

---

## 4. AI Processing Failure State Machine

AI task execution follows a formal deterministic state machine:

```
                  ┌──────────────┐
                  │ NOT_STARTED  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   QUEUED     │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  PROCESSING  │
                  └──────┬───────┘
                         │
         ┌───────────────┼────────────────────────┬──────────────────────┐
         ▼               ▼                        ▼                      ▼
  ┌─────────────┐ ┌─────────────┐        ┌──────────────────┐  ┌──────────────────┐
  │  SUCCEEDED  │ │   PARTIAL   │        │ LOW_CONFIDENCE   │  │ VALIDATION_FAILED│
  └─────────────┘ └─────────────┘        └────────┬─────────┘  └────────┬─────────┘
                                                  │                     │
                                                  ▼                     ▼
                                         ┌──────────────────────────────────────────┐
                                         │          REQUIRES_HUMAN_REVIEW           │
                                         └──────────────────────────────────────────┘
```

### State Definitions & Handling:
- `NOT_STARTED`: Task initialized in database.
- `QUEUED`: Enqueued in Celery / Redis task queue.
- `PROCESSING`: Active model inference underway.
- `SUCCEEDED`: Inference complete, schema validation passed, task-specific confidence threshold satisfied.
- `PARTIAL`: Multi-field extraction partially completed; missing optional fields.
- `LOW_CONFIDENCE`: Extraction completed but confidence is below the task-specific policy threshold. Triggers `REQUIRES_HUMAN_REVIEW` or deterministic fallback.
- `VALIDATION_FAILED`: LLM output failed Pydantic JSON Schema validation. Triggers `REQUIRES_HUMAN_REVIEW`.
- `FAILED`: Model API error, timeout, or circuit breaker trip. Triggers Fallback Eligibility Gate evaluation or `REQUIRES_HUMAN_REVIEW`.
- `REQUIRES_HUMAN_REVIEW`: Task flagged for visual review on Officer Workbench UI.
- `CANCELLED`: Job revoked by user or system supervisor.

> **CRITICAL FAILURE ISOLATION RULE:** An AI processing failure (`FAILED`, `VALIDATION_FAILED`, `LOW_CONFIDENCE`) MUST NEVER automatically result in a compliance `FAIL` status or a bidder `DISQUALIFIED` outcome. It MUST produce a `NOT_VERIFIED` or `REQUIRES_HUMAN_REVIEW` status.

---

## 5. Human-in-the-Loop (HITL) Checkpoints

The platform enforces 6 mandatory human review checkpoints where AI outputs require officer intervention:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          6 MANDATORY HUMAN-IN-THE-LOOP CHECKPOINTS                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│ CHECKPOINT 1: Tender Requirement Approval (Admin confirms AI-mined clauses)             │
│ CHECKPOINT 2: Low-Confidence Extraction Review (Officer verifies fields below policy threshold) │
│ CHECKPOINT 3: Conflicting Identity Info Review (Officer checks mismatched names/PANs)   │
│ CHECKPOINT 4: High-Risk Anomaly Signal Review (Officer reviews risk flags)              │
│ CHECKPOINT 5: Unresolved Govt Verification Review (Officer checks MANUAL_FALLBACK)     │
│ CHECKPOINT 6: Final Qualification / Disqualification Decision (Officer explicit choice)│
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### Officer Override Auditing
When a procurement officer modifies or overrides an AI-extracted candidate value or itemized compliance status:
1. The original AI-extracted value, model ID, and confidence score are preserved unchanged.
2. The overridden value, officer User ID, timestamp, and **mandatory rationale text** are recorded in `manual_overrides`.
3. The override action emits an immutable event to the SHA-256 tamper-evident `audit_events` ledger.
