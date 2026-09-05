# Phase 1 Data Security & Privacy Model Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-011  
**Version:** 1.1.0  
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

## 2. Password, Credential, & Secret Handling Architecture

> [!IMPORTANT]
> **Strict Password & Credential Security Rules:**  
> 1. **No Plaintext Passwords:** Passwords MUST NEVER be stored in plaintext anywhere in database tables, log files, or cache layers.  
> 2. **No Reversible Encryption for Passwords:** Reversible encryption (e.g. AES/RSA) MUST NOT be used for password storage. Passwords MUST be cryptographically salted and hashed.  
> 3. **Dedicated Password Hashing:** Password verification MUST use a dedicated slow password hashing algorithm (**Argon2id** / **bcrypt** / **scrypt**) with cryptographically random per-user salts.  
> 4. **No Secrets in Database Tables:** API keys, GSP client secrets, Protean OPV credentials, JWT signing private keys, and MinIO root passwords MUST NEVER be stored in application database tables.  
> 5. **Secret Isolation:** Credential material is managed exclusively via HashiCorp Vault or secure environment-level secret mounts and loaded into application memory at runtime.

---

## 3. Comprehensive Pre-AI Data Protection & Privacy Pipeline

To enforce compliance with the Digital Personal Data Protection (DPDP) Act 2023, regex pattern matching is treated as only ONE component of a comprehensive multi-stage Pre-AI Data Protection Pipeline. **The platform MUST NOT automatically transmit every uploaded document to an external cloud AI provider.**

```
┌──────────────┐     ┌────────────────┐     ┌─────────────────────┐     ┌───────────────────┐
│ SOURCE FILE  │──►  │ CLASSIFICATION │──►  │ SENSITIVITY ASSESS  │──►  │ PII POLICY ENGINE │
└──────────────┘     └────────────────┘     └─────────────────────┘     └───────────────────┘
                                                                                  │
┌──────────────┐     ┌────────────────┐     ┌─────────────────────┐               │
│ AI PROVIDER  │◄──  │ AI ELIGIBILITY │◄──  │ DETERMINISTIC REDACT│◄──────────────┘
└──────────────┘     └────────────────┘     └─────────────────────┘
```

### Multi-Stage Pipeline Controls:
1. **Document Classification:** Identifies document type (Tax Invoice, Financial Audit, OEM Certificate, Proprietary Technical Spec, Personal ID Copy).
2. **Sensitivity Assessment & Document Blocking:** High-sensitivity personal documents (e.g., individual passport copies, personal tax returns) are **BLOCKED from external cloud AI processing** and routed exclusively to local OCR parser or officer human review.
3. **Structured Pattern Detection:** Combines regex patterns (Aadhaar, personal phone, bank account), dictionary lookups, and NER (Named Entity Recognition) to tag sensitive tokens.
4. **Document-Type Specific Redaction:** Applies contextual redaction rules based on document category (e.g. redacting personal signatures and individual bank details on proprietary technical specifications).
5. **Allowlist & Policy Check:** Verifies that document fields contain authorized organizational PII (GSTIN, Corporate PAN, CIN, Official Corporate Address) necessary for public tender evaluation.
6. **External-AI Eligibility Routing:** If a document passes all eligibility checks, text is transmitted to Cloud AI (Gemini / OpenAI); otherwise, processing falls back to Local Offline LLM (Ollama Qwen 2.5) or manual human review.

---

## 4. Field-Level Encryption & Hashing Strategy

### 4.1 Encryption at Rest (AES-256-GCM)
- Database columns classified as `RESTRICTED / PII` MUST be encrypted at rest using **AES-256-GCM** with unique initialization vectors (IV) per record.
- Affected Columns: `users.email`, `users.password_hash`, `bidder_identities.identifier_value`, `source_documents.storage_uri`.

### 4.2 Cryptographic Integrity Hashing (SHA-256)
- SHA-256 integrity hashes computed for `source_documents.sha256_hash`, `evidence_records.evidence_sha256`, `government_verification_results.payload_hash`, `officer_decisions.snapshot_hash`, and `audit_hash_chain_blocks.current_block_hash`.

---

## 5. Database Role-Based Access Control (RBAC)

Database user privileges MUST enforce strict least-privilege segregation:
- `app_backend_user`: `SELECT, INSERT, UPDATE` on business tables; `INSERT, SELECT` ONLY on audit & evidence tables (`NO UPDATE`, `NO DELETE`).
- `app_auditor_user`: `SELECT` ONLY on audit logs and evidence ledger.
