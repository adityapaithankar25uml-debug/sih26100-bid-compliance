# 13 — Source Register

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05  
**Research Date:** 2026-09-05

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## Source Register

Every factual claim in the Phase 0 documentation is backed by the sources listed below. Sources are ordered by category and rated for authority.

### Authority Levels

| Level | Description |
|-------|------------|
| 🟢 A1 | Official Government of India website / portal |
| 🟢 A2 | Official ministry / department / agency website |
| 🟡 A3 | Government-authorized partner / intermediary |
| 🟡 A4 | Reputable industry / legal publication |
| 🟠 A5 | Secondary source (tech blog, comparison site) |

---

## 1. GeM (Government e-Marketplace)

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S01 | GeM, Government of India | GeM Portal | https://gem.gov.in | 🟢 A1 | GeM is the official government marketplace; no suitable public developer API confirmed | Yes |
| S02 | Research finding | GeM API availability | Web search, 2026-09-05 | 🟡 A4 | No suitable publicly documented/publicly accessible API confirmed for GeM | Yes |

---

## 2. API Setu

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S03 | MeitY, Government of India | API Setu Portal | https://apisetu.gov.in | 🟢 A1 | API Setu is the official Open API platform; hosts 4,200+ APIs | Yes |
| S04 | MeitY, Government of India | API Setu Documentation | https://docs.apisetu.gov.in | 🟢 A1 | Architecture, developer guides, onboarding flows | Yes |
| S05 | MeitY, Government of India | API Setu Partner Portal | https://partners.apisetu.gov.in | 🟢 A1 | Partner registration portal for DigiLocker and other APIs | Yes |
| S06 | Digital India | Digital India - API Setu | https://digitalindia.gov.in | 🟢 A1 | API Setu is part of Digital India initiative | Yes |

---

## 3. DigiLocker

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S07 | MeitY / DigiLocker | DigiLocker Portal | https://digilocker.gov.in | 🟢 A1 | Official DigiLocker portal | Yes |
| S08 | MeitY / DigiLocker | DigiLocker Partner Portal | https://partners.apisetu.gov.in | 🟢 A1 | Partner onboarding requires registration, verification call, agreement signing; OAuth 2.0 + OpenID Connect; sandbox available | Yes |

---

## 4. GSTN (GST Network)

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S09 | GSTN | GST Developer Portal | https://developer.gst.gov.in | 🟢 A1 | Official API documentation for GST system-to-system integration; RESTful, JSON-based | Yes |
| S10 | GSTN | GST Portal - Search Taxpayer | https://www.gst.gov.in | 🟢 A1 | Public GSTIN lookup available (with CAPTCHA); provides status, legal name, registration date | Yes |
| S11 | GSTN | GSTN Organization | https://gstn.org.in | 🟢 A1 | GST Suvidha Provider (GSP) program; ASP must partner with GSP for API access | Yes |

---

## 5. MCA (Ministry of Corporate Affairs)

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S12 | MCA, Government of India | MCA V3 Portal | https://www.mca.gov.in | 🟢 A1 | Official portal for corporate filings; Master Data section for company lookup; no suitable public REST API confirmed | Yes |
| S13 | Research finding | MCA API availability | Web search, 2026-09-05 | 🟡 A4 | No suitable public API confirmed for CIN/DIN verification; third-party providers offer APIs | Yes |

---

## 6. Udyam / MSME

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S14 | Ministry of MSME | Udyam Registration Portal | https://udyamregistration.gov.in | 🟢 A1 | Official registration portal; no suitable public API confirmed for verification | Yes |
| S15 | Ministry of MSME | MSME Portal | https://msme.gov.in | 🟢 A1 | Official MSME ministry website | Yes |

---

## 7. Income Tax / PAN

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S16 | Protean eGov Technologies (formerly NSDL) | Online PAN Verification (OPV) API | https://www.protean-india.com | 🟡 A3 | Official PAN verification API exists; requires entity registration + Class 2/3 DSC; production endpoint available | Yes |
| S17 | Research finding | PAN API access requirements | Web search, 2026-09-05 | 🟡 A4 | API is for eligible entities only; requests must be digitally signed | Yes |

---

## 8. EPFO

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S18 | EPFO | EPFO Official Website | https://www.epfindia.gov.in | 🟢 A1 | Official EPFO website; no suitable public API confirmed | Yes |
| S19 | EPFO | Unified Employer Portal | https://unifiedportal-emp.epfindia.gov.in | 🟢 A1 | Employer portal for compliance; TRRN search; e-Report Card; no suitable public API confirmed | Yes |

---

## 9. ESIC

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S20 | ESIC | ESIC Portal | https://www.esic.gov.in | 🟢 A1 | Official ESIC portal; no suitable public API confirmed | Yes |
| S21 | ESIC | Employer Search | https://portal.esic.gov.in/EmployerSearch/ | 🟢 A1 | Manual employer search by State/District/Code; web verification method | Yes |

---

## 10. Startup India / DPIIT

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S22 | DPIIT | Startup India Portal | https://www.startupindia.gov.in | 🟢 A2 | Official portal; Certificate Validation tool; Recognition Mapping Verification; no suitable public API confirmed | Yes |

---

## 11. NSIC

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S23 | NSIC | NSIC Official Website | https://www.nsic.co.in | 🟢 A2 | Official NSIC website; no suitable public API confirmed | Yes |
| S24 | NSIC | NSIC SPRS Online | https://www.nsicspronline.com | 🟢 A2 | Single Point Registration Scheme portal; manual verification only | Yes |

---

## 12. CPPP / eProcurement

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S25 | NIC / Government of India | Central Public Procurement Portal | https://eprocure.gov.in/cppp | 🟢 A1 | Official CPPP; no suitable public API confirmed; Debarment List searchable by Login ID or PAN | Yes |
| S26 | NIC | CPPP Debarment List | https://eprocure.gov.in | 🟢 A1 | Debarment list exists but is manually searchable only | Yes |

---

## 13. DPIIT / Make in India

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S27 | DPIIT | Public Procurement (Preference to Make in India) Order, 2017 (amended July 2024) | https://dpiit.gov.in | 🟢 A2 | Official order defining Class-I (≥50%), Class-II (≥20% to <50%), Non-Local (<20%); exclusions from local content; verification requirements; GTE threshold of ₹200 Cr | Yes |
| S28 | DPIIT | PPP-MII Notifications | https://dpiit.gov.in | 🟢 A2 | Amendment history and sector-specific notifications | Yes |

---

## 14. BIS

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S29 | BIS | BIS Manak Online | https://www.manakonline.in | 🟢 A2 | Licence verification via CM/L number, CRS R-number, HUID; no suitable public API confirmed | Yes |
| S30 | BIS | BIS Care App | App Stores | 🟢 A2 | Mobile app for product verification; no API for programmatic access confirmed | Yes |

---

## 15. CPCL

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S31 | CPCL | CPCL Official Website | https://www.cpcl.co.in | 🟢 A2 | Official CPCL website; subsidiary of IOCL; Ministry of Petroleum & Natural Gas | Yes |
| S32 | NIC / CPCL | CPCL e-Tendering Portal | https://cpcletenders.nic.in | 🟢 A1 | Official e-procurement portal; NIC-managed; DSC required; tender download free | Yes |

---

## 16. Competitor Sources

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S33 | NimbleS2P | NimbleS2P Platform | https://nimbles2p.com | 🟠 A5 | Compliance-first P2P platform with Indian statutory capability | Yes |
| S34 | Arched | Arched AI | https://arched.ai | 🟠 A5 | AI-powered tender matching for government contractors | Yes |
| S35 | Tenderkart | Tenderkart | https://tenderkart.in | 🟠 A5 | AI-powered tender analysis and discovery | Yes |
| S36 | QuickBid | QuickBid | https://quickbid.co.in | 🟠 A5 | AI platform for government contracting | Yes |
| S37 | Nexizo | Nexizo AI | https://nexizo.ai | 🟠 A5 | Deep tender document analysis | Yes |
| S38 | Elitemindz | ZYNO Procurement | https://elitemindz.co | 🟠 A5 | AI-powered P2P platform | Yes |

---

## 17. Regulatory / Legal Sources

| # | Source Organization | Source Title | URL | Authority | What It Proves | Current? |
|---|-------------------|-------------|-----|-----------|---------------|----------|
| S39 | Government of India | Digital Personal Data Protection Act, 2023 | gazette.gov.in | 🟢 A1 | Data protection law governing PII processing | Yes |
| S40 | Government of India | Information Technology Act, 2000 | meity.gov.in | 🟢 A1 | Cybersecurity and electronic transaction law | Yes |
| S41 | Ministry of Finance | General Financial Rules, 2017 | doe.gov.in | 🟢 A1 | Financial rules for government procurement | Yes |
| S42 | CVC | Central Vigilance Commission Guidelines | https://cvc.gov.in | 🟢 A1 | Integrity and transparency guidelines for procurement | Yes |

---

## Production Suitability Assessment

| Source | Production Integration | Reasoning |
|--------|----------------------|-----------|
| API Setu | ✅ Yes (with approval) | Official government platform; OAuth 2.0; sandbox available |
| DigiLocker | ✅ Yes (with partner onboarding) | Official; secure; consent-based |
| GST via GSP | ✅ Yes (with GSP partnership) | Official channel; well-documented |
| PAN via Protean | ✅ Yes (with registration + DSC) | Official channel; digitally signed |
| MCA via third-party | ⚠️ Conditional | Requires reputable third-party provider; compliance with DPDP Act |
| Udyam via third-party | ⚠️ Conditional | Same as MCA |
| EPFO | ❌ Manual fallback | No suitable public API confirmed |
| ESIC | ❌ Manual fallback | No suitable public API confirmed |
| Startup India | ❌ Manual fallback | No suitable public API confirmed |
| NSIC | ❌ Manual fallback | No suitable public API confirmed |
| CPPP | ❌ Manual fallback | No suitable public API confirmed |
| BIS | ❌ Manual fallback | No suitable public API confirmed |
| GeM | ❌ Manual fallback | No suitable public API confirmed |

