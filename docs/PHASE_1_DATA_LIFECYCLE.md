# Phase 1 Data Lifecycle & Retention Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-010  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines technical data retention policies, immutability rules, archival stages, and soft deletion patterns. No automated cleanup scripts, SQL cron jobs, backend services, or application code are created.

---

## 1. Data Lifecycle Philosophy

Public procurement data at CPCL is subject to strict regulatory oversight by the Central Vigilance Commission (CVC), the Comptroller and Auditor General of India (CAG), and statutory audit authorities under the General Financial Rules (GFR 2017).

The data lifecycle model enforces **historical immutability** for all evaluation, evidence, decision, and audit records, while establishing structured retention policies for raw file blobs and transient session data.

---

## 2. Category-Specific Data Lifecycles

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CATEGORY DATA LIFECYCLE STAGES                           │
├───────────────────────┬─────────────────────────────────────────────────────┤
│ 1. SOURCE DOCUMENTS   │ UPLOAD ──► HASH ──► ENCRYPTED STORE ──► AUDIT RETENTION│
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 2. OCR EXTRACTIONS    │ PARSE ──► STRUCTURE ──► SCHEMA VALIDATE ──► SNAPSHOT │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 3. GOVT VERIFICATIONS │ REQUEST ──► ADAPTER EXECUTE ──► TTL CACHE ──► DB LOG │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 4. EVIDENCE LEDGER    │ ASSEMBLE ──► SHA-256 HASH ──► APPEND-ONLY ──► SEALED │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 5. OFFICER DECISION   │ DRAFT ──► RATIONALE ──► SEALED SNAPSHOT ──► PERMANENT│
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 6. AUDIT LOG LEDGER   │ CAPTURE ──► HASH BLOCK ──► APPEND-ONLY ──► PERMANENT │
└───────────────────────┴─────────────────────────────────────────────────────┘
```

### 2.1 Source Documents (`source_documents`)
1. **Ingestion & Validation:** Upload stream validated against MIME magic bytes, size limits, and virus scanning.
2. **Cryptographic Hashing:** Unique SHA-256 hash computed immediately to detect duplicate file uploads.
3. **Encrypted Storage:** File stored in encrypted MinIO object storage buckets (`AES-256`).
4. **Retention:** Preserved for the duration of the tender evaluation and legal dispute window.

### 2.2 OCR Document Extractions (`document_extractions`, `extracted_fields`)
1. **Extraction Run:** Layout analysis, page rendering, and field extraction executed by AI provider layer.
2. **Schema Validation:** Extracted fields validated against Pydantic schemas.
3. **Immutability:** Extraction snapshots are immutable. Upgrading OCR models creates a new `DocumentExtraction` version row without mutating historical extractions.

### 2.3 Government Verification Payloads (`government_verification_results`)
1. **Adapter Execution:** Dispatched in configured mode (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`).
2. **Transient Caching:** Response payload cached in Redis with configurable TTL (e.g., 24 hours) to prevent redundant external API calls.
3. **Permanent Record:** Verification payload snapshot and SHA-256 payload hash persisted in `government_verification_results` table for audit provenance.

### 2.4 Evidence Ledger Records (`evidence_records`)
1. **Assembly:** Links specific requirement evaluation to exact document bounding box or API verification result.
2. **SHA-256 Hashing:** Cryptographic evidence hash generated.
3. **Append-Only Retention:** Evidence records are strictly append-only. Corrections or overrides generate a new evidence version linked to the `parent_evidence_id`.

### 2.5 Officer Decisions & Overrides (`officer_decisions`, `manual_overrides`)
1. **Decision Form Submission:** Procurement officer inputs decision choice (`QUALIFY`, `DISQUALIFY`, `SEEK_CLARIFICATION`) and mandatory rationale text.
2. **Cryptographic Sign-Off:** System generates sealed decision snapshot and SHA-256 snapshot hash.
3. **Permanent Retention:** Officer decision records are permanently preserved and cannot be overwritten or deleted.

### 2.6 Audit Trail Events (`audit_events`, `audit_hash_chain_blocks`)
1. **Event Capture:** System events recorded in append-only `audit_events` table.
2. **Hash Block Sealing:** Background worker links event to preceding hash block: `Block_n = SHA256(Block_{n-1} + Timestamp + Actor + Payload)`.
3. **Permanent Vigilance Ledger:** Permanent retention for CVC and legal audit inspection.

---

## 3. Data Immutability & Append-Only Rules

To maintain vigilance compliance, database-level privileges MUST prohibit `UPDATE` and `DELETE` operations on audit and evidence tables.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IMMUTABILITY & APPEND-ONLY ENFORCEMENT                   │
├───────────────────────────────────┬─────────────────────────────────────────┤
│ TABLE NAME                        │ PERMITTED DATABASE OPERATIONS           │
├───────────────────────────────────┼─────────────────────────────────────────┤
│ `evidence_records`                │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
│ `evidence_links`                  │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
│ `officer_decisions`               │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
│ `manual_overrides`                │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
│ `audit_events`                    │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
│ `audit_hash_chain_blocks`         │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
└───────────────────────────────────┴─────────────────────────────────────────┘
```

---

## 4. Soft Deletion Policy

For non-auditable business master entities (e.g., `users`, `departments`), soft deletion is implemented using an explicit `deleted_at TIMESTAMPTZ` column.

- **Hard Deletes Prohibited:** Rows are never removed via `DELETE FROM table`.
- **Query Scoping:** Active application queries automatically append `WHERE deleted_at IS NULL`.
- **Audit Preservation:** Soft-deleted entities retain their historical references in past tender evaluation snapshots and audit logs.

---

## 5. Conceptual Legal & Regulatory Retention Matrix

The table below specifies data retention policies across domain entities. Retention timelines dependent on unconfirmed statutory procurement guidelines are explicitly tagged as `REQUIRES GOVERNMENT APPROVAL` or `POLICY CONFIGURATION REQUIRED`.

| Domain Category | Entity Tables | Active Lifecycle | Archival Strategy | Statutory Retention Period |
| :--- | :--- | :--- | :--- | :--- |
| **User & Tenant Master** | `users`, `roles`, `departments` | Active Employment | Soft-delete on deactivation | `POLICY CONFIGURATION REQUIRED` |
| **Tender Notices & Rules**| `tenders`, `tender_versions`, `requirements` | Tender Evaluation Window | Read-Only Cold Storage | `REQUIRES GOVERNMENT APPROVAL` (Min 10 Yrs per CVC) |
| **Bidder Submissions** | `bidders`, `bid_submissions`, `submission_covers` | Active Tender Process | Read-Only Cold Storage | `REQUIRES GOVERNMENT APPROVAL` (Min 10 Yrs per CVC) |
| **Raw Upload Files** | `source_documents` | Evaluation Phase | Encrypted MinIO Storage Bucket | `POLICY CONFIGURATION REQUIRED` |
| **OCR Extractions** | `document_extractions`, `extracted_fields` | Evaluation Phase | Retained with Source Document | `POLICY CONFIGURATION REQUIRED` |
| **Govt Verification Logs**| `verification_requests`, `results` | Active Verification | Immutable Database Storage | `REQUIRES GOVERNMENT APPROVAL` |
| **Evidence Ledger** | `evidence_records`, `evidence_links` | Permanent Audit Record | Immutable Append-Only Ledger | `REQUIRES GOVERNMENT APPROVAL` (Permanent Audit Ledger) |
| **Officer Decisions** | `officer_decisions`, `manual_overrides` | Permanent Legal Record | Immutable Sealed Ledger | `REQUIRES GOVERNMENT APPROVAL` (Permanent Legal Record) |
| **Audit Log Ledger** | `audit_events`, `audit_hash_chain_blocks` | Permanent Vigilance Record | Immutable SHA-256 Hash Chain | `REQUIRES GOVERNMENT APPROVAL` (Permanent Vigilance Record) |
