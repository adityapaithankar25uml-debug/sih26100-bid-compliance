# 18. Requirement Traceability Matrix (RTM)

**Document ID:** SIH26100-DOC-018  
**Version:** 1.0.0  
**Phase:** Phase 0 — Final Traceability Matrix  
**Problem Statement:** SIH 26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement  
**Organization:** Ministry of Petroleum & Natural Gas (CPCL)  

---

## 1. Traceability Architecture Principle

Every requirement in the SIH 26100 platform must be completely traceable across the entire software architecture chain:
$$\text{SIH Requirement} \longrightarrow \text{Product Feature} \longrightarrow \text{Backend Capability} \longrightarrow \text{AI Capability} \longrightarrow \text{Verification Capability} \longrightarrow \text{Evidence Grounding} \longrightarrow \text{UI Component} \longrightarrow \text{Automated Test}$$

This ensures zero unverified claims, zero orphaned code components, and complete audit readiness for hackathon evaluators.

---

## 2. Complete Traceability Matrix

| SIH 26100 Problem Statement Requirement | Product Feature | Backend Capability | AI / ML Capability | Verification Capability | Evidence Artifact | UI Interface Component | Automated Test Suite |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Automation of Tender Prequalification Criteria Ingestion** | Tender NIT Clause Extractor | Tender Parser Service (`FastAPI` + `Pydantic`) | Local LLM (`Ollama Qwen 2.5 3B`) extracts structured parameters from raw PDF text | AST Schema Validator verifies parameter data types (Currency, Exp Years) | NIT PDF page snippet with highlighted clause parameters | `TenderSetupView.tsx` (Rule Configuration Form & Clause Preview) | `test_tender_parser.py` (Unit tests for NIT extraction against reference schemas) |
| **2. Automated Verification of Vendor Credentials (GST, PAN, MCA)** | Multi-Tiered Vendor Verification Gateway | `VendorGatewayManager` (Live/Sandbox/Mock/Manual routing) | None (100% deterministic regex checksum & API validation) | Checksum algorithm (GSTIN Modulus 36, PAN regex, Udyam syntax matcher) | API JSON Response Payload / Cryptographic Mock Verification Token | `VendorIdentityCard.tsx` (Status badges: `LIVE`, `MOCK`, `MANUAL`) | `test_vendor_gateway.py` (Mock API integration tests & checksum regex suite) |
| **3. Automated Compliance Evaluation of Bidder Submissions** | Deterministic Compliance Scoring Engine | `RuleEngineCore` (Pydantic boolean evaluation pipeline) | ZERO AI in scoring (100% Python boolean logic execution) | Mathematical comparator (`>=`, `<=`, `==`, Set Inclusion) | Execution Evaluation Log with exact inputs and calculated boolean results | `ComplianceMatrixTable.tsx` (Pass/Fail itemized checklist table) | `test_rule_engine.py` (Edge-case boundary testing for financial thresholds) |
| **4. High-Precision Technical & Financial Document Processing** | Multi-Doc OCR & Metric Extractor | `DocOCRService` (`PyMuPDF` + `PaddleOCR`) | Vision-Language / Text LLM extracts financial numbers & dates from scanned PDFs | Source Bounding Box coordinate calculator (`[x0, y0, x1, y1]`) | Extracted JSON metrics linked to exact PDF token coordinates | `SplitPDFViewer.tsx` (Side-by-side PDF preview with visual bounding boxes) | `test_ocr_extractor.py` (Accuracy benchmark tests against standard scanned PDFs) |
| **5. Make in India (MII) & Local Content Verification** | MII Order Classifier & UDIN Checker | `MIIVerificationModule` | OCR extracts local content percentage & ICAI UDIN string | DPIIT Class-I/II/Non-Local threshold checker + UDIN regex validator | CA Certificate PDF snippet highlighting UDIN and Local Content % | `MakeInIndiaWidget.tsx` (Class-I / Class-II badge & UDIN status indicator) | `test_mii_verifier.py` (Unit tests for Class-I/II logic and UDIN regex format) |
| **6. MSE / Startup Exemption Handling (EMD & Turnover)** | Exemption Rule Engine | `ExemptionManager` | OCR extracts Udyam Enterprise Activity classification | Activity Classifier (Denies exemption for Traders; approves Manufacturers/Services) | Udyam Certificate snippet highlighting NIC Activity Code | `ExemptionStatusCard.tsx` (Exemption approval/denial rationale card) | `test_exemption_engine.py` (Test suite for Trader vs Manufacturer rules) |
| **7. Human Committee Review & Manual Override** | Committee Override Module | `OverrideService` (Audit state machine update handler) | None | Non-empty rationale validator + Officer identity signer | Cryptographically signed Audit Event with Officer ID, timestamp & remarks | `OfficerOverrideModal.tsx` (Override dialog with mandatory justification text) | `test_override_service.py` (State machine transition & mandatory note tests) |
| **8. Audit Trail & Central Vigilance Commission (CVC) Compliance** | Immutable Audit Logger | `AuditLogger` (Append-only SHA-256 hash-chained logger) | None | SHA-256 hash chain verifier `Hash(n) == SHA256(Hash(n-1) + Payload)` | Immutable JSON Audit Log File with unbroken cryptographic chain | `AuditLogViewer.tsx` (Searchable timeline with cryptographic hash status) | `test_audit_logger.py` (Hash chain tamper-detection & integrity tests) |
| **9. Cartelization & Collusive Bidding Alert** | Multi-Bidder Cross-Analytic Engine | `CartelizationDetector` | None (Relational graph set-intersection) | Exact matching on Director DINs, Addresses, Phone Numbers & File Metadata | Cross-Bidder Collusion Matrix highlighting matching entity parameters | `CollusionMatrixView.tsx` (Bidder interaction graph & shared parameter alerts) | `test_cartelization.py` (Graph matching tests on synthetic collusive bidder pairs) |

---

## 3. Traceability Sign-off

- **Coverage:** 100% of SIH 26100 problem statement requirements mapped to backend, AI, verification, evidence, UI, and test suite.
- **Implementation Constraint:** No application code generated during Phase 0 baseline definition.
- **Phase Status:** Phase 0 Baseline Definition **COMPLETE**.
