# Phase 8 — SIH Problem Statement to Solution Traceability Matrix

## Problem Statement Summary

- **Problem Statement ID:** SIH26100
- **Title:** AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Ministry / Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)
- **Theme:** Smart Automation
- **PS Requirement Coverage:** Comprehensive

---

## SIH Requirement Traceability Matrix

| Requirement ID | SIH PS Requirement / Capability | Implemented Component | Demonstration Location | Evidence / Test | Current Status | Production Gap / Onboarding Path |
|---|---|---|---|---|---|---|
| **REQ-01** | Udyam / MSME Certificate & Category Verification | Government Adapter (`UDYAM`), Evidence Model & Compliance Rules | `/verification` & `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires authorized API onboarding with Ministry of MSME / Udyam portal |
| **REQ-02** | GSTIN Registration & Filing Compliance Verification | Government Adapter (`GST`), Evidence Model & Compliance Rules | `/verification` & `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires authorized API onboarding with GST Network (GSTN) |
| **REQ-03** | Income Tax PAN Verification & Entity Matching | Government Adapter (`PAN`), Evidence Model & Compliance Rules | `/verification` & `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires authorized PAN verification API onboarding |
| **REQ-04** | Make in India (MII) Local Content % Verification | Deterministic Rule (`R_MII_01`), Evidence Model (`MII_DECLARATION`), PII/Extraction Gateway | `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **DEMO PROTOTYPE** | Production auditor verification for local content validation |
| **REQ-05** | EPFO Establishment Registration & Remittance Verification | Government Adapter (`EPFO`), Evidence Model & Compliance Rules | `/verification` & `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires authorized EPFO portal API onboarding |
| **REQ-06** | ESIC Establishment Registration Verification | Government Adapter (`ESIC`), Evidence Model & Compliance Rules | `/verification` & `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires authorized ESIC portal API integration credentials |
| **REQ-07** | DPIIT Startup India Recognition & Tax Exemption | Government Adapter (`STARTUP_INDIA`), Evidence Model & Compliance Rules | `/verification` & `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires authorized DPIIT portal API onboarding |
| **REQ-08** | NSIC Single Point Registration Scheme Verification | Government Adapter (`NSIC`), Evidence Model & Compliance Rules | `/verification` & `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires NSIC portal web service API credentials |
| **REQ-09** | OEM Authorization Code & MAAF Verification | Government Adapter (`OEM_AUTH`), Evidence Model & Compliance Rules | `/verification` & `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Production OEM registry integration / verified manufacturer directory |
| **REQ-10** | DigiLocker Consent-Based Document Verification | Government Adapter (`DIGILOCKER`), Document Intelligence Pipeline | `/verification` & `/documents/upload` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires DigiLocker integration credentials and user consent gateway |
| **REQ-11** | GeM / Central Procurement Debarment List Check | Government Adapter (`DEBARMENT`), Evidence Model & Risk Engine | `/verification` & `/risk` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires central debarment API synchronization |
| **REQ-12** | GeM Seller Profile Rating & Incident History | Government Adapter (`GEM_PROFILE`), Evidence Model & Risk Engine | `/verification` & `/risk` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **MOCK / DEMO MODE** | Requires GeM seller assessment API sandbox access |
| **REQ-13** | Tender-Specific Financial & Technical Specs Verification | Deterministic Rule Engine (`app/services/compliance_engine.py`) | `/tenders/TEN_01` & `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **DEMO PROTOTYPE** | Production custom rule expression parser for complex multi-tier tender clauses |
| **REQ-14** | AI Document Intelligence & Structuring | AI Gateway (`app/services/ai_gateway.py`), Text Parser & Extraction Pipeline | `/documents/[id]` & `/bids/SUB_01` | Pytest `test_phase3_document_ai.py`, Playwright E2E | **DEMO PROTOTYPE** | Production OCR scaling workers for high-volume tenders |
| **REQ-15** | Deterministic Compliance Evaluation Engine | Compliance Engine (`app/services/compliance_engine.py`), Evaluation Snapshots | `/bids/SUB_01` | Pytest `test_phase4_verification_and_compliance.py`, Playwright E2E | **DEMO PROTOTYPE** | Production rule versioning migration pipeline across active tenders |
| **REQ-16** | Multi-Dimensional Evidence Model | Evidence Service (`app/services/evidence_service.py`), 9 Quality Dimensions | `/evidence` & `/bids/SUB_01` | Pytest `test_phase5_evidence_risk_human_review.py`, Playwright E2E | **DEMO PROTOTYPE** | Automated external source freshness polling scheduler |
| **REQ-17** | Advisory Risk Engine & Flagging | Risk Service (`app/services/risk_service.py`), Risk Signals & Scoring | `/risk` & `/bids/SUB_01` | Pytest `test_phase5_evidence_risk_human_review.py`, Playwright E2E | **DEMO PROTOTYPE** | Machine learning anomaly model calibration on historical procurement data |
| **REQ-18** | Human Review Task Queue & Officer Workspace | Officer Review Workspace (`app/services/officer_review_service.py`) | `/human-review` & `/bids/SUB_01` | Pytest `test_phase5_evidence_risk_human_review.py`, Playwright E2E | **DEMO PROTOTYPE** | Integration with enterprise SSO for officer assignments |
| **REQ-19** | Officer Decision Authority & Non-Destructive Override | Officer Decision Service (`app/services/officer_decision_service.py`) | `/bids/SUB_01` | Pytest `test_phase5_evidence_risk_human_review.py`, Playwright E2E | **DEMO PROTOTYPE** | Production digital signing integration for final award decisions |
| **REQ-20** | Four-Eyes Dual Approval Policy Workflow | Four-Eyes Policy Threshold Evaluator (`app/services/officer_decision_service.py`) | `/bids/SUB_01` | Pytest `test_phase5_evidence_risk_human_review.py`, Playwright E2E | **DEMO PROTOTYPE** | Multi-level approval matrix configuration for high-value tenders |
| **REQ-21** | Tamper-Evident SHA-256 Audit Hash Chain | Audit Service (`app/services/audit_service.py`), Canonical Event Logger | `/audit` | Pytest `test_audit_hash_chain.py`, Playwright E2E | **DEMO PROTOTYPE** | Periodic external ledger / timestamping authority anchoring |
| **REQ-22** | Procurement Officer Executive Dashboard | Next.js Command Center (`frontend/app/dashboard/page.tsx`) | `/dashboard` | Playwright E2E (`phase6-procurement.spec.ts`) | **DEMO PROTOTYPE** | Custom analytical reporting widgets |

---

## Architectural Principles Enforcement Summary

1. **AI Non-Authoritative Principle:** AI extraction is advisory. Deterministic compliance rules evaluate structured facts. Evidence and provenance support the evaluation. The authorized human officer retains final procurement decision authority.
2. **Normalized Government Adapter Architecture:** 12 government sources integrated behind uniform `GovernmentSourceAdapter` interfaces. All mock endpoints explicitly state `MOCK / DEMO` integration mode.
3. **Deterministic Evaluation:** Qualification rules perform boolean evaluation without non-deterministic AI variance.
4. **Non-Destructive Manual Overrides:** Point-in-time `EvaluationSnapshot` records original rule outcomes before officer manual override.
5. **Tamper-Evident SHA-256 Audit Lineage:** Every state change generates a canonical JSON payload hashed into a prev_hash linked chain.
