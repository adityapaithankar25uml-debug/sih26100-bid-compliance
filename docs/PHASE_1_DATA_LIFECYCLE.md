# Phase 1 Data Lifecycle & Retention Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-010  
**Version:** 1.1.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines technical data retention policies, immutability rules, archival stages, and soft deletion patterns. No automated cleanup scripts, SQL cron jobs, backend services, or application code are created.

---

## 1. Data Lifecycle Philosophy

Public procurement data at CPCL is subject to regulatory oversight by statutory audit authorities under the General Financial Rules (GFR 2017) and internal vigilance guidelines.

The data lifecycle model enforces **historical immutability** for all evaluation, evidence, decision, and audit records, while establishing configurable retention policies for raw file blobs and transient session data.

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

---

## 3. Configurable Retention Policy Matrix

System retention schedules are NOT hardcoded into database schemas or code logic. All retention periods MUST be configured dynamically according to applicable legal and organizational policies. Where statutory guidelines are unconfirmed, retention parameters are marked `POLICY CONFIGURATION REQUIRED` or `REQUIRES GOVERNMENT APPROVAL`.

| Domain Category | Entity Tables | Active Lifecycle | Archival Strategy | Statutory Retention Period |
| :--- | :--- | :--- | :--- | :--- |
| **User & Tenant Master** | `users`, `roles`, `departments` | Active Employment | Soft-delete on deactivation | `POLICY CONFIGURATION REQUIRED` |
| **Tender Notices & Rules**| `tenders`, `tender_versions`, `requirements` | Tender Evaluation Window | Read-Only Cold Storage | `REQUIRES GOVERNMENT APPROVAL` |
| **Bidder Submissions** | `bidders`, `bid_submissions`, `submission_covers` | Active Tender Process | Read-Only Cold Storage | `REQUIRES GOVERNMENT APPROVAL` |
| **Raw Upload Files** | `source_documents` | Evaluation Phase | Encrypted MinIO Storage Bucket | `POLICY CONFIGURATION REQUIRED` |
| **OCR Extractions** | `document_extractions`, `extracted_fields` | Evaluation Phase | Retained with Source Document | `POLICY CONFIGURATION REQUIRED` |
| **Govt Verification Logs**| `verification_requests`, `attempts`, `results` | Active Verification | Immutable Database Storage | `REQUIRES GOVERNMENT APPROVAL` |
| **Evidence Ledger** | `evidence_records` | Permanent Audit Record | Immutable Append-Only Ledger | `REQUIRES GOVERNMENT APPROVAL` |
| **Officer Decisions** | `officer_decisions`, `manual_overrides` | Permanent Legal Record | Immutable Sealed Ledger | `REQUIRES GOVERNMENT APPROVAL` |
| **Audit Log Ledger** | `audit_events`, `audit_hash_chain_blocks` | Permanent Vigilance Record | Immutable SHA-256 Hash Chain | `REQUIRES GOVERNMENT APPROVAL` |

---

## 4. Data Immutability & Append-Only Rules

To maintain vigilance compliance, database-level privileges MUST prohibit `UPDATE` and `DELETE` operations on audit and evidence tables.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    IMMUTABILITY & APPEND-ONLY ENFORCEMENT                   │
├───────────────────────────────────┬─────────────────────────────────────────┤
│ TABLE NAME                        │ PERMITTED DATABASE OPERATIONS           │
├───────────────────────────────────┼─────────────────────────────────────────┤
│ `evidence_records`                │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
│ `officer_decisions`               │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
│ `manual_overrides`                │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
│ `audit_events`                    │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
│ `audit_hash_chain_blocks`         │ INSERT, SELECT ONLY (No UPDATE / DELETE)│
└───────────────────────────────────┴─────────────────────────────────────────┘
```

---

## 5. Soft Deletion Policy

For non-auditable business master entities (e.g., `users`, `departments`), soft deletion is implemented using an explicit `deleted_at TIMESTAMPTZ` column. Rows are never removed via hard `DELETE`. Active queries filter `WHERE deleted_at IS NULL`.
