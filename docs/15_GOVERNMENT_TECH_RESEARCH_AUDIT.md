# 15. Government Technology Research Audit

**Document ID:** SIH26100-DOC-015  
**Version:** 1.0.0  
**Phase:** Phase 0 — Technical Ground Truth & Audit  
**Author:** Government Technology Research Auditor  
**Status:** Audit Completed & Ground Truth Verified  

---

## 1. Audit Overview & Methodology

This audit evaluated all Phase 0 research artifacts (`01_PROBLEM_ANALYSIS.md` to `14_PHASE_0_DECISION_LOG.md`) for **SIH Problem Statement 26100** ("AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement" - Ministry of Petroleum & Natural Gas / CPCL).

The goal of this audit is to ensure zero naive assumptions regarding Indian government digital infrastructure, API access, procurement regulations, and AI capabilities.

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## 2. Definitive Classification of Government Data Integrations

| Data Source | Official Govt Entity | API Status | Access Requirements | Audit Tag | Production Fallback Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GSTN** | Goods and Services Tax Network | Restricted | GSP/ASP Partnership + MOIA Approval | `OFFICIAL_DOCUMENTED` / `REQUIRES_GOVERNMENT_APPROVAL` | Offline GSTIN Regex Checksum (`22AAAAA0000A1Z5`) + Mock ASP API Gateway |
| **API Setu** | MeitY / NIC | Restricted | Nodal Officer MoU + Govt Dept Approval | `OFFICIAL_DOCUMENTED` / `REQUIRES_GOVERNMENT_APPROVAL` | Local API Setu Gateway Simulator |
| **MCA21** | Ministry of Corporate Affairs | Unconfirmed Public API | Govt Inter-departmental MoU / KYB Intermediary | `REQUIRES_GOVERNMENT_APPROVAL` / `MOCK_ONLY` | CIN/LLPIN Regex Engine + MCA Master Data PDF Parser |
| **Udyam Portal** | Ministry of MSME | Unconfirmed Public API | Closed Bank/Govt Integration | `REQUIRES_GOVERNMENT_APPROVAL` / `MOCK_ONLY` | Udyam QR Code Reader + OCR + Registration Regex (`UDYAM-XX-00-0000000`) |
| **PAN Verification** | Income Tax Dept / Protean | Commercial / Restricted | Protean/NSDL Agency Agreement | `OFFICIAL_DOCUMENTED` / `REQUIRES_GOVERNMENT_APPROVAL` | PAN Regex Validation + PAN-GSTIN Cross Check |
| **DigiLocker** | MeitY | Public Developer Portal | Partner App Approval (2-4 wks) | `OFFICIAL_DOCUMENTED` / `REQUIRES_GOVERNMENT_APPROVAL` | OAuth 2.0 Staging Sandbox + Direct Signed PDF OCR |
| **EPFO** | Ministry of Labour | Unconfirmed Public API | Internal EPFO Portals Only | `MANUAL_FALLBACK` / `MOCK_ONLY` | TRRN Payment Receipt OCR + ECR Parser |
| **ESIC** | Ministry of Labour | Unconfirmed Public API | Internal Portals Only | `MANUAL_FALLBACK` / `MOCK_ONLY` | Monthly ESI Contribution Receipt OCR |
| **Startup India** | DPIIT | Unconfirmed Public API | Internal Portals Only | `MANUAL_FALLBACK` / `MOCK_ONLY` | Recognition Certificate OCR + Ref Regex |
| **NSIC** | NSIC Ltd. | Unconfirmed Public API | Internal Portals Only | `MANUAL_FALLBACK` / `MOCK_ONLY` | SPRS Exemption Certificate OCR |
| **CPPP / GeM Banned List** | Dept of Expenditure | Web Searchable / Web Lists | Web Published PDF / HTML Search | `CONFIRMED` / `MANUAL_FALLBACK` | Local Banned Vendor Crawler & DB Lookup |
| **DPIIT Local Content (MII)** | DPIIT / Min of Commerce | Policy-based (No Central API) | Document Declarations / CA Certs | `OFFICIAL_DOCUMENTED` / `MANUAL_FALLBACK` | CA Certificate UDIN Parser + Class-I/II Rule Engine |
| **CPCL Vendor Master** | CPCL / IOCL | Enterprise Private | CPCL Internal SAP Network | `CONFIRMED` / `REQUIRES_GOVERNMENT_APPROVAL` | Schema-matched Staging SQLite DB + SAP Mock API |

---

## 3. Corrective Technical Clarifications

### 3.1 Scraping vs. OCR Strategy
Web scraping of government portals (EPFO, ESIC, MCA V3) is **prohibited as a primary strategy** due to Cloudflare WAF, CAPTCHAs, and legal terms of service. The platform mandates **Bidder Document Upload + OCR Parsing + Cryptographic Signature Check** as the primary fallback, reserving API calls for approved sandboxes/mock gateways.

### 3.2 AI vs. Rule Engine Boundary
- **AI / LLM Role:** Strictly bound to **unstructured text extraction** (reading scanned PDFs, extracting clause parameters, parsing CA certificates). Every extracted value MUST include a source citation `(Document, Page, Line Segment)`.
- **Rule Engine Role:** Strictly **deterministic Python logic** (evaluating boolean compliance, verifying mathematical equations, comparing turnover thresholds, checking debarment status).

### 3.3 Make in India (MII) & UDIN Validation
Under DPIIT guidelines, tenders > ₹10 Crore require a CA Certificate with a **Unique Document Identification Number (UDIN)** issued under ICAI rules. The system verifies:
1. Bidder Classification: Class-I (≥50%), Class-II (≥20% & <50%), Non-Local (<20%).
2. UDIN format and ICAI signature validity.

---

## 4. Phase 0 Audit Sign-off

- **All 14 Core Phase 0 Documents Verified:** Ground truth established.
- **Audit Deliverable:** [AUDIT_REPORT.md](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/AUDIT_REPORT.md) generated at workspace root.
- **Application Code Status:** 0 lines of code written, conforming strictly to Phase 0 requirements.
- **Phase Status:** Phase 0 Audit **COMPLETE**. Ready for Phase 1 architecture when requested.

