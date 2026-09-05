# Phase 1 Architectural Gap & Implementation Decision Register

**Project:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
**Organization:** Ministry of Petroleum & Natural Gas / CPCL
**Phase:** Phase 1 — Architecture & Design
**Task:** Task 12 — Final Architecture Integration, Consistency, Traceability & Implementation Readiness Review
**Document Status:** DESIGN DRAFT / READ-ONLY VALIDATION READY

---

## 1. Executive Summary

This register catalogs items that intentionally remain open at the conclusion of Phase 1 Architecture & Design. It provides an explicit classification framework to distinguish true **Architecture Gaps** from **Implementation Details**, **External Dependencies**, and **Policy Decisions**.

By explicitly capturing these items rather than falsely claiming universal resolution, Phase 1 establishes clear boundaries and prerequisites for Phase 2 implementation.

---

## 2. Gap Classification Taxonomy

1. **ARCHITECTURE GAP (AG):** High-level structural decision requiring further architectural evaluation before Phase 2 component build.
2. **IMPLEMENTATION DETAIL (ID):** Standard software engineering decision (e.g., choice of library, internal class layout, CSS token value) deferred to Phase 2 coding.
3. **EXTERNAL DEPENDENCY (ED):** External system, API access, cloud subscription, or vendor dependency controlled outside the development team.
4. **POLICY DECISION (PD):** Governance, legal, administrative, or organizational policy decision owned by CPCL / MoPNG / GeM stakeholders.

---

## 3. Comprehensive Open Items Register

| Item ID | Title / Topic | Category | Description & Impact | Resolution Requirement & Owner |
| :--- | :--- | :--- | :--- | :--- |
| **GAP-001** | Production Identity Provider (IdP) Integration | **EXTERNAL DEPENDENCY** | GeM / CPCL enterprise Single Sign-On (SSO) SAML 2.0 / OAuth2 / Keycloak integration. | Obtain production SAML/OAuth2 endpoints and metadata XML from CPCL IT Dept. Owner: CPCL IT. |
| **GAP-002** | Official Government API Credentials & IP Allowlisting | **EXTERNAL DEPENDENCY** | Staging and Production API credentials for GSTN Sandbox, MCA21 API, UDIN Portal, and MSME Udyam. | Formal registration and onboarding on NIC / Govt API gateways. Owner: MoPNG / CPCL Procurement. |
| **GAP-003** | LLM Provider Production Selection & SLA Agreement | **POLICY DECISION** | Choice between self-hosted open-weights LLM (Llama 3 70B on vLLM) vs. Managed Cloud AI (Azure OpenAI / AWS Bedrock). | Data residency approval and cloud AI budget authorization. Owner: CPCL Management & Cyber Cell. |
| **GAP-004** | Document Processing Sandbox Isolation Infrastructure | **IMPLEMENTATION DETAIL** | Specific gVisor vs. Firecracker microVM configuration for parsing untrusted PDFs. | Select microVM technology based on cloud container runner capabilities in Phase 2. Owner: DevOps Team. |
| **GAP-005** | Production Procurement Rule Catalog Compilation | **POLICY DECISION** | Formal translation of CPCL Purchase Manual 2024 and GeM GTC 4.0 into AST Python policy rules. | Policy Rule Committee sign-off on canonical rule definitions. Owner: CPCL Procurement Committee. |
| **GAP-006** | Production Cloud Infrastructure Sizing & Instance Scaling | **IMPLEMENTATION DETAIL** | Sizing PostgreSQL instance (e.g., `db.m6g.xlarge` vs `db.m6g.2xlarge`) and Redis memory capacity. | Perform load testing in Phase 2 staging environment to determine exact capacity. Owner: Performance Lead. |
| **GAP-007** | Automated Antivirus Engine Fine-Tuning | **IMPLEMENTATION DETAIL** | ClamAV signature database update mirror frequency and quarantine storage policy. | Configure ClamAV daemon container parameters in Task 10 base image. Owner: Security Engineer. |
| **GAP-008** | Staging / Sandbox Data Anonymization Pipeline | **IMPLEMENTATION DETAIL** | Scripting synthetic bid document generation and anonymized GSTIN test data for developer testing. | Build synthetic data generator scripts during Phase 2 sprint 1. Owner: QA & Testing Team. |
| **GAP-009** | Production SLA & Operational Runbooks | **POLICY DECISION** | Formalizing incident response timelines (P1 response < 15 mins) and operational escalation matrix. | Draft and approve operational runbooks prior to production launch. Owner: CPCL Operations. |
| **GAP-010** | STQC Cyber Security Audit & Certification | **EXTERNAL DEPENDENCY** | Third-party Indian Government STQC (Standardisation Testing and Quality Certification) audit. | Submit architecture and code for STQC audit before production deployment. Owner: MoPNG Cyber Cell. |

---

## 4. Gap Assessment & Readiness Impact

- **Zero Blocking Architectural Gaps:** No item classified as `ARCHITECTURE GAP (AG)` remains unresolved. The structural blueprint of the platform is complete and sound.
- **External Dependencies & Policy Decisions Identified:** Items `GAP-001`, `GAP-002`, `GAP-003`, `GAP-005`, and `GAP-010` depend on external institutional actions. They do not block Phase 2 technical initialization (which can proceed using mock/sandbox adapters defined in Task 5).
- **Implementation Details Deferred:** Items classified as `IMPLEMENTATION DETAIL (ID)` are standard development choices properly assigned to Phase 2 implementation sprints.
