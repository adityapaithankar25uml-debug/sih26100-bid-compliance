# Phase 1 AI Data Execution Flow Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-022  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document provides visual Mermaid sequence and data flow diagrams for all AI-assisted platform workflows. No application controllers, code files, or backend scripts are created.

---

## 1. Flow 1: Document Upload, Layout Parsing, & AI Field Extraction

```mermaid
sequenceDiagram
    autonumber
    actor Officer as Procurement Officer
    participant API as API Gateway (/api/v1)
    participant Worker as Background Celery Worker
    participant Storage as Encrypted MinIO Storage
    participant Privacy as Pre-AI Privacy Gateway
    participant Gateway as AI Gateway Interface
    participant Model as Approved AI Model (vLLM/Ollama)
    participant DB as PostgreSQL Database

    Officer->>API: POST /api/v1/submissions/{id}/documents/upload
    API->>Storage: Store Encrypted PDF File
    API->>DB: Record Document Status (PENDING_EXTRACTION)
    API-->>Officer: 202 Accepted (Location: /api/v1/jobs/{job_id})
    API->>Worker: Dispatch Extraction Job (job_id)
    Worker->>Storage: Retrieve Document PDF
    Worker->>Worker: Render Page Images & OCR Parsing
    Worker->>Privacy: Sanitize Extracted Text (PII Redaction)
    Privacy-->>Worker: Sanitized Text Chunk + Sensitivity Level
    Worker->>Gateway: AIGatewayRequest (Task: STRUCTURED_EXTRACTION)
    Gateway->>Model: Execute Prompt + JSON Schema Target
    Model-->>Gateway: Raw Structured Output Payload
    Gateway->>Worker: Validated Structured Fields + Provenance
    Worker->>DB: Save ExtractedFields & Evidence Candidates
    Worker->>DB: Update Job Status (COMPLETED)
    Officer->>API: GET /api/v1/jobs/{job_id}
    API-->>Officer: 200 OK (status: COMPLETED, result_url)
```

---

## 2. Flow 2: Tender Notice Ingestion & Human Requirement Confirmation

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Procurement Admin
    participant API as API Gateway (/api/v1)
    participant Gateway as AI Gateway Interface
    participant Model as Category 1/3 Reasoning Model
    participant DB as PostgreSQL Database

    Admin->>API: POST /api/v1/tenders (Upload NIT PDF)
    API->>Gateway: AIGatewayRequest (Task: REQUIREMENT_MINING)
    Gateway->>Model: Extract Eligibility Clauses + Rule Mapping Candidates
    Model-->>Gateway: Candidate Requirement List Envelope
    Gateway->>API: Validated Candidate Proposals
    API->>DB: Save Requirements (isConfirmedByHuman: FALSE)
    API-->>Admin: 200 OK (Render Workbench UI with Unconfirmed Candidates)
    Admin->>API: POST /api/v1/tender-versions/{id}/requirements/confirm
    Note over Admin,API: Admin reviews, edits thresholds, & binds Python Rules
    API->>DB: Update Requirements (isConfirmedByHuman: TRUE)
    API->>DB: Lock TenderVersion Snapshot
    API-->>Admin: 200 OK (Tender Evaluation Ready)
```

---

## 3. Flow 3: Multi-Document Entity Resolution & Rule Evaluation

```mermaid
sequenceDiagram
    autonumber
    actor Officer as Procurement Officer
    participant API as API Gateway (/api/v1)
    participant Gateway as AI Gateway Interface
    participant Model as Category 3 Model (Anomaly Detection)
    participant Adapter as Govt Verification Adapter Gateway
    participant RuleEngine as Deterministic Python Rule Engine
    participant DB as PostgreSQL Database

    Officer->>API: POST /api/v1/bid-submissions/{id}/evaluate
    API->>Gateway: AIGatewayRequest (Task: ANOMALY_DETECTION)
    Gateway->>Model: Cross-Document Entity Resolution Check
    Model-->>Gateway: Anomaly Signal List (Mismatched PAN/GSTIN)
    API->>Adapter: Trigger Authoritative Govt Verification (GSTN / MCA)
    Adapter-->>API: Verified Payload + Provenance Tag ([LIVE_VERIFIED])
    API->>RuleEngine: Execute Registered Pydantic Compliance Rules
    Note over RuleEngine: Rule Engine compares Verified Payload vs Requirement
    RuleEngine-->>API: ComplianceEvaluation Result (PASS / FAIL / REVIEW)
    API->>DB: Save ComplianceEvaluations & Risk Profile
    API-->>Officer: 200 OK (Render Evaluation Workbench)
```

---

## 4. Flow 4: Explanation Generation & CVC Audit Report Export

```mermaid
sequenceDiagram
    autonumber
    actor Auditor as Auditor / Officer
    participant API as API Gateway (/api/v1)
    participant Grounder as Grounding Verification Engine
    participant Gateway as AI Gateway Interface
    participant Model as Approved AI Model
    participant DB as PostgreSQL Database

    Auditor->>API: POST /api/v1/reports/export (Format: PDF)
    API->>DB: Fetch Evaluation Results + Evidence Records
    API->>Gateway: AIGatewayRequest (Task: COMPLIANCE_EXPLANATION)
    Gateway->>Model: Generate Plain Language Explanation (Context: Evidence IDs)
    Model-->>Gateway: Raw Explanation Text Payload
    Gateway->>Grounder: Verify 100% Evidence Citation Grounding
    Grounder-->>API: Grounded Explanation Envelope
    API->>API: Compile CVC Audit PDF Report
    API->>DB: Record Audit Event & Hash Block
    API-->>Auditor: 200 OK (PDF Stream / Download Link)
```
