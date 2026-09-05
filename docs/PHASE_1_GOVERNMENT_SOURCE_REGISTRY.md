# Phase 1 — Government Source Registry Specification

## Overview

The **Government Source Registry** serves as the central administrative catalog and operational directory for all external government integrations supported by the **SIH26100 Bid Compliance Verification Platform**.

It defines the metadata, authorization requirements, supported operating modes, security classifications, freshness policies, and resilience rules for every government source.

> [!CAUTION]
> **NO SECRETS IN REGISTRY:** The Source Registry contains **zero API keys, passwords, client secrets, private keys, or certificates**. All security credentials are stored in external secret management systems (e.g., AWS Secrets Manager / HashiCorp Vault) and injected into adapter runtimes via environment variables at execution time.

---

## 1. Registry Data Schema

Every registered government source record strictly adheres to the following logical metadata schema:

| Metadata Field | Type | Description / Constraints |
| :--- | :--- | :--- |
| `sourceId` | String | Unique registry key (e.g., `"SRC_GSTN"`, `"SRC_UDYAM"`). |
| `sourceName` | String | Official display name (e.g., `"Goods & Services Tax Network"`). |
| `sourceCategory` | Enum | Source category enum (`GOVERNMENT_API`, `GOVERNMENT_DIGITAL_SERVICE`, `AUTHORIZED_API_AGGREGATOR`, etc.). |
| `authority` | String | Responsible ministry/department (e.g., `"Ministry of Finance"`). |
| `documentationReference` | String | Link or reference to official public documentation/gazette. |
| `verificationTypes` | Array[String] | Supported compliance verification types (e.g., `["GSTIN_STATUS", "TAX_FILING_RECORDS"]`). |
| `authorizationRequired` | Boolean | True if formal department MOU, onboarding, or client approval is needed. |
| `consentRequired` | Boolean | True if explicit bidder consent delegation token is required. |
| `productionAvailable` | Boolean | True if an authorized production endpoint is active and configured. |
| `sandboxAvailable` | Boolean | True if an official sandbox testing endpoint is accessible. |
| `mockAvailable` | Boolean | True if a local synthetic mock adapter is implemented. |
| `manualFallbackAvailable` | Boolean | Always `True`; manual officer fallback is mandatory for all sources. |
| `adapterStatus` | Enum | Status of adapter software (`ACTIVE`, `DEPRECATED`, `EXPERIMENTAL`, `DISABLED`). |
| `adapterVersion` | String | SemVer string of active adapter class (e.g., `"1.0.0"`). |
| `supportedIdentifiers` | Array[String] | Array of identifier keys accepted (e.g., `["GSTIN", "PAN"]`). |
| `freshnessPolicyReference` | String | Policy key governing maximum cache retention (e.g., `"POL_FRESHNESS_GST_30D"`). |
| `securityClassification` | Enum | Sensitivity classification (`CONFIDENTIAL`, `RESTRICTED`, `PUBLIC`). |
| `dataHandlingPolicy` | String | Rules governing PII masking, tokenization, and encryption. |
| `rateLimitPolicy` | JSON Object | Max requests per minute, burst allowance, and window size. |
| `timeoutPolicy` | JSON Object | Connect timeout (ms) and Read timeout (ms). |
| `retryPolicy` | JSON Object | Max retries, initial backoff (ms), and max backoff (ms). |
| `lastReviewedAt` | Timestamp | ISO 8601 timestamp of last architectural review. |
| `reviewedBy` | String | User ID or role of reviewing architect. |
| `operationalStatus` | Enum | Health status (`OPERATIONAL`, `DEGRADED`, `MAINTENANCE`, `OFFLINE`). |

---

## 2. Master Source Registry Catalog

Below is the frozen Phase 1 registry defining the 12 target government integration boundaries:

### 2.1 GST Integration (`SRC_GSTN`)
* **Source Name:** Goods & Services Tax Network (GSTN)
* **Authority:** Department of Revenue, Ministry of Finance
* **Category:** `AUTHORIZED_API_AGGREGATOR` (via API Setu / GSP Gateway)
* **Supported Verification Types:** `GSTIN_ACTIVE_STATUS`, `FILING_REGULARITY`, `BUSINESS_JURISDICTION`
* **Identifiers:** `GSTIN`, `PAN`
* **Authorization Required:** Yes (GSP registration or API Setu approval)
* **Consent Required:** No (Public status lookup)
* **Modes Supported:** `LIVE` (conditional), `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 30 Days (`POL_FRESHNESS_GST_30D`)
* **Security Classification:** `RESTRICTED`
* **Timeout / Retries:** Connect 3000ms, Read 5000ms, Retries 3 (Exponential Backoff)

### 2.2 Udyam / MSME Integration (`SRC_UDYAM`)
* **Source Name:** Udyam Registration Portal
* **Authority:** Ministry of Micro, Small and Medium Enterprises
* **Category:** `GOVERNMENT_API` / `AUTHORIZED_API_AGGREGATOR`
* **Supported Verification Types:** `MSME_REGISTRATION_STATUS`, `ENTERPRISE_CLASSIFICATION` (Micro/Small/Medium), `ANNUAL_TURNOVER_VERIFICATION`
* **Identifiers:** `UDYAM_REGISTRATION_NUMBER`
* **Authorization Required:** Yes (API Setu / MSME portal onboarding)
* **Consent Required:** No
* **Modes Supported:** `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 90 Days (`POL_FRESHNESS_UDYAM_90D`)
* **Security Classification:** `RESTRICTED`
* **Timeout / Retries:** Connect 3000ms, Read 5000ms, Retries 3

### 2.3 PAN / Income Tax Integration (`SRC_PAN`)
* **Source Name:** Income Tax Department e-Filing Portal / NSDL API
* **Authority:** Central Board of Direct Taxes (CBDT), Ministry of Finance
* **Category:** `AUTHORIZED_API_AGGREGATOR`
* **Supported Verification Types:** `PAN_VALIDITY`, `ENTITY_NAME_MATCH`, `TAX_RETURN_FILING_STATUS`
* **Identifiers:** `PAN`
* **Authorization Required:** Yes (Formal NSDL/Income Tax department agreement)
* **Consent Required:** Yes (Bidder PAN verification consent)
* **Modes Supported:** `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 180 Days (`POL_FRESHNESS_PAN_180D`)
* **Security Classification:** `CONFIDENTIAL`
* **Timeout / Retries:** Connect 2500ms, Read 4000ms, Retries 2

### 2.4 MCA Corporate Filings (`SRC_MCA`)
* **Source Name:** Ministry of Corporate Affairs (MCA21 Portal)
* **Authority:** Ministry of Corporate Affairs
* **Category:** `GOVERNMENT_API`
* **Supported Verification Types:** `CIN_ACTIVE_STATUS`, `DIRECTOR_DIN_VERIFICATION`, `PAID_UP_CAPITAL`, `FINANCIAL_FILING_TIMELINESS`
* **Identifiers:** `CIN`, `DIN`, `LLPIN`
* **Authorization Required:** Yes (MCA G2G integration gateway approval)
* **Consent Required:** No
* **Modes Supported:** `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 90 Days (`POL_FRESHNESS_MCA_90D`)
* **Security Classification:** `RESTRICTED`
* **Timeout / Retries:** Connect 4000ms, Read 8000ms, Retries 2

### 2.5 EPFO Compliance (`SRC_EPFO`)
* **Source Name:** Employees' Provident Fund Organisation Portal
* **Authority:** Ministry of Labour and Employment
* **Category:** `GOVERNMENT_API` / `GOVERNMENT_PORTAL_MANUAL`
* **Supported Verification Types:** `EPFO_REGISTRATION_STATUS`, `MONTHLY_ECR_FILING_VERIFICATION`, `ACTIVE_MEMBER_COUNT`
* **Identifiers:** `EPFO_ESTABLISHMENT_CODE`, `TRRN`
* **Authorization Required:** Yes
* **Consent Required:** No
* **Modes Supported:** `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 30 Days (`POL_FRESHNESS_EPFO_30D`)
* **Security Classification:** `RESTRICTED`
* **Timeout / Retries:** Connect 3000ms, Read 6000ms, Retries 2

### 2.6 ESIC Compliance (`SRC_ESIC`)
* **Source Name:** Employees' State Insurance Corporation Portal
* **Authority:** Ministry of Labour and Employment
* **Category:** `GOVERNMENT_API` / `GOVERNMENT_PORTAL_MANUAL`
* **Supported Verification Types:** `ESIC_REGISTRATION_STATUS`, `CONTRIBUTION_PAYMENT_VERIFICATION`
* **Identifiers:** `ESIC_EMPLOYER_CODE`
* **Authorization Required:** Yes
* **Consent Required:** No
* **Modes Supported:** `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 30 Days (`POL_FRESHNESS_ESIC_30D`)
* **Security Classification:** `RESTRICTED`
* **Timeout / Retries:** Connect 3000ms, Read 6000ms, Retries 2

### 2.7 Startup India / DPIIT (`SRC_STARTUP`)
* **Source Name:** Startup India Hub / DPIIT Portal
* **Authority:** Department for Promotion of Industry and Internal Trade (DPIIT)
* **Category:** `AUTHORIZED_API_AGGREGATOR`
* **Supported Verification Types:** `DPIIT_RECOGNITION_STATUS`, `EXEMPTION_ELIGIBILITY` (EMD/Prior Experience)
* **Identifiers:** `DPIIT_RECOGNITION_NUMBER`
* **Authorization Required:** Yes (API Setu endpoint)
* **Consent Required:** No
* **Modes Supported:** `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 90 Days (`POL_FRESHNESS_STARTUP_90D`)
* **Security Classification:** `PUBLIC`
* **Timeout / Retries:** Connect 2500ms, Read 4000ms, Retries 3

### 2.8 NSIC Registration (`SRC_NSIC`)
* **Source Name:** National Small Industries Corporation Portal
* **Authority:** Ministry of Micro, Small and Medium Enterprises
* **Category:** `GOVERNMENT_API` / `DOCUMENT_BASED_EVIDENCE`
* **Supported Verification Types:** `SINGLE_POINT_REGISTRATION_STATUS`, `MONETARY_LIMIT_VERIFICATION`
* **Identifiers:** `NSIC_CERTIFICATE_NUMBER`
* **Authorization Required:** Yes
* **Consent Required:** No
* **Modes Supported:** `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 90 Days (`POL_FRESHNESS_NSIC_90D`)
* **Security Classification:** `RESTRICTED`
* **Timeout / Retries:** Connect 3000ms, Read 5000ms, Retries 2

### 2.9 DigiLocker Document Verification (`SRC_DIGILOCKER`)
* **Source Name:** DigiLocker National Digital Document Wallet
* **Authority:** Ministry of Electronics and Information Technology (MeitY)
* **Category:** `GOVERNMENT_DIGITAL_SERVICE`
* **Supported Verification Types:** `ISSUED_CERTIFICATE_VERIFICATION`, `CRYPTOGRAPHIC_ORIGIN_PROOF`
* **Identifiers:** `DIGILOCKER_URI`, `DOC_ID`
* **Authorization Required:** Yes (DigiLocker Requester Portal onboarding)
* **Consent Required:** Yes (OAuth2 User Consent Flow)
* **Modes Supported:** `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 365 Days / Certificate Lifetime (`POL_FRESHNESS_DIGILOCKER_365D`)
* **Security Classification:** `CONFIDENTIAL`
* **Timeout / Retries:** Connect 3000ms, Read 6000ms, Retries 2

### 2.10 OEM Authorization Verification (`SRC_OEM_AUTH`)
* **Source Name:** OEM Manufacturer Portal / Direct Verification Service
* **Authority:** OEM Manufacturer (Private Entity)
* **Category:** `DOCUMENT_BASED_EVIDENCE` / `OFFICIAL_CERTIFICATE/DOCUMENT`
* **Supported Verification Types:** `MAF_VALIDITY`, `TERRITORY_AUTHORIZATION`, `TENDER_SPECIFIC_AUTHORIZATION`
* **Identifiers:** `MAF_REFERENCE_NUMBER`, `OEM_GSTIN`
* **Authorization Required:** Yes (Vendor/OEM agreement)
* **Consent Required:** No
* **Modes Supported:** `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** Tender Specific (`POL_FRESHNESS_TENDER_BOUND`)
* **Security Classification:** `RESTRICTED`
* **Timeout / Retries:** Connect 3000ms, Read 5000ms, Retries 2

### 2.11 Multi-Source Debarment Check (`SRC_DEBARMENT`)
* **Source Name:** GeM / CPPP / Departmental Blacklisting Registries
* **Authority:** Ministry of Finance / GeM Portal / CPCL Procurement Vigilance
* **Category:** `GOVERNMENT_PORTAL_MANUAL` / `AUTHORIZED_API_AGGREGATOR`
* **Supported Verification Types:** `NATIONAL_DEBARMENT_CHECK`, `CPPP_BLACKLIST_SEARCH`, `ORGANIZATION_DEBARMENT`
* **Identifiers:** `PAN`, `GSTIN`, `LEGAL_NAME`
* **Authorization Required:** Yes
* **Consent Required:** No
* **Modes Supported:** `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 1 Day (`POL_FRESHNESS_DEBARMENT_1D`)
* **Security Classification:** `CONFIDENTIAL`
* **Timeout / Retries:** Connect 2500ms, Read 4000ms, Retries 3

### 2.12 GeM Vendor Verification (`SRC_GEM_VENDOR`)
* **Source Name:** Government e-Marketplace (GeM) Vendor Registry
* **Authority:** GeM SPV, Ministry of Commerce and Industry
* **Category:** `GOVERNMENT_API` / `AUTHORIZED_API_AGGREGATOR`
* **Supported Verification Types:** `GEM_SELLER_ID_STATUS`, `ASSESSMENT_STATUS`, `RESCELLER_VERIFICATION`
* **Identifiers:** `GEM_SELLER_ID`, `GSTIN`
* **Authorization Required:** Yes (GeM platform API partner onboarding)
* **Consent Required:** No
* **Modes Supported:** `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`
* **Freshness Policy:** 30 Days (`POL_FRESHNESS_GEM_30D`)
* **Security Classification:** `RESTRICTED`
* **Timeout / Retries:** Connect 3000ms, Read 5000ms, Retries 3

---

## 3. Dynamic Source Resolution Logic

When an application workflow requests compliance verification for a requirement:

```
[Verification Request Received]
              │
              ▼
┌────────────────────────────────────────────────────────┐
│ Query Source Registry by sourceId                      │
└────────────────────────────────────────────────────────┘
              │
              ├──────────────────────────┐
              ▼ (Source Found)           ▼ (Source Disabled/Missing)
┌───────────────────────────┐   ┌───────────────────────────┐
│ Inspect Operational Status│   │ Fast-Fail: SOURCE_DISABLED│
└───────────────────────────┘   └───────────────────────────┘
              │
              ├──────────────────────────┐
              ▼ (OPERATIONAL)            ▼ (OFFLINE/MAINTENANCE)
┌───────────────────────────┐   ┌───────────────────────────┐
│ Select Adapter for Active │   │ Route Request to          │
│ System Operating Mode     │   │ MANUAL_FALLBACK Workflow  │
└───────────────────────────┘   └───────────────────────────┘
```
