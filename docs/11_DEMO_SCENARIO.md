# 11 — Demo Scenario

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05

---

## Demo Overview

**Duration:** 8–10 minutes  
**Audience:** SIH judges (technical evaluators, domain experts, ministry representatives)  
**Goal:** Demonstrate end-to-end AI-powered bid compliance verification with realistic scenarios

---

## Demo Structure (Timeline)

| Time | Step | Feature Demonstrated | Duration |
|------|------|---------------------|----------|
| 0:00 | Opening | Problem statement; solution overview | 1 min |
| 1:00 | Step 1 | Tender import & AI requirement extraction | 1.5 min |
| 2:30 | Step 2 | Officer confirms requirements | 0.5 min |
| 3:00 | Step 3 | Add bidders & upload documents | 1 min |
| 4:00 | Step 4 | AI document classification & extraction | 1 min |
| 5:00 | Step 5 | Government verification + cross-source checking | 1.5 min |
| 6:30 | Step 6 | Compliance evaluation & risk scoring | 1 min |
| 7:30 | Step 7 | AI explanation & recommendations | 0.5 min |
| 8:00 | Step 8 | Officer decision & audit trail | 1 min |
| 9:00 | Closing | Summary, innovation highlights, Q&A setup | 1 min |

---

## Synthetic Tender Document

### "CPCL/PROC/2026-27/INSTRUMENTATION/001"

**Title:** Supply, Installation, and Commissioning of Process Control Instrumentation for CPCL Manali Refinery

**Estimated Value:** ₹8.5 Crore

**Requirements (10 items):**

| # | Requirement | Category | Mandatory | Threshold |
|---|------------|----------|-----------|-----------|
| R1 | Valid PAN Card | STATUTORY | Yes | Must be active |
| R2 | Active GST Registration | STATUTORY | Yes | Status must be ACTIVE |
| R3 | Company Registration (CIN) | LEGAL | Yes | Company must be ACTIVE; not struck off |
| R4 | Minimum Annual Turnover ≥ ₹5 Crore (any of last 3 FY) | FINANCIAL | Yes | ₹5,00,00,000 |
| R5 | Minimum 3 years experience in process instrumentation | EXPERIENCE | Yes | 3 years |
| R6 | OEM Authorization for offered equipment | TECHNICAL | Yes | Valid authorization letter |
| R7 | Not blacklisted/debarred by any Govt/PSU | ELIGIBILITY | Yes | Not on any debarment list |
| R8 | Udyam/MSME Registration (if claiming MSME benefits) | STATUTORY | Conditional | Valid if claimed |
| R9 | Make in India — Local Content Declaration | LOCAL_CONTENT | Yes | Class-I or Class-II |
| R10 | Signed Integrity Pact | DECLARATION | Yes | Signed document |

---

## Four Bidder Scenarios

### Bidder A: "Precision Instruments India Pvt. Ltd." — CLEAN PASS ✅

**Scenario:** A well-documented, compliant bidder. All documents valid, all verifications pass, no conflicts.

| Requirement | Status | Evidence |
|------------|--------|---------|
| R1: PAN | ✅ PASS | PAN: AADCP1234A — VERIFIED Active |
| R2: GST | ✅ PASS | GSTIN: 33AADCP1234A1ZK — VERIFIED Active, returns filed |
| R3: CIN | ✅ PASS | CIN: U33120TN2015PTC098765 — VERIFIED Active |
| R4: Turnover | ✅ PASS | ₹12.3 Cr (FY 2024-25) — extracted from balance sheet |
| R5: Experience | ✅ PASS | 8 years — verified from work orders (2017-2025) |
| R6: OEM Auth | ✅ PASS | Valid authorization letter from Yokogawa India |
| R7: Debarment | ✅ PASS | Not found on any debarment list |
| R8: MSME | ✅ PASS | UDYAM-TN-02-0012345 — Small Enterprise, VERIFIED |
| R9: Make in India | ✅ PASS | Class-I Local Supplier (65% local content declared) |
| R10: Integrity Pact | ✅ PASS | Signed document uploaded |

**Cross-Source Check:** All names match: "PRECISION INSTRUMENTS INDIA PVT. LTD." across PAN, GST, MCA  
**Compliance Score:** 100 | **Evidence Confidence:** 92 | **Risk Score:** 5  
**Risk Classification:** 🟢 LOW  
**AI Recommendation:** "All mandatory requirements met with high-confidence evidence. No conflicts detected."

---

### Bidder B: "TechFlow Solutions LLP" — MISSING DOCUMENTS 🟡

**Scenario:** A bidder with missing documents. Some requirements cannot be evaluated. Requires procurement officer to request clarification.

| Requirement | Status | Evidence |
|------------|--------|---------|
| R1: PAN | ✅ PASS | PAN: AAQFT5678B — VERIFIED Active |
| R2: GST | ✅ PASS | GSTIN: 33AAQFT5678B1Z5 — VERIFIED Active |
| R3: CIN | ✅ PASS | LLPIN: AAP-4567 — VERIFIED Active |
| R4: Turnover | 🟠 MISSING | **No financial statements uploaded** |
| R5: Experience | 🟡 REVIEW | 2 work orders uploaded but unclear scope — AI confidence LOW (0.45) |
| R6: OEM Auth | 🟠 MISSING | **No OEM authorization letter uploaded** |
| R7: Debarment | ✅ PASS | Not found on any debarment list |
| R8: MSME | ⬜ N/A | Not claiming MSME benefits |
| R9: Make in India | 🟡 REVIEW | Declaration uploaded but local content % not clearly stated |
| R10: Integrity Pact | ✅ PASS | Signed document uploaded |

**Cross-Source Check:** Names match across PAN, GST, MCA  
**Compliance Score:** 50 | **Evidence Confidence:** 45 | **Risk Score:** 55  
**Risk Classification:** 🟡 MEDIUM  
**AI Recommendation:** "2 mandatory documents are missing (financial statements, OEM authorization). Experience evidence requires manual review — work order scope is unclear. Recommend requesting clarification from bidder before final evaluation."

---

### Bidder C: "Industrial Controls & Systems Pvt. Ltd." — CONFLICT/INCONSISTENCY 🟣

**Scenario:** A bidder whose data reveals cross-source conflicts. Different names on different registrations. GST shows irregular filing. Entity resolution raises questions.

| Requirement | Status | Evidence |
|------------|--------|---------|
| R1: PAN | ✅ PASS | PAN: AABCI9876C — VERIFIED Active, Name: "INDUSTRIAL CONTROLS AND SYSTEMS PVT LTD" |
| R2: GST | ⚠️ REVIEW | GSTIN: 33AABCI9876C1ZQ — Status: ACTIVE but **irregular filing** (3 returns not filed) |
| R3: CIN | 🟣 CONFLICT | CIN: U31200TN2012PTC087654 — Name on MCA: "**ICS TECHNOLOGIES PVT LTD**" — **NAME MISMATCH** |
| R4: Turnover | ✅ PASS | ₹7.8 Cr (FY 2024-25) — extracted from balance sheet |
| R5: Experience | ✅ PASS | 10 years — verified from multiple work orders |
| R6: OEM Auth | 🟡 REVIEW | Authorization letter uploaded but issued to "**ICS Technologies**" — **NAME MISMATCH with PAN** |
| R7: Debarment | ✅ PASS | Not found on any debarment list |
| R8: MSME | 🟣 CONFLICT | Udyam: UDYAM-TN-02-0098765 — Classification: **MEDIUM** but claims **SMALL** enterprise benefits |
| R9: Make in India | ✅ PASS | Class-II Local Supplier (35% local content) |
| R10: Integrity Pact | ✅ PASS | Signed document uploaded |

**Cross-Source Conflicts Detected:**
1. 🔴 CRITICAL: MCA name "ICS Technologies Pvt Ltd" ≠ PAN name "Industrial Controls and Systems Pvt Ltd" — **Possible name change not updated, or different entity**
2. 🟡 HIGH: OEM authorization issued to "ICS Technologies" — doesn't match current PAN name
3. 🟡 HIGH: GST returns irregular (3 unfiled returns)
4. 🟠 MEDIUM: Udyam shows MEDIUM classification but bidder claims SMALL enterprise benefits

**Compliance Score:** 70 | **Evidence Confidence:** 38 | **Risk Score:** 78  
**Risk Classification:** 🔴 CRITICAL  
**AI Recommendation:** "Multiple cross-source conflicts detected. The company name on MCA records ('ICS Technologies Pvt Ltd') does not match PAN records ('Industrial Controls and Systems Pvt Ltd'). This could indicate: (1) a legitimate name change not reflected in all registrations, or (2) an entity mismatch. Additionally, the bidder claims SMALL enterprise benefits but Udyam registration shows MEDIUM classification. Recommend investigation before proceeding."

---

### Bidder D: "GlobalTech Instruments India Pvt. Ltd." — NON-COMPLIANT / FAIL 🔴

**Scenario:** A bidder who fails multiple mandatory requirements. Clear disqualification case.

| Requirement | Status | Evidence |
|------------|--------|---------|
| R1: PAN | ✅ PASS | PAN: AADCG3456D — VERIFIED Active |
| R2: GST | 🔴 FAIL | GSTIN: 33AADCG3456D1Z8 — Status: **CANCELLED** (cancelled on 15/06/2025) |
| R3: CIN | ✅ PASS | CIN: U29190TN2019PTC123456 — VERIFIED Active |
| R4: Turnover | 🔴 FAIL | ₹2.1 Cr (FY 2024-25) — **below ₹5 Cr threshold** |
| R5: Experience | 🔴 FAIL | Company incorporated 2019 — **only 6 years; experience certificates show 2 years relevant work** |
| R6: OEM Auth | 🟤 EXPIRED | Authorization letter from Honeywell dated 2023, **expired March 2025** |
| R7: Debarment | 🔴 FAIL | **FOUND on CPPP debarment list** — debarred by BPCL on 10/01/2025 |
| R8: MSME | ⬜ N/A | Not claiming |
| R9: Make in India | 🔴 FAIL | **Non-Local Supplier** (12% local content) — below 20% minimum |
| R10: Integrity Pact | ✅ PASS | Signed document uploaded |

**Critical Failures:**
1. 🔴 GST registration CANCELLED — bidder cannot legally supply goods/services
2. 🔴 Turnover ₹2.1 Cr < ₹5 Cr minimum
3. 🔴 Only 2 years relevant experience < 3 years minimum
4. 🔴 Found on BPCL debarment list — blacklisted
5. 🔴 Non-local supplier (12% < 20% minimum)

**Compliance Score:** 30 | **Evidence Confidence:** 85 | **Risk Score:** 95  
**Risk Classification:** 🔴 CRITICAL  
**AI Recommendation:** "This bidder fails 5 mandatory requirements. Most critically: (1) GST registration is CANCELLED (cannot legally supply), and (2) bidder is DEBARRED by BPCL. These are absolute disqualifying conditions. Additionally, turnover, experience, and local content requirements are not met. OEM authorization has expired."

---

## Demo Flow Script

### Opening (0:00 – 1:00)
"We're presenting an AI-powered bid compliance verification platform designed for government procurement officers. Today's procurement evaluation at organizations like CPCL involves manually checking dozens of bidder documents against tender requirements — a process that takes days and is error-prone. Our platform automates this with AI-powered document intelligence, government verification, deterministic rule evaluation, and a complete audit trail. Critically, AI assists — but the procurement officer always makes the final decision."

### Step 1: Tender Import (1:00 – 2:30)
- Upload the synthetic CPCL tender document
- Show AI extracting 10 requirements in real-time
- Highlight: AI identifies requirement categories, thresholds, and source clauses
- Show confidence scores for each extraction

### Step 2: Officer Confirms (2:30 – 3:00)
- Officer reviews extracted requirements
- Modifies one requirement (e.g., corrects a threshold)
- Confirms the requirement checklist
- Point out: "AI proposed, human confirmed"

### Step 3: Add Bidders (3:00 – 4:00)
- Add 4 bidders with their identifiers
- Show real-time format validation (PAN, GSTIN patterns)
- Show PAN-GSTIN cross-validation (deterministic check)
- Upload document batches for each bidder

### Step 4: AI Document Processing (4:00 – 5:00)
- Show AI classifying documents (PAN card → PAN_CARD, balance sheet → FINANCIAL_STATEMENT)
- Show field extraction with confidence scores
- Highlight a low-confidence extraction flagged for review
- Show how officer can correct an AI extraction

### Step 5: Verification & Cross-Checking (5:00 – 6:30)
- Trigger government verification (all modes clearly labelled as MOCK)
- Show results flowing in: PAN ✅, GST ✅/❌, MCA ✅/🟣, Debarment ✅/🔴
- **KEY DEMO MOMENT:** Show Bidder C's cross-source conflict detection
  - "Notice how the system detected that the MCA name doesn't match the PAN name — this could indicate a legitimate name change or an entity mismatch"
- Show Bidder D's debarment hit: "This bidder was found on the BPCL debarment list"
- Show the 360 Identity Graph for a bidder

### Step 6: Compliance Evaluation (6:30 – 7:30)
- Show the compliance matrix for all 4 bidders
- Color-coded status for each requirement
- Three-dimensional scores visible
- Risk classification: 🟢 LOW, 🟡 MEDIUM, 🔴 CRITICAL, 🔴 CRITICAL
- Point out: "These are deterministic rule evaluations — every result is reproducible and traceable"

### Step 7: AI Explanation (7:30 – 8:00)
- Click on Bidder C's evaluation
- Show AI-generated explanation citing specific evidence
- Highlight evidence citations: "The system cites the exact page and field from each document"
- Show recommendations: "The AI suggests investigation, but does NOT recommend disqualification — that's the officer's decision"

### Step 8: Officer Decision & Audit (8:00 – 9:00)
- Officer qualifies Bidder A with rationale: "All requirements met, high confidence"
- Officer requests clarification for Bidder B: "Missing financial statements and OEM authorization"
- Officer flags Bidder C for investigation: "Name mismatch requires verification of corporate history"
- Officer disqualifies Bidder D: "Multiple mandatory failures including debarment"
- Generate audit report — show complete timeline, evidence chain, decision rationale
- Point out: "Every decision, every verification, every AI output is logged in an immutable audit trail"

### Closing (9:00 – 10:00)
"Our platform transforms bid compliance verification from a multi-day manual process into an AI-assisted, evidence-backed, auditable workflow. AI interprets documents and flags issues. Government sources verify identities. Deterministic rules evaluate compliance. Evidence proves every finding. And the procurement officer makes the final decision with full confidence and a complete audit trail."

---

## Demo Environment Requirements

| Component | Requirement |
|-----------|------------|
| **Frontend** | Web application running locally or on cloud |
| **Backend** | API server with all services running |
| **Database** | Pre-loaded with synthetic tender and bidder data |
| **AI Service** | Connected to Gemini/GPT API for real-time extraction and explanation |
| **Mock Services** | Pre-configured mock government verification responses |
| **Network** | Internet required for AI API calls only; all else local |
| **Backup** | Pre-computed results available if AI API is slow during demo |
| **Display** | 1080p minimum; ideally projector/large screen |

---

## Demo Preparation Checklist

- [ ] Synthetic tender document created (realistic CPCL format)
- [ ] 4 bidder data sets prepared
- [ ] Mock government responses configured for all scenarios
- [ ] Debarment mock list with Bidder D entry
- [ ] Pre-uploaded documents for all bidders
- [ ] AI prompts tested and refined for extraction quality
- [ ] Cross-source conflict data configured for Bidder C
- [ ] Audit report template designed
- [ ] Backup pre-computed results ready
- [ ] Demo rehearsed 3+ times
- [ ] Timing verified (under 10 minutes)
