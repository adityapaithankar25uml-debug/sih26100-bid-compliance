# Phase 1 Data Security & Privacy Model Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-011  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines data security classification, encryption parameters, PII masking rules under DPDP Act 2023, and secret isolation mandates. No security code libraries, encryption keys, SQL scripts, or application source files are created.

---

## 1. Four-Tier Data Classification Framework

All domain data attributes specified in the Data Dictionary are classified into one of four security tiers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FOUR-TIER DATA CLASSIFICATION SCHEMA                     │
├───────────────────────┬─────────────────────────────────────────────────────┤
│ 1. PUBLIC             │ Tender NIT titles, eligibility criteria descriptions,│
│                       │ policy versions, & non-sensitive entity legal names │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 2. INTERNAL           │ System ULID identifiers, requirement codes, cover    │
│                       │ definitions, & compliance status evaluation flags   │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 3. CONFIDENTIAL       │ Extracted financial turnover figures, CA audit text,│
│                       │ user usernames, & raw government verification data  │
├───────────────────────┼─────────────────────────────────────────────────────┤
│ 4. RESTRICTED / PII   │ Personal email addresses, phone numbers, password   │
│                       │ hashes, & encrypted object storage bucket URIs      │
└───────────────────────┴─────────────────────────────────────────────────────┘
```

---

## 2. Field-Level Encryption & Hashing Strategy

### 2.1 Encryption at Rest (AES-256-GCM)
- Database columns classified as `RESTRICTED / PII` MUST be encrypted at rest using **AES-256-GCM** (Galois/Counter Mode) with unique initialization vectors (IV) per record.
- Affected Columns:
  - `users.email`
  - `users.password_hash` (Salted Argon2id / bcrypt hash)
  - `bidder_identities.identifier_value`
  - `source_documents.storage_uri`

### 2.2 Cryptographic Integrity Hashing (SHA-256)
- **Document Hashing:** SHA-256 hash computed on upload (`source_documents.sha256_hash`).
- **Evidence Hashing:** SHA-256 hash computed on evidence record assembly (`evidence_records.evidence_sha256`).
- **Verification Payload Hashing:** SHA-256 hash computed on raw government responses (`government_verification_results.payload_hash`).
- **Officer Decision Sealing:** SHA-256 hash computed on signed decision snapshot (`officer_decisions.snapshot_hash`).
- **Audit Ledger Chaining:** Block chaining computed across previous and current blocks (`audit_hash_chain_blocks.current_block_hash`).

---

## 3. DPDP Act 2023 Compliance & PII Masking Architecture

To comply with the Digital Personal Data Protection (DPDP) Act 2023, data transmitted to external cloud AI providers (Google Gemini API / OpenAI API) MUST be sanitized locally before leaving the application boundary.

```
┌─────────────────────────────────────────────────────────┐
│              LOCAL OCR TEXT STREAM INGESTION            │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│           LOCAL DETERMINISTIC REGEX REDACTOR            │
│  • Mask Personal Aadhaar: `[0-9]{4} [0-9]{4} [0-9]{4}`  │
│  • Mask Personal Phone:   `[+0-9]{10,13}`               │
│  • Mask Bank Account:     `[0-9]{9,18}`                 │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│         SANITIZED ORGANIZATIONAL DATA ONLY             │
│  (GSTIN, PAN, CIN, Corporate Address, Financials)       │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│         EXTERNAL AI PROVIDER (Gemini / OpenAI)          │
└─────────────────────────────────────────────────────────┘
```

### Key DPDP Act Rules:
1. **Organizational PII Permitted:** Commercial identifiers (GSTIN, Corporate PAN, CIN, Udyam Number, Official Corporate Address) necessary for public tender eligibility evaluation are classified as business enterprise data and processed for evaluation.
2. **Individual PII Redacted:** Personal Aadhaar numbers, personal bank account numbers, and personal phone numbers extracted from scanned attachments (e.g. proprietor ID copies) MUST be redacted locally before AI transit.

---

## 4. Absolute Secrets & Credentials Exclusion Policy

> [!CAUTION]
> **Strict Database Prohibition:**  
> The database schema MUST NEVER contain tables or columns intended to store API keys, GSP partnership secrets, Protean OPV credentials, JWT signing private keys, MinIO root credentials, or database passwords.

### Secret Isolation Architecture:
- All system credentials and private keys MUST be managed externally via **HashiCorp Vault** or secure environment-level secret mounts.
- Application backend modules retrieve temporary secret tokens in-memory via Vault API / environment variables — secrets are NEVER written to PostgreSQL tables or log files.

---

## 5. Database RBAC & Application Access Security

Database user privileges MUST enforce strict least-privilege segregation:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DATABASE USER ROLE PRIVILEGE MATRIX                       │
├─────────────────────┬───────────────────────────────────────────────────────┤
│ DB ROLE NAME        │ PERMITTED DATABASE PRIVILEGES                         │
├─────────────────────┼───────────────────────────────────────────────────────┤
│ `app_backend_user`  │ `SELECT`, `INSERT`, `UPDATE` on standard domain tables │
│                     │ `INSERT`, `SELECT` ONLY on audit & evidence tables     │
│                     │ (`NO UPDATE`, `NO DELETE` granted)                    │
├─────────────────────┼───────────────────────────────────────────────────────┤
│ `app_migrator_user` │ DDL privileges (`CREATE TABLE`, `ALTER`, `INDEX`)      │
│                     │ Used strictly during Phase 2 database migration jobs  │
├─────────────────────┼───────────────────────────────────────────────────────┤
│ `app_auditor_user`  │ `SELECT` ONLY on audit logs, evidence ledger, & DB    │
│                     │ (`NO INSERT`, `NO UPDATE`, `NO DELETE` granted)       │
└─────────────────────┴───────────────────────────────────────────────────────┘
```
