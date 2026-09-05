# 17. Final Requirements Baseline (MoSCoW Categorization)

**Document ID:** SIH26100-DOC-017  
**Version:** 1.0.0  
**Phase:** Phase 0 — Final Baseline  
**Problem Statement:** SIH 26100 (AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement)  
**Organization:** Ministry of Petroleum & Natural Gas (CPCL)  

---

## 1. Executive Summary & Categorization Strategy

This document establishes the authoritative requirements baseline for the SIH 26100 platform. Requirements are derived directly from the problem statement, CPCL procurement guidelines, government integration reality audit, and jury review.

Requirements are partitioned using the **MoSCoW** framework:
- **MUST HAVE (MVP Mandatory):** Direct core requirements of SIH 26100. Non-negotiable for hackathon demo.
- **SHOULD HAVE (High Value):** Essential operational capabilities for real-world CPCL committee usability.
- **COULD HAVE (Innovation/Delighters):** Advanced features like collusion/cartelization detection.
- **DEFERRED (Post-Hackathon/Enterprise Phase):** Capabilities requiring direct government MoUs or full production deployment.

---

## 2. Detailed Requirement Specification

### 2.1 MUST HAVE (Core SIH 26100 Requirements)

#### Req-MH-01: Tender Document & Clause Parameter Configuration
- **Requirement ID:** REQ-MH-01
- **Requirement:** System must ingest Tender NIT/GeM Custom Parameter PDFs and extract mandatory pre-qualification criteria (Turnover, Experience, EMD, MII, Land Border).
- **User:** CPCL Procurement Officer / Tender Creator
- **Input:** Tender NIT PDF document or GeM Parameter JSON
- **Output:** Structured Tender Compliance Schema (YAML/JSON)
- **Verification Method:** Manual committee sign-off on extracted rule parameters.
- **AI Involvement:** Local LLM extracts clause parameters from unstructured NIT text.
- **Deterministic Logic:** Pydantic validation schema parses extracted fields into strict typed data types.
- **Evidence Required:** Clause text snippet with page and line number from Tender NIT PDF.
- **Government Source:** CPCL / GeM Tender Portal
- **Integration Mode:** PDF Upload / File System
- **Security Consideration:** Role-Based Access Control (Tender Creator only).
- **Priority:** MUST HAVE

#### Req-MH-02: Bidder Document Batch Ingestion & Cover Separation
- **Requirement ID:** REQ-MH-02
- **Requirement:** System must ingest multi-bidder document packages and separate them into Cover 1 (Fee/EMD) and Cover 2 (Techno-Commercial).
- **User:** Evaluation Committee Member
- **Input:** Zip archive / PDF files per bidder (Turnover, GST, Udyam, Orders, CA Certs).
- **Output:** Categorized Bidder Document Tree per cover.
- **Verification Method:** Visual file tree check in UI.
- **AI Involvement:** Classification LLM identifies document types (GST Cert, CA Audit, Order Copy).
- **Deterministic Logic:** MIME type verification, PDF page count check, and file hash calculation.
- **Evidence Required:** Original uploaded PDF files anchored to bidder ID.
- **Government Source:** GeM Portal Bidder Submission Package
- **Integration Mode:** Local Disk / Object Storage
- **Security Consideration:** AES-256 storage encryption, virus scan check.
- **Priority:** MUST HAVE

#### Req-MH-03: Multi-Tiered Vendor Verification Gateway (GSTIN / PAN / Udyam)
- **Requirement ID:** REQ-MH-03
- **Requirement:** System must verify vendor identity and registration numbers using a multi-tiered LIVE / SANDBOX / MOCK / MANUAL gateway architecture.
- **User:** System / Evaluation Engine
- **Input:** Vendor GSTIN, PAN, Udyam Registration Number
- **Output:** Verification status object with explicit provenance tag (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL`).
- **Verification Method:** Automated API response check or Regex Checksum validation.
- **AI Involvement:** None (100% API & Regex logic).
- **Deterministic Logic:** Modulus 36 GSTIN checksum calculation, PAN structure regex matching (`[A-Z]{3}[PCHFATBLJG][A-Z]{1}[0-9]{4}[A-Z]{1}`), Udyam format validation.
- **Evidence Required:** API Response Payload / Cryptographic Mock Token + Verification Timestamp.
- **Government Source:** GSTN / Income Tax / Udyam Portal
- **Integration Mode:** Multi-Tiered (Live API -> Staging Sandbox -> Local Mock Gateway -> Manual OCR)
- **Security Consideration:** API key encryption in memory, zero storage of plain auth secrets.
- **Priority:** MUST HAVE

#### Req-MH-04: Deterministic Compliance Rule Engine & Scoring
- **Requirement ID:** REQ-MH-04
- **Requirement:** System must evaluate bidder extracted data against tender compliance criteria and compute deterministic Pass/Fail flags per clause.
- **User:** System / Evaluation Engine
- **Input:** Extracted Bidder Metrics + Structured Tender Compliance Schema
- **Output:** Itemized Compliance Breakdown Matrix (Pass/Fail per clause + Overall Status).
- **Verification Method:** Automated unit testing of boolean mathematical comparisons.
- **AI Involvement:** ZERO (Strictly prohibited from scoring logic).
- **Deterministic Logic:** Mathematical comparison (e.g. `Bidder_Turnover >= Tender_Min_Turnover`, `Bidder_Exp_Years >= Tender_Min_Years`).
- **Evidence Required:** Equation execution log with exact variable inputs and evaluated boolean outputs.
- **Government Source:** N/A (Internal Platform Engine)
- **Integration Mode:** Local Application Engine
- **Security Consideration:** Immutable memory execution, zero prompt injection risk.
- **Priority:** MUST HAVE

#### Req-MH-05: Source Grounding & Bounding-Box Evidence Viewer
- **Requirement ID:** REQ-MH-05
- **Requirement:** System must link every extracted financial/compliance value to its exact location in the bidder's uploaded PDF.
- **User:** Committee Member / Auditor
- **Input:** Evaluated Compliance Clause Result
- **Output:** PDF Viewer automatically highlighting the exact text snippet with a visual bounding box.
- **Verification Method:** Visual inspection by committee member in UI.
- **AI Involvement:** OCR / Layout Analysis model provides token coordinate bounding boxes `[x0, y0, x1, y1]`.
- **Deterministic Logic:** Coordinate mapping onto PDF page overlay.
- **Evidence Required:** Interactive PDF page overlay showing exact highlighted line.
- **Government Source:** Bidder Uploaded Documents
- **Integration Mode:** Local PDF Viewer Integration
- **Security Consideration:** Read-only document stream rendering.
- **Priority:** MUST HAVE

#### Req-MH-06: Human-in-the-Loop Officer Review & Override
- **Requirement ID:** REQ-MH-06
- **Requirement:** System must allow procurement officers to review AI/Rule engine results, accept/reject recommendations, and apply manual overrides with mandatory remarks.
- **User:** Senior CPCL Procurement Officer
- **Input:** Override Action + Mandatory Justification Text
- **Output:** Updated Compliance Result with `[OVERRIDDEN_BY_OFFICER]` tag.
- **Verification Method:** Officer sign-off confirmation.
- **AI Involvement:** None.
- **Deterministic Logic:** Status state machine update + mandatory non-empty text validation.
- **Evidence Required:** Officer ID, Timestamp, Previous Status, New Status, Justification Note.
- **Government Source:** CPCL Evaluation Committee
- **Integration Mode:** UI Action Endpoint
- **Security Consideration:** Cryptographic signature of officer override entry.
- **Priority:** MUST HAVE

---

### 2.2 SHOULD HAVE (High Value Operational Features)

#### Req-SH-01: Make in India (MII) & CA UDIN Validation
- **Requirement ID:** REQ-SH-01
- **Requirement:** System must classify bidders into Class-I (≥50%), Class-II (≥20%), or Non-Local (<20%) local content categories and verify ICAI UDIN on CA certificates for high-value tenders.
- **User:** Procurement Officer
- **Input:** Local Content Declaration PDF / CA Certificate
- **Output:** MII Class Category + UDIN Validity Status
- **Verification Method:** Regex UDIN structural validation (`18/24 digit ICAI format`) + Local Content % rule check.
- **AI Involvement:** OCR extracts local content percentage and UDIN string.
- **Deterministic Logic:** Threshold classification logic.
- **Evidence Required:** CA Certificate snippet with highlighted UDIN and Local Content percentage.
- **Government Source:** DPIIT / ICAI UDIN Portal
- **Integration Mode:** Document OCR + ICAI Format Checker
- **Security Consideration:** Audit log of CA certificate verification.
- **Priority:** SHOULD HAVE

#### Req-SH-02: MSE / Startup EMD & Turnover Exemption Rule Engine
- **Requirement ID:** REQ-SH-02
- **Requirement:** System must evaluate Udyam / Startup India certificates and apply EMD/Turnover waivers ONLY IF bidder is classified as Manufacturer/Service Provider (denying reseller exemptions per GeM/CPCL rules).
- **User:** Committee Member
- **Input:** Udyam Certificate OCR Data
- **Output:** Exemption Eligibility Status (`APPROVED_MANUFACTURER` vs `DENIED_TRADER`).
- **Verification Method:** Rule engine check against Udyam Enterprise Activity Code (NIC Code).
- **AI Involvement:** OCR extracts enterprise classification text.
- **Deterministic Logic:** Boolean match on Manufacturing vs Trading activity string.
- **Evidence Required:** Udyam certificate activity section highlighting NIC code.
- **Government Source:** Ministry of MSME / DPIIT
- **Integration Mode:** Document OCR + Local Exemption Rules
- **Security Consideration:** Read-only rule evaluation.
- **Priority:** SHOULD HAVE

#### Req-SH-03: Immutable Hash-Chained Audit Trail (CVC / CAG Ready)
- **Requirement ID:** REQ-SH-03
- **Requirement:** System must record every tender creation, document ingestion, rule execution, API call, and officer override in an append-only, SHA-256 hash-chained log.
- **User:** CVC / CAG / Internal Auditor
- **Input:** Platform System Events
- **Output:** Audit Trail Verification Report & Hash Integrity Status
- **Verification Method:** Automated SHA-256 chain recalculation test.
- **AI Involvement:** None.
- **Deterministic Logic:** Cryptographic hash generation `Hash(n) = SHA256(Hash(n-1) + EventPayload)`.
- **Evidence Required:** Verifiable JSON log stream with unbroken cryptographic hashes.
- **Government Source:** CPCL Internal Vigilance Department
- **Integration Mode:** Embedded Audit Logger
- **Security Consideration:** Write-once log storage, non-repudiation.
- **Priority:** SHOULD HAVE

---

### 2.3 COULD HAVE (Innovation & Delighters)

#### Req-CH-01: Collusive Bidding & Cartelization Detector
- **Requirement ID:** REQ-CH-01
- **Requirement:** System must cross-analyze all submitted bidder packages in a tender batch to detect common Directors, shared PANs, identical document metadata, or matching IP/submission patterns.
- **User:** Vigilance Officer / Procurement Head
- **Input:** Full Tender Batch Document Metadata & Entity Data
- **Output:** Collusion Risk Matrix highlighting shared parameters between Bidder X and Bidder Y.
- **Verification Method:** Graph matching / Set intersection test.
- **AI Involvement:** None (100% relational graph matching).
- **Deterministic Logic:** Exact match join on Director DINs, Addresses, and Phone Numbers.
- **Evidence Required:** Side-by-side comparison table highlighting matching entity fields.
- **Government Source:** MCA Master Data / Tender Submissions
- **Integration Mode:** Multi-Bidder Batch Analytics Engine
- **Security Consideration:** Strictly internal committee access only.
- **Priority:** COULD HAVE

---

### 2.4 DEFERRED (Post-Hackathon Enterprise Scope)

#### Req-DF-01: Direct Production NIC API Setu & MCA V3 Integration
- **Requirement ID:** REQ-DF-01
- **Requirement:** Direct live production integration with MeitY API Setu gateway and MCA V3 database via official government department MoU credentials.
- **Priority:** DEFERRED (Requires formal Ministry MoU and production IP whitelisting post-SIH).

#### Req-DF-02: Automated SAP S/4HANA Vendor Master Synchronization
- **Requirement ID:** REQ-DF-02
- **Requirement:** Direct automated push of qualified bidder status into CPCL's enterprise SAP ERP vendor master database.
- **Priority:** DEFERRED (Enterprise staging requirement post-pilot approval).

---

## 3. Summary Baseline Table

| Req ID | Title | Priority | AI Role | Deterministic Logic | Verification Mode |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-MH-01** | Tender Clause Configuration | **MUST HAVE** | LLM Extraction | Pydantic Schema | Manual Sign-off |
| **REQ-MH-02** | Bidder Package Cover Separation | **MUST HAVE** | LLM Classifier | File Hash & MIME | Visual Tree Check |
| **REQ-MH-03** | Multi-Tier Vendor Gateway | **MUST HAVE** | None | Regex / Checksum | Multi-Tier Gateway |
| **REQ-MH-04** | Deterministic Compliance Engine | **MUST HAVE** | ZERO | Boolean Comparison | Unit Tests |
| **REQ-MH-05** | Source Grounding Evidence Viewer | **MUST HAVE** | Layout OCR | Bounding Box Map | Interactive UI |
| **REQ-MH-06** | Officer Review & Override | **MUST HAVE** | None | State Machine | Officer Audit Note |
| **REQ-SH-01** | Make in India & UDIN Check | **SHOULD HAVE** | OCR Extraction | Threshold & Regex | CA Cert Snippet |
| **REQ-SH-02** | MSE Trader vs Manufacturer Check | **SHOULD HAVE** | OCR Extraction | Activity Match | Udyam Activity Snippet |
| **REQ-SH-03** | SHA-256 Hash-Chained Audit Log | **SHOULD HAVE** | None | Cryptographic Hash | Hash Chain Verifier |
| **REQ-CH-01** | Cartelization & Collusion Detector | **COULD HAVE** | None | Graph Set Intersection | Cross-Bidder Matrix |
| **REQ-DF-01** | Direct Production NIC API Access | **DEFERRED** | N/A | N/A | N/A |
| **REQ-DF-02** | CPCL SAP S/4HANA Push | **DEFERRED** | N/A | N/A | N/A |
