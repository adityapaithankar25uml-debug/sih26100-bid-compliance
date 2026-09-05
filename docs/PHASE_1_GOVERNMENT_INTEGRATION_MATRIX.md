# Phase 1 — Government Integration Readiness Matrix & Profile Catalog

## Mandatory Qualification Standard

> [!IMPORTANT]
> **GOVERNMENT API AVAILABILITY QUALIFICATION STATEMENT:**
> In accordance with project architecture rules, the **SIH26100 Bid Compliance Verification Platform** qualifies all external government integration capabilities using explicit, non-assumptive language:
>
> *"The system supports integration through an authorized or approved source or integration mechanism, subject to onboarding, credentials, permissions, availability, and applicable policy."*
>
> No statement in this document or platform interface falsely claims that public, open, or unauthenticated APIs are currently available for every government portal.

---

## 1. Executive Master Integration Matrix

The matrix below summarizes the operational readiness, integration mechanisms, authorization dependencies, and fallback strategies for all 12 target integration boundaries:

| # | Target Source | Verification Type | Identifier | Official Source Identified | Official Docs Identified | Integration Mechanism | Authorization Required | Consent Required | Sandbox Available | Production Access Established | Mock Available | Manual Fallback | Expected Evidence | Freshness Basis | Security Class | Known Limitations | Next Onboarding Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **GSTN** | GSTIN Status / Filings | GSTIN / PAN | Yes | Yes | API Setu / GSP Gateway | Yes (GSP MoU) | No | Yes | **NO (CONDITIONAL)** | Yes | Yes | `GSTIN_Verification_Record` | Policy (30D) | RESTRICTED | GSP commercial fee / G2G agreement required | Apply for GSP / API Setu credentials |
| 2 | **Udyam / MSME** | MSME Classification | Udyam Reg No | Yes | Yes | API Setu / MSME Portal | Yes (MSME Dept) | No | Yes | **NO (CONDITIONAL)** | Yes | Yes | `MSME_Udyam_Record` | Policy (90D) | RESTRICTED | Enterprise turnover data restricted | Request API Setu MSME schema access |
| 3 | **PAN / Tax** | PAN Validity / Name Match | PAN | Yes | Yes | NSDL / Income Tax API | Yes (CBDT MoU) | Yes | Yes | **NO (CONDITIONAL)** | Yes | Yes | `PAN_Tax_Verification_Record` | Policy (180D)| CONFIDENTIAL | Tax filing data requires explicit consent | Formalize NSDL/CBDT MoU |
| 4 | **MCA21** | CIN Status / Directors | CIN / DIN | Yes | Yes | MCA G2G Gateway | Yes (MCA Approval)| No | Yes | **NO (CONDITIONAL)** | Yes | Yes | `MCA_Corporate_Record` | Policy (90D) | RESTRICTED | Director DIN lookups rate-limited | Apply for MCA G2G API access |
| 5 | **EPFO** | ECR Filing Regularity | EPFO Code / TRRN| Yes | No | **MANUAL / UNVERIFIED** | Yes (EPFO Dept) | No | No | **NO (MOCK ONLY)** | Yes | Yes | `EPFO_Compliance_Record` | Policy (30D) | RESTRICTED | No public open API confirmed | Use Officer Manual Fallback workflow |
| 6 | **ESIC** | Employer Contribution | ESIC Code | Yes | No | **MANUAL / UNVERIFIED** | Yes (ESIC Dept) | No | No | **NO (MOCK ONLY)** | Yes | Yes | `ESIC_Compliance_Record` | Policy (30D) | RESTRICTED | Portal queries require CAPTCHA | Use Officer Manual Fallback workflow |
| 7 | **Startup India** | DPIIT Recognition | DPIIT Number | Yes | Yes | API Setu Endpoint | Yes (DPIIT / MeitY)| No | Yes | **NO (CONFIRMED_DOCS)**| Yes | Yes | `Startup_DPIIT_Record` | Policy (90D) | PUBLIC | Recognition validity bounded by 10-year rule | Register on API Setu for DPIIT endpoint |
| 8 | **NSIC** | SPRS Status / Capacity | Cert Number | Yes | No | **MANUAL / UNVERIFIED** | Yes (NSIC Dept) | No | No | **NO (MOCK ONLY)** | Yes | Yes | `NSIC_Registration_Record` | Policy (90D) | RESTRICTED | Certificate verification portal based | Use Officer Manual Fallback workflow |
| 9 | **DigiLocker** | Issued Document Proof | URI / Doc ID | Yes | Yes | DigiLocker Requester API| Yes (MeitY Onboard)| Yes | Yes | **NO (CONFIRMED_DOCS)**| Yes | Yes | `DigiLocker_Verified_Document` | Policy (365D)| CONFIDENTIAL | Requires bidder OAuth2 consent flow | Complete DigiLocker Requester Onboarding |
| 10 | **OEM Auth (MAF)**| Manufacturer Auth Letter | MAF Ref / GSTIN | Yes | N/A | Document Verification | Yes (OEM Verification)| No | No | **NO (MANUAL ONLY)** | Yes | Yes | `OEM_Authorization_Record` | Tender Bound | RESTRICTED | Private OEMs lack standard public API | Verify digitally signed MAF or portal |
| 11 | **Debarment Lists**| Multi-Source Blacklist | PAN / GSTIN / Name| Yes | No | **MANUAL / UNVERIFIED** | Yes (Procurement) | No | No | **NO (MANUAL ONLY)** | Yes | Yes | `Debarment_Check_Record` | Policy (1D) | CONFIDENTIAL | Debarment records fragmented across portals| Aggregate departmental lists + Manual Check |
| 12 | **GeM Vendor** | Seller ID / Assessment | GeM Seller ID | Yes | Yes | GeM Platform API | Yes (GeM Onboard) | No | Yes | **NO (CONDITIONAL)** | Yes | Yes | `GeM_Vendor_Record` | Policy (30D) | RESTRICTED | API access restricted to GeM platform partners| Coordinate with GeM SPV integration team |

---

## 2. Source-Specific Integration Profiles

### Profile 1: GST Verification (`SRC_GSTN`)
1. **Verification Purpose:** Validate bidder GSTIN status (Active/Cancelled), filing regularity (GSTR-1, GSTR-3B compliance), legal business name, and registered jurisdiction.
2. **Typical Identifiers:** 15-character GSTIN, 10-character PAN.
3. **Expected Verification Concepts:** Entity Active State, Registration Date, Taxpayer Type (Regular/Composition), Primary Place of Business.
4. **Source Category:** `AUTHORIZED_API_AGGREGATOR`
5. **Authorization Dependency:** API Setu agreement or licensed GST Suvidha Provider (GSP) client credentials.
6. **Readiness Classification:** **CONDITIONAL** (API documented on API Setu; production access dependent on GSP credentials).
7. **Sandbox Availability:** Available on MeitY API Setu sandbox environment.
8. **Mock Strategy:** Synthetic GST adapter returning active/inactive mock JSON payloads matching standard GSTIN schema.
9. **Manual Fallback:** Procurement Officer opens `https://services.gst.gov.in/services/searchtp` manually, searches GSTIN, and attaches portal receipt.
10. **Evidence Requirements:** Immutable `GSTIN_Verification_Record` with portal/gateway transaction reference and payload hash.
11. **Freshness Consideration:** Valid for 30 days (`POL_FRESHNESS_GST_30D`).
12. **Security Classification:** `RESTRICTED`
13. **Failure Scenarios:** GSP rate limits, 503 portal maintenance, canceled GSTIN status.
14. **Human Review Conditions:** Material discrepancy or ambiguity in legal entity name or inactive GST status.

---

### Profile 2: Udyam / MSME Verification (`SRC_UDYAM`)
1. **Verification Purpose:** Verify MSME status (Micro, Small, or Medium Enterprise) to evaluate tender fee/EMD exemption eligibility and procurement purchase preference under Public Procurement Policy for MSEs Order.
2. **Typical Identifiers:** Udyam Registration Number (`UDYAM-XX-00-0000000`).
3. **Expected Verification Concepts:** Enterprise Category (Micro/Small/Medium), Major Activity (Manufacturing/Services), DIC Jurisdiction, Turnover Exemption Qualification.
4. **Source Category:** `GOVERNMENT_API` / `AUTHORIZED_API_AGGREGATOR`
5. **Authorization Dependency:** Onboarding with Ministry of MSME / API Setu integration portal.
6. **Readiness Classification:** **CONDITIONAL**
7. **Sandbox Availability:** Available via API Setu developer portal.
8. **Mock Strategy:** Synthetic Udyam adapter yielding Micro/Small/Medium status payloads.
9. **Manual Fallback:** Officer accesses Udyam Verification Portal (`https://udyamregistration.gov.in/udyam_verify.aspx`), enters Udyam number, and uploads portal verification receipt/screenshot.
10. **Evidence Requirements:** `MSME_Udyam_Record` storing classification details and verification timestamp.
11. **Freshness Consideration:** 90 Days (`POL_FRESHNESS_UDYAM_90D`).
12. **Security Classification:** `RESTRICTED`
13. **Failure Scenarios:** Invalid Udyam format, portal CAPTCHA barrier, expired enterprise classification.
14. **Human Review Conditions:** Discrepancy between declared MSME category and Udyam certificate payload.

---

### Profile 3: PAN / Income Tax Verification (`SRC_PAN`)
1. **Verification Purpose:** Confirm bidder legal name, tax entity classification, active PAN status, and Income Tax return filing compliance under Section 206AB.
2. **Typical Identifiers:** 10-character Alphanumeric PAN.
3. **Expected Verification Concepts:** Active PAN Status, Name on Card, Tax Category (Company/Firm/Individual), Tax Return Filing Timeliness.
4. **Source Category:** `AUTHORIZED_API_AGGREGATOR`
5. **Authorization Dependency:** MoU with CBDT / Income Tax Department or licensed NSDL API partner agreement.
6. **Readiness Classification:** **CONDITIONAL**
7. **Sandbox Availability:** NSDL developer test gateway.
8. **Mock Strategy:** Local synthetic PAN verification handler.
9. **Manual Fallback:** Manual verification via Income Tax e-Filing portal `Verify PAN` utility by Procurement Officer.
10. **Evidence Requirements:** `PAN_Tax_Verification_Record` with NSDL/CBDT verification token.
11. **Freshness Consideration:** 180 Days (`POL_FRESHNESS_PAN_180D`).
12. **Security Classification:** `CONFIDENTIAL` (Strict PII).
13. **Failure Scenarios:** PAN-Aadhaar unlinked status, name mismatch due to abbreviations.
14. **Human Review Conditions:** Material discrepancy or ambiguity in legal entity name.

---

### Profile 4: MCA Corporate Verification (`SRC_MCA`)
1. **Verification Purpose:** Verify corporate existence of Companies and LLPs, check active status, corporate identity number (CIN), authorized/paid-up capital, and Director Identification Numbers (DIN).
2. **Typical Identifiers:** 21-character CIN, 7-character LLPIN, 8-character DIN.
3. **Expected Verification Concepts:** Company Status (Active/Struck Off), Date of Incorporation, Registered Office Address, Paid-up Capital Amount.
4. **Source Category:** `GOVERNMENT_API`
5. **Authorization Dependency:** MCA G2G Gateway integration approval.
6. **Readiness Classification:** **CONDITIONAL**
7. **Sandbox Availability:** Staging environment provided by MCA21 portal team.
8. **Mock Strategy:** Synthetic MCA adapter supplying company master data payloads.
9. **Manual Fallback:** Procurement Officer queries MCA Master Data portal (`https://www.mca.gov.in/mcafoportal/showCheckCompanyMasterData.do`) manually.
10. **Evidence Requirements:** `MCA_Corporate_Record` detailing corporate status and incorporation date.
11. **Freshness Consideration:** 90 Days (`POL_FRESHNESS_MCA_90D`).
12. **Security Classification:** `RESTRICTED`
13. **Failure Scenarios:** MCA portal maintenance windows, company status marked as `DORMANT` or `UNDER_LIQUIDATION`.
14. **Human Review Conditions:** Company status not `ACTIVE` or paid-up capital below tender eligibility threshold.

---

### Profile 5: EPFO Compliance (`SRC_EPFO`)
1. **Verification Purpose:** Verify establishment registration with Employees' Provident Fund Organisation and confirm monthly Electronic Challan cum Return (ECR) filing regularity for labor compliance.
2. **Typical Identifiers:** EPFO Establishment Code (26 characters), TRRN (Temporary Return Reference Number).
3. **Expected Verification Concepts:** Establishment Active Status, Monthly ECR Filing Regularity, Covered Employee Count.
4. **Source Category:** `GOVERNMENT_PORTAL_MANUAL` / `GOVERNMENT_API`
5. **Authorization Dependency:** Formal G2G API agreement with EPFO.
6. **Readiness Classification:** **PRODUCTION ACCESS NOT ESTABLISHED** (Public production API not confirmed; default to Mock & Manual).
7. **Sandbox Availability:** None.
8. **Mock Strategy:** Deterministic mock adapter generating ECR filing records.
9. **Manual Fallback:** Officer searches EPFO Establishment Search Portal (`https://unifiedportal-epfo.epfindia.gov.in/publicSearch/`), inputs establishment code, and downloads ECR payment receipt.
10. **Evidence Requirements:** `EPFO_Compliance_Record` referencing TRRN and payment date.
11. **Freshness Consideration:** 30 Days (`POL_FRESHNESS_EPFO_30D`).
12. **Security Classification:** `RESTRICTED`
13. **Failure Scenarios:** Unannounced EPFO portal updates, missing monthly ECR filing.
14. **Human Review Conditions:** Gap of >2 months in EPFO monthly ECR filings.

---

### Profile 6: ESIC Compliance (`SRC_ESIC`)
1. **Verification Purpose:** Confirm employer registration with Employees' State Insurance Corporation and verify monthly contribution payment records.
2. **Typical Identifiers:** 17-digit ESIC Employer Code.
3. **Expected Verification Concepts:** Employer Registration Status, Monthly Contribution Filing Regularity.
4. **Source Category:** `GOVERNMENT_PORTAL_MANUAL` / `GOVERNMENT_API`
5. **Authorization Dependency:** ESIC Department API authorization.
6. **Readiness Classification:** **PRODUCTION ACCESS NOT ESTABLISHED** (Public production API not confirmed).
7. **Sandbox Availability:** None.
8. **Mock Strategy:** Synthetic ESIC adapter returning contribution compliance JSON.
9. **Manual Fallback:** Officer navigates to ESIC Portal (`https://www.esic.in`), performs Employer Search, and verifies payment status.
10. **Evidence Requirements:** `ESIC_Compliance_Record` storing employer code and payment status.
11. **Freshness Consideration:** 30 Days (`POL_FRESHNESS_ESIC_30D`).
12. **Security Classification:** `RESTRICTED`
13. **Failure Scenarios:** Portal downtime, employer marked inactive.
14. **Human Review Conditions:** Missing ESIC contribution records for active contract period.

---

### Profile 7: Startup India / DPIIT (`SRC_STARTUP`)
1. **Verification Purpose:** Verify DPIIT Recognition for startups to grant statutory relaxation in prior turnover and prior experience criteria (as per MoF public procurement guidelines).
2. **Typical Identifiers:** DPIIT Recognition Certificate Number (`DPIIT00000`).
3. **Expected Verification Concepts:** Recognition Active Status, Entity Type, Exemption Eligibility.
4. **Source Category:** `AUTHORIZED_API_AGGREGATOR`
5. **Authorization Dependency:** API Setu registration for Startup India endpoint.
6. **Readiness Classification:** **CONFIRMED_DOCUMENTATION (Production Access Not Established)** (Official API Setu integration documentation identified; production credentials and live connectivity are not currently established for the platform).
7. **Sandbox Availability:** API Setu Sandbox environment.
8. **Mock Strategy:** Synthetic Startup India adapter.
9. **Manual Fallback:** Manual verification via Startup India Recognition Portal (`https://www.startupindia.gov.in`).
10. **Evidence Requirements:** `Startup_DPIIT_Record` storing recognition certificate metadata.
11. **Freshness Consideration:** 90 Days (`POL_FRESHNESS_STARTUP_90D`).
12. **Security Classification:** `PUBLIC`
13. **Failure Scenarios:** Startup age exceeding 10-year limit, incorporation date mismatch.
14. **Human Review Conditions:** Recognition expired or entity exceeded turnover threshold.

---

### Profile 8: NSIC Registration (`SRC_NSIC`)
1. **Verification Purpose:** Verify Single Point Registration Scheme (SPRS) certificates issued by NSIC for MSME benefits and monetary limit evaluations.
2. **Typical Identifiers:** NSIC Certificate Number, GP Registration Reference.
3. **Expected Verification Concepts:** SPRS Registration Active Status, Store/Item Specifications, Monetary Capacity Limit.
4. **Source Category:** `DOCUMENT_BASED_EVIDENCE` / `GOVERNMENT_API`
5. **Authorization Dependency:** NSIC Portal G2G API access.
6. **Readiness Classification:** **PRODUCTION ACCESS NOT ESTABLISHED** (Public production API not confirmed).
7. **Sandbox Availability:** None.
8. **Mock Strategy:** Synthetic NSIC adapter.
9. **Manual Fallback:** Officer verifies certificate authenticity on NSIC Online Portal (`https://www.nsicspronline.com`).
10. **Evidence Requirements:** `NSIC_Registration_Record` capturing monetary limit and validity period.
11. **Freshness Consideration:** 90 Days (`POL_FRESHNESS_NSIC_90D`).
12. **Security Classification:** `RESTRICTED`
13. **Failure Scenarios:** Expired certificate, bid value exceeding NSIC monetary limit.
14. **Human Review Conditions:** Bid monetary value exceeds NSIC approved limit by >10%.

---

### Profile 9: DigiLocker Document Verification (`SRC_DIGILOCKER`)
1. **Verification Purpose:** Retrieve and verify cryptographically signed digital certificates (e.g., Incorporation Certificates, Tax Certificates, Land/Registration Documents) directly from MeitY DigiLocker repository.
2. **Typical Identifiers:** DigiLocker Document URI, OAuth Access Token.
3. **Expected Verification Concepts:** Document Cryptographic Origin, Issuer Signature Validity, Unaltered PDF SHA-256 Hash.
4. **Source Category:** `GOVERNMENT_DIGITAL_SERVICE`
5. **Authorization Dependency:** Formal onboarding as a Registered Requester on MeitY DigiLocker Portal.
6. **Readiness Classification:** **CONFIRMED_DOCUMENTATION (Production Access Not Established)** (Official MeitY DigiLocker API specification exists; production requester credentials and live connectivity are not currently established for the platform).
7. **Sandbox Availability:** DigiLocker Sandbox Gateway.
8. **Mock Strategy:** Synthetic DigiLocker OAuth and document retrieval adapter.
9. **Manual Fallback:** Officer requests bidder to present original physical certificate or verified portal copy.
10. **Evidence Requirements:** `DigiLocker_Verified_Document` with digital signature validation envelope.
11. **Freshness Consideration:** 365 Days / Certificate Lifetime (`POL_FRESHNESS_DIGILOCKER_365D`).
12. **Security Classification:** `CONFIDENTIAL`
13. **Failure Scenarios:** Bidder denies OAuth consent, issuer repository temporarily unreachable.
14. **Human Review Conditions:** Digital signature validation fails or certificate revoked by issuer.

---

### Profile 10: OEM Authorization Verification (`SRC_OEM_AUTH`)
1. **Verification Purpose:** Validate Manufacturer Authorization Form (MAF) letters issued by Original Equipment Manufacturers to authorized distributors/bidders.
2. **Typical Identifiers:** MAF Serial Reference Number, OEM GSTIN, Tender Reference.
3. **Expected Verification Concepts:** OEM Legal Name, Authorized Territory, Tender Authorization Period, Product Model Coverage.
4. **Source Category:** `DOCUMENT_BASED_EVIDENCE` / `OFFICIAL_CERTIFICATE/DOCUMENT`
5. **Authorization Dependency:** OEM-specific verification portal or direct digital signature verification.
6. **Readiness Classification:** **MANUAL ONLY** (Private OEMs lack standardized public APIs).
7. **Sandbox Availability:** None.
8. **Mock Strategy:** Synthetic OEM verification adapter returning sample MAF validation envelopes.
9. **Manual Fallback:** Procurement Officer sends official verification email or checks OEM partner validation portal.
10. **Evidence Requirements:** `OEM_Authorization_Record` capturing MAF reference, validity dates, and officer confirmation notes.
11. **Freshness Consideration:** Tender Bound (`POL_FRESHNESS_TENDER_BOUND`).
12. **Security Classification:** `RESTRICTED`
13. **Failure Scenarios:** Expired MAF letter, MAF restricted to different geographical region.
14. **Human Review Conditions:** All OEM authorizations require human officer final sign-off.

---

### Profile 11: Multi-Source Debarment Check (`SRC_DEBARMENT`)
1. **Verification Purpose:** Verify whether a bidder, its directors, or its parent entity have been blacklisted, debarred, suspended, or subjected to administrative procurement restrictions by GeM, CPPP, Ministry of Petroleum & Natural Gas, CPCL, or other public procurement authorities.
2. **Typical Identifiers:** PAN, GSTIN, Legal Business Name, Director DINs.
3. **Expected Verification Concepts:** Debarment Status (Clear/Debarred), Issuing Authority, Period of Debarment, Effective From/To Dates.
4. **Source Category:** `GOVERNMENT_PORTAL_MANUAL` / `AUTHORIZED_API_AGGREGATOR`
5. **Authorization Dependency:** Access to departmental debarment registries and CPPP administrative restriction portals.
6. **Readiness Classification:** **MANUAL ONLY** (No single authoritative nationwide debarment API exists).
7. **Sandbox Availability:** None.
8. **Mock Strategy:** Synthetic debarment adapter scanning mock blacklisting database.
9. **Manual Fallback:** Procurement Officer cross-references CPPP Debarment List (`https://eprocure.gov.in`), GeM Blacklist, and CPCL Internal Administrative Restriction Lists.
10. **Evidence Requirements:** `Debarment_Check_Record` combining outputs across all checked registries.
11. **Freshness Consideration:** 1 Day (`POL_FRESHNESS_DEBARMENT_1D`).
12. **Security Classification:** `CONFIDENTIAL`
13. **Failure Scenarios:** Partial name match on common corporate titles, fragmented departmental lists.
14. **Human Review Conditions:** ANY positive or partial match on debarment databases mandates immediate escalation to CPCL Vigilance / Procurement Committee.

---

### Profile 12: GeM Vendor Verification (`SRC_GEM_VENDOR`)
1. **Verification Purpose:** Verify GeM Seller ID status, vendor assessment score, reseller authorization status, and primary product categories registered on Government e-Marketplace.
2. **Typical Identifiers:** GeM Seller ID, GSTIN.
3. **Expected Verification Concepts:** Seller Active Status, Vendor Assessment Completed (Yes/No), Verified Reseller Status.
4. **Source Category:** `GOVERNMENT_API` / `AUTHORIZED_API_AGGREGATOR`
5. **Authorization Dependency:** GeM SPV platform API integration agreement.
6. **Readiness Classification:** **CONDITIONAL**
7. **Sandbox Availability:** GeM Staging Environment.
8. **Mock Strategy:** Synthetic GeM vendor adapter returning seller profile payloads.
9. **Manual Fallback:** Procurement Officer inspects seller profile page directly on GeM Portal (`https://gem.gov.in`).
10. **Evidence Requirements:** `GeM_Vendor_Record` capturing seller ID, assessment status, and registration date.
11. **Freshness Consideration:** 30 Days (`POL_FRESHNESS_GEM_30D`).
12. **Security Classification:** `RESTRICTED`
13. **Failure Scenarios:** Seller account suspended on GeM, pending vendor re-assessment.
14. **Human Review Conditions:** GeM Seller account suspended or vendor assessment status marked incomplete.
