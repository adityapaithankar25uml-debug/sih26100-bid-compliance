# 04 — Government Integration Matrix

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05  
**Research Date:** 2026-09-05  
**Disclaimer:** This matrix reflects research as of September 2026. Government API availability changes frequently. All claims are backed by sources in `13_SOURCE_REGISTER.md`.

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## Integration Status Legend

| Status | Meaning |
|--------|---------|
| ✅ AVAILABLE | Official API exists and is accessible (with appropriate registration/approval) |
| ⚠️ RESTRICTED | API exists but requires specific authorization, GSP partnership, or government approval |
| ❌ UNCONFIRMED / RESTRICTED | No suitable publicly documented/publicly accessible API was confirmed for our intended workflow during Phase 0 research; portal is web-only or requires government authorization |
| 🔄 VIA INTERMEDIARY | Available only through authorized third-party providers |
| 📋 MANUAL ONLY | Verification must be performed manually through web portals |

---

## 1. GeM (Government e-Marketplace)

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for our intended workflow during Phase 0 research |
| **Public?** | No |
| **Authentication required?** | N/A |
| **Registration required?** | N/A |
| **Approval required?** | N/A — System-to-system integration requires formal arrangement with GeM administration |
| **Sandbox available?** | No |
| **Production access?** | No (for external parties) |
| **Available through API Setu?** | Not as a public API; specific datasets may be shared through government-to-government channels |
| **Data obtainable** | Tender details (via manual download from gem.gov.in), GeM category codes, published bid information |
| **Data NOT obtainable** | Bid submission data, bidder profiles, internal evaluation data, transaction history |
| **User consent required?** | N/A |
| **Legal restrictions** | GeM ToS prohibits scraping; data is property of Government of India |
| **SIH prototype access?** | ❌ NO |
| **Correct fallback** | Manual tender document upload by procurement officer; synthetic tender data for demo |
| **Architecture mode** | MOCK for SIH → MANUAL for production (until official integration arranged) |

**Source:** GeM Portal (gem.gov.in); no developer documentation found.  
**CONFIRMED:** No suitable publicly documented/publicly accessible API was confirmed for GeM during Phase 0 research. Any claims of open public GeM API access are unverified.

---

## 2. API Setu (apisetu.gov.in)

| Question | Answer |
|----------|--------|
| **Official API exists?** | ✅ YES — API Setu is itself the API marketplace |
| **Public?** | Registration required to subscribe to specific APIs |
| **Authentication required?** | Yes — OAuth 2.0, API Keys |
| **Registration required?** | Yes — Organization registration on apisetu.gov.in |
| **Approval required?** | Yes — Each API subscription requires publisher approval |
| **Sandbox available?** | Yes — Sandbox environments available for testing |
| **Production access?** | Yes — After approval by API publisher |
| **Data obtainable** | Varies by subscribed API — Document verification (DigiLocker), identity verification, business data |
| **Data NOT obtainable** | Not all government data is on API Setu; each department decides what to publish |
| **User consent required?** | Yes — For Document APIs (user-specific data) |
| **Legal restrictions** | Data usage limited to stated purpose; DPDP Act compliance required |
| **SIH prototype access?** | ⚠️ UNCERTAIN — Registration possible; approval timeline uncertain for hackathon |
| **Correct fallback** | MOCK adapters simulating API Setu responses |
| **Architecture mode** | SANDBOX where approved → MOCK for SIH demo |

**Source:** apisetu.gov.in; docs.apisetu.gov.in  
**OFFICIAL_DOCUMENTED:** API Setu hosts 4,200+ APIs across categories. Partner registration via partners.apisetu.gov.in.

---

## 3. DigiLocker

| Question | Answer |
|----------|--------|
| **Official API exists?** | ✅ YES — Partner API via partners.apisetu.gov.in |
| **Public?** | No — Partner registration required |
| **Authentication required?** | Yes — OAuth 2.0 with OpenID Connect |
| **Registration required?** | Yes — As "Requester" on DigiLocker Partner Portal |
| **Approval required?** | Yes — Verification call + agreement signing required |
| **Sandbox available?** | Yes — Sandbox environment available post-registration |
| **Production access?** | Yes — After partner approval |
| **Data obtainable** | Government-issued digital documents: PAN, driving license, academic certificates, Aadhaar (with consent) |
| **Data NOT obtainable** | Documents not yet digitized by issuers; private sector documents |
| **User consent required?** | Yes — Explicit user (bidder) consent via OAuth flow |
| **Legal restrictions** | DPDP Act; user must grant consent; data cannot be stored beyond stated purpose |
| **SIH prototype access?** | ⚠️ UNLIKELY within hackathon timeline — approval process involves verification call and agreement |
| **Correct fallback** | MOCK adapter simulating DigiLocker document fetch; clearly labelled |
| **Architecture mode** | MOCK for SIH → SANDBOX/LIVE for production |

**Source:** partners.apisetu.gov.in; DigiLocker documentation  
**OFFICIAL_DOCUMENTED:** DigiLocker API requires formal partner onboarding. Cannot be self-service within days.  
**REQUIRES_GOVERNMENT_APPROVAL:** Yes.

---

## 4. GSTN (GST Network)

| Question | Answer |
|----------|--------|
| **Official API exists?** | ✅ YES — Via GST Developer Portal (developer.gst.gov.in) |
| **Public?** | Partially — "Search Taxpayer" is semi-public; full APIs require GSP partnership |
| **Authentication required?** | Yes — API keys via GSP |
| **Registration required?** | Yes — Must partner with a licensed GSP or register as an ASP |
| **Approval required?** | Yes — GSP authorization required for most APIs |
| **Sandbox available?** | Yes — Via GSPs (e.g., MasterGST, others) |
| **Production access?** | Yes — Through authorized GSP only |
| **Available through API Setu?** | Service APIs for GSTIN verification available |
| **Data obtainable** | GSTIN status, legal name, trade name, registration date, business type, filing status, return filing summary |
| **Data NOT obtainable** | Detailed return data without taxpayer consent + OTP; private financial details |
| **User consent required?** | Yes — For detailed data access (OTP-based consent) |
| **Legal restrictions** | Taxpayer must enable API access in their profile; enhanced security notifications active since 2025 |
| **SIH prototype access?** | ⚠️ POSSIBLE via GSP sandbox — but requires GSP partnership |
| **Correct fallback** | MOCK adapter; manual verification via gst.gov.in Search Taxpayer |
| **Architecture mode** | SANDBOX (if GSP sandbox obtained) → MOCK for SIH demo |

**Source:** developer.gst.gov.in; gstn.org.in  
**OFFICIAL_DOCUMENTED:** GSTIN basic lookup is publicly accessible on gst.gov.in (with CAPTCHA). Programmatic access requires GSP.  
**REQUIRES_GOVERNMENT_APPROVAL:** GSP partnership or ASP registration.

---

## 5. MCA (Ministry of Corporate Affairs)

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for MCA company verification during Phase 0 research |
| **Public?** | No |
| **Authentication required?** | N/A |
| **Registration required?** | N/A |
| **Approval required?** | N/A |
| **Sandbox available?** | No (only through third-party providers) |
| **Production access?** | No (official) |
| **Available through API Setu?** | Not confirmed as a public API |
| **Data obtainable (via portal)** | Company master data, CIN details, director details, charges, compliance status (manual lookup) |
| **Data NOT obtainable (programmatically)** | Same data — no API for automated access |
| **User consent required?** | No — Company registration data is public record |
| **Legal restrictions** | DPDP Act considerations for director PII |
| **SIH prototype access?** | ❌ NO — No official API |
| **Correct fallback** | MOCK adapter with realistic company data; manual verification via mca.gov.in |
| **Architecture mode** | MOCK for SIH → 🔄 VIA INTERMEDIARY (Decentro/SurePass) or MANUAL for production |

**Source:** mca.gov.in; research confirms no official public API  
**CONFIRMED:** No suitable publicly documented/publicly accessible API was confirmed for MCA company verification during Phase 0 research. Third-party providers (Decentro, SurePass, AuthBridge) offer APIs that access MCA data.  
**ASSUMPTION:** For production, a third-party KYB provider would be needed for automated MCA verification.

---

## 6. Udyam/MSME Registration

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for Udyam/MSME verification during Phase 0 research |
| **Public?** | No |
| **Authentication required?** | N/A |
| **Registration required?** | N/A |
| **Approval required?** | N/A |
| **Sandbox available?** | No |
| **Production access?** | No |
| **Available through API Setu?** | Not confirmed as a standalone public API |
| **Data obtainable (via portal)** | Udyam Registration Number verification, enterprise name, classification (Micro/Small/Medium), activity type |
| **Data NOT obtainable** | Bulk verification; historical registration data |
| **User consent required?** | No — Registration data is public record on udyamregistration.gov.in |
| **Legal restrictions** | Standard data protection |
| **SIH prototype access?** | ❌ NO |
| **Correct fallback** | MOCK adapter; manual verification via udyamregistration.gov.in |
| **Architecture mode** | MOCK for SIH → 🔄 VIA INTERMEDIARY or MANUAL for production |

**Source:** udyamregistration.gov.in; msme.gov.in  
**CONFIRMED:** No suitable publicly documented/publicly accessible API was confirmed for Udyam/MSME verification during Phase 0 research. Third-party KYB providers offer Udyam verification APIs by interfacing with official records.

---

## 7. Income Tax / PAN Verification

| Question | Answer |
|----------|--------|
| **Official API exists?** | ✅ YES — Protean eGov Technologies (formerly NSDL) provides OPV API |
| **Public?** | ⚠️ RESTRICTED — For eligible entities only |
| **Authentication required?** | Yes — Digital Signature Certificate (Class 2/3) + User ID |
| **Registration required?** | Yes — Must register with Protean eGov |
| **Approval required?** | Yes — Eligibility criteria must be met |
| **Sandbox available?** | Yes (through Protean) |
| **Production access?** | Yes — After registration and DSC procurement |
| **Available through API Setu?** | PAN verification available in API Setu catalog |
| **Data obtainable** | PAN validity, name on PAN, status (Active/Inactive/Deactivated) |
| **Data NOT obtainable** | Income tax returns, financial details, assessment data |
| **User consent required?** | No — PAN is a business identifier; basic verification doesn't require consent |
| **Legal restrictions** | Must be an eligible entity; requests must be digitally signed |
| **SIH prototype access?** | ❌ UNLIKELY — Registration and DSC procurement timeline |
| **Correct fallback** | MOCK adapter; PAN format validation (deterministic) |
| **Architecture mode** | MOCK for SIH → LIVE (via Protean or API Setu) for production |

**Source:** Protean eGov Technologies (protean-india.com); NSDL documentation  
**OFFICIAL_DOCUMENTED:** Official PAN verification API exists via Protean. Requires entity registration + Class 2/3 DSC.  
**REQUIRES_GOVERNMENT_APPROVAL:** Entity registration with Protean.

---

## 8. EPFO (Employees' Provident Fund Organisation)

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for EPFO compliance verification during Phase 0 research |
| **Public?** | No |
| **Authentication required?** | N/A |
| **Registration required?** | N/A (for verification) |
| **Approval required?** | N/A |
| **Sandbox available?** | No |
| **Production access?** | No |
| **Available through API Setu?** | Citizen-centric UAN data may be available; employer compliance verification is not |
| **Data obtainable (via portal)** | Establishment search, e-Report Card, TRRN query (manual only) |
| **Data NOT obtainable** | Employer compliance status via API; contribution history via API |
| **User consent required?** | Yes — For employee-level data |
| **Legal restrictions** | Employee PII protected; employer compliance data access restricted |
| **SIH prototype access?** | ❌ NO |
| **Correct fallback** | MANUAL verification by procurement officer; document upload (PF registration certificate) |
| **Architecture mode** | MANUAL for SIH → MANUAL for production (unless API becomes available) |

**Source:** epfindia.gov.in; EPFO Unified Employer Portal  
**CONFIRMED:** No suitable publicly documented/publicly accessible API was confirmed for EPFO during Phase 0 research. Verification requires manual portal access or third-party providers.

---

## 9. ESIC (Employees' State Insurance Corporation)

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for ESIC during Phase 0 research |
| **Public?** | No |
| **Authentication required?** | N/A |
| **Registration required?** | N/A |
| **Approval required?** | N/A |
| **Sandbox available?** | No |
| **Production access?** | No |
| **Available through API Setu?** | Not confirmed |
| **Data obtainable (via portal)** | Employer search by State/District/Employer Code (manual) |
| **Data NOT obtainable** | Compliance status, contribution history via API |
| **User consent required?** | Yes — For employee-level data |
| **Legal restrictions** | Data privacy; employer data access restricted |
| **SIH prototype access?** | ❌ NO |
| **Correct fallback** | MANUAL verification; document upload (ESIC registration certificate) |
| **Architecture mode** | MANUAL for SIH and production |

**Source:** esic.gov.in; portal.esic.gov.in  
**CONFIRMED:** No suitable publicly documented/publicly accessible API was confirmed for ESIC during Phase 0 research. The official Employer Search feature on esic.gov.in is the only verification method.

---

## 10. Startup India (DPIIT Recognition)

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for Startup India during Phase 0 research |
| **Public?** | No |
| **Authentication required?** | N/A |
| **Registration required?** | N/A |
| **Approval required?** | N/A |
| **Sandbox available?** | No |
| **Production access?** | No |
| **Data obtainable (via portal)** | Certificate validation (by certificate number + entity name); recognition mapping verification (DIPP + CIN + PAN + OTP) |
| **Data NOT obtainable** | Bulk verification; API-based recognition status |
| **User consent required?** | Yes — OTP-based verification for recognition mapping |
| **Legal restrictions** | Standard data protection |
| **SIH prototype access?** | ❌ NO |
| **Correct fallback** | MANUAL verification via startupindia.gov.in; uploaded certificate with AI field extraction |
| **Architecture mode** | MANUAL for SIH and production |

**Source:** startupindia.gov.in  
**CONFIRMED:** No suitable publicly documented/publicly accessible API was confirmed for Startup India during Phase 0 research. Web-based certificate validation and recognition mapping verification available.

---

## 11. NSIC (National Small Industries Corporation)

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for NSIC during Phase 0 research |
| **Public?** | No |
| **Authentication required?** | N/A |
| **Registration required?** | N/A |
| **Approval required?** | N/A |
| **Sandbox available?** | No |
| **Production access?** | No |
| **Data obtainable** | Registration validity (manual verification with NSIC field office) |
| **Data NOT obtainable** | Programmatic verification of any kind |
| **User consent required?** | No |
| **Legal restrictions** | Standard |
| **SIH prototype access?** | ❌ NO |
| **Correct fallback** | Document upload; AI extraction of certificate fields; MANUAL verification |
| **Architecture mode** | MANUAL |

**Source:** nsic.co.in; nsicspronline.com  
**CONFIRMED:** No suitable publicly documented/publicly accessible API was confirmed for NSIC during Phase 0 research. Certificate verification requires contact with issuing NSIC field office.

---

## 12. CPPP / eProcurement

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for CPPP during Phase 0 research |
| **Public?** | No |
| **Authentication required?** | N/A |
| **Registration required?** | N/A |
| **Approval required?** | N/A (NIC manages the platform) |
| **Sandbox available?** | No |
| **Production access?** | No |
| **Data obtainable (via portal)** | Active tenders, corrigendum, bid awards, MIS reports (manual search) |
| **Data NOT obtainable** | Programmatic tender search; bid details via API |
| **Debarment list available?** | Yes — CPPP has a Debarment List searchable by Login ID or PAN |
| **User consent required?** | No |
| **Legal restrictions** | Anti-scraping; government data |
| **SIH prototype access?** | ❌ NO API; debarment list is manually searchable |
| **Correct fallback** | Manual tender import; CPPP debarment list via manual check |
| **Architecture mode** | MANUAL |

**Source:** eprocure.gov.in  
**CONFIRMED:** No suitable publicly documented/publicly accessible API was confirmed for CPPP during Phase 0 research. CPPP debarment list is a key resource for blacklisting verification (searchable by PAN).

---

## 13. Debarment / Blacklisting Sources

| Source | Type | Access Method |
|--------|------|--------------|
| CPPP Debarment List | Centralized (partial) | Manual search by Login ID or PAN on eprocure.gov.in |
| Department-specific lists | Fragmented | Individual ministry/PSU websites |
| CPCL holiday/banned list | Organization-specific | CPCL procurement portal or internal records |
| CVC guidelines | Policy | cvc.gov.in — guidelines on blacklisting process |

**CONFIRMED:** No single authoritative nationwide debarment database covering all relevant procurement entities was confirmed. Verification requires checking multiple sources.  
**ASSUMPTION:** The system should aggregate debarment data from CPPP + CPCL-specific list + manual entry. Support periodic refresh.

---

## 14. DPIIT / Make in India

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for local content verification |
| **Public?** | Policy documents are public (dpiit.gov.in) |
| **Data obtainable** | Policy text, order notifications, sector-specific thresholds |
| **Data NOT obtainable** | Automated local content verification; bidder-specific local content certification |
| **SIH prototype access?** | Policy documents can be referenced; no API |
| **Correct fallback** | Rule engine implementing policy rules; bidder self-declaration with AI extraction |
| **Architecture mode** | DETERMINISTIC RULE ENGINE |

**Source:** dpiit.gov.in — Public Procurement (Preference to Make in India) Order 2017, amended July 2024  
**OFFICIAL_DOCUMENTED:** Make in India compliance is policy-based, not API-based. Our system must implement the policy rules and support versioning.

---

## 15. BIS (Bureau of Indian Standards)

| Question | Answer |
|----------|--------|
| **Official API exists?** | ❌ UNCONFIRMED — No suitable publicly documented/publicly accessible API was confirmed for BIS during Phase 0 research |
| **Public?** | No |
| **Data obtainable (via portal/app)** | ISI licence verification (CM/L number), CRS R-number verification, HUID verification (via BIS Care App and manakonline.in) |
| **SIH prototype access?** | ❌ NO API |
| **Correct fallback** | MANUAL verification; document upload |
| **Architecture mode** | MANUAL |

**Source:** manakonline.in; BIS Care App  
**CONFIRMED:** BIS provides manual verification tools (web portal and mobile app) but no suitable public API was confirmed.

---

## 16. CPCL Procurement/Tender Sources

| Question | Answer |
|----------|--------|
| **e-Procurement portal** | cpcletenders.nic.in (NIC-managed) |
| **GeM integration** | CPCL uses GeM for applicable procurements |
| **Tender format** | NIT documents, BOQ, technical specifications via NIC portal |
| **API available?** | ❌ UNCONFIRMED — No suitable public API confirmed |
| **Vendor registration** | Online via NIC portal; DSC required |
| **Correct fallback** | Manual tender document upload; CPCL-specific requirement templates |
| **Architecture mode** | MANUAL import |

**Source:** cpcletenders.nic.in; cpcl.co.in  
**CONFIRMED:** CPCL uses NIC's e-procurement platform. No suitable public API was confirmed for external integration.

---

## Summary Matrix

| Integration | Official API | Public | Sandbox | SIH Access | Recommended Mode |
|------------|-------------|--------|---------|------------|-----------------|
| GeM | ❌ | — | — | ❌ | MOCK |
| API Setu | ✅ | Registration | ✅ | ⚠️ | MOCK/SANDBOX |
| DigiLocker | ✅ | Partner | ✅ | ⚠️ | MOCK |
| GSTN | ✅ | Via GSP | ✅ | ⚠️ | MOCK/SANDBOX |
| MCA | ❌ | — | — | ❌ | MOCK |
| Udyam | ❌ | — | — | ❌ | MOCK |
| PAN (Protean) | ✅ | Restricted | ✅ | ❌ | MOCK |
| EPFO | ❌ | — | — | ❌ | MANUAL |
| ESIC | ❌ | — | — | ❌ | MANUAL |
| Startup India | ❌ | — | — | ❌ | MANUAL |
| NSIC | ❌ | — | — | ❌ | MANUAL |
| CPPP | ❌ | — | — | ❌ | MANUAL |
| DPIIT/MII | ❌ (policy) | — | — | N/A | RULE ENGINE |
| BIS | ❌ | — | — | ❌ | MANUAL |
| CPCL Portal | ❌ | — | — | ❌ | MANUAL |

**Critical Finding:** The majority of government verification sources do NOT have publicly confirmed APIs for our workflow. Our architecture MUST support graceful fallback to MANUAL and MOCK modes. This is not a limitation — it is a realistic design that accounts for India's current government digital infrastructure.

