# Phase 1 — Government Manual Fallback Workflow Architecture

## Executive Principles

> [!IMPORTANT]
> **MANUAL FALLBACK IS A FIRST-CLASS SAFETY NET:**
> Automated government APIs may experience network outages, rate limits, schema revisions, or lack public availability altogether.
> Manual verification by an authorized Procurement Officer is a **first-class, fully supported architectural pathway** in the platform—not a system failure state.
> Manual fallback produces standard, auditable `EvidenceRecord` objects stamped with `operating_mode = MANUAL_FALLBACK`.

---

## 1. Manual Fallback Architecture & Trigger Conditions

```
                               ┌────────────────────────────────────────┐
                               │     VERIFICATION REQUEST INITIATED     │
                               └────────────────────────────────────────┘
                                                   │
                ┌──────────────────────────────────┴──────────────────────────────────┐
                ▼                                                                     ▼
┌────────────────────────────────────────┐                         ┌────────────────────────────────────────┐
│     AUTOMATED INTEGRATION PATHWAY      │                         │     MANUAL FALLBACK TRIGGER CONDITIONS │
├────────────────────────────────────────┤                         ├────────────────────────────────────────┤
│ Adapters attempt automated API lookup  │                         │ • Upstream Gateway Timeout / 5xx       │
│ (LIVE / SANDBOX / MOCK modes)          │                         │ • Circuit Breaker Opened               │
└────────────────────────────────────────┘                         │ • HTTP 429 Rate Limit Exhausted        │
                │                                                  │ • Missing API Authorization Credentials│
                │ (Fails / Unavailable)                            │ • Source Classification = MANUAL_ONLY  │
                └─────────────────────────────────────────────────►│ • Material Identity Ambiguity          │
                                                                   └────────────────────────────────────────┘
                                                                                      │
                                                                                      ▼
                                                                   ┌────────────────────────────────────────┐
                                                                   │ PROC. OFFICER WORKBENCH TASK CREATED   │
                                                                   └────────────────────────────────────────┘
```

---

## 2. End-to-End Manual Fallback Workflow

When manual verification is triggered, the system executes an auditable multi-step workflow:

```mermaid
sequenceDiagram
    autonumber
    participant Orch as Verification Orchestrator
    participant Task as Task Queue Service
    participant UI as Procurement Officer Workbench
    participant Off as Procurement Officer
    participant Engine as Compliance Rule Engine
    participant Audit as Audit Hash-Chain Engine

    Orch->>Task: Create Manual Verification Task (request_id, bidder_id, req_id)
    Task->>UI: Notify Procurement Officer (Priority Alert)
    UI->>Off: Display Task Details, Identifier & Portal Direct Links

    Off->>Off: Inspect Official Govt Portal (e.g., CPPP / GST / Udyam Portal)
    Off->>UI: Enter Verification Reference No, Date, Status & Upload Evidence Artifact
    UI->>UI: Validate Mandatory Fields & File Integrity Hash

    opt Dual-Verification Required (Policy-Configured High Risk)
        UI->>Off: Request Second Officer Approval (Four-Eyes Principle)
    end

    UI->>Orch: Submit Manual Verification Envelope
    Orch->>Orch: Generate EvidenceRecord (Mode: MANUAL_FALLBACK)
    Orch->>Audit: Write MANUAL_VERIFICATION_COMPLETED Audit Block
    Orch->>Engine: Send EvidenceRecord for Rule Evaluation
    Engine-->>UI: Update Rule Evaluation Status to VERIFIED / NON_COMPLIANT
```

---

## 3. Data Entry & Upload Controls

When completing a manual verification, Procurement Officers must capture sufficient traceable source evidence according to applicable procedures via the Workbench UI:

### 3.1 Mandatory Form Fields
1. **Target Source System:** Dropdown of official registered sources (`SRC_GSTN`, `SRC_UDYAM`, `SRC_DEBARMENT`, etc.).
2. **Official Portal URL:** Exact web portal URL inspected (e.g., `https://services.gst.gov.in/services/searchtp`).
3. **Official Source / Reference Identifier:** Official Transaction Reference, Certificate Number, Document Number, Notice Number, or Search Reference string.
4. **Verification Timestamp:** Date and time of manual inspection.
5. **Business Verification Status:** Officer ruling (`VERIFIED`, `NOT_VERIFIED`, `EXPIRED`, `MISMATCH`).
6. **Officer Verification Notes:** Detailed rationale justifying the manual determination.
7. **Traceable Source Evidence Artifact:** Approved evidence artifact according to applicable procedure (e.g., official downloadable PDF, portal verification receipt, digitally signed document, certificate, or portal screenshot).

### 3.2 File Attachment Security & Integrity
* **Allowed Formats:** Cryptographically inspected PDF, PNG, or JPEG files.
* **Integrity Hashing:** Cryptographic hashing (SHA-256) is applied to all captured evidence files to ensure tamper-evident integrity.
* **Virus Scanning:** All uploads pass through ClamAV / security scanning before storage in MinIO object storage.

---

## 4. Policy-Configurable Dual-Verification Controls (Four-Eyes Principle)

High-risk manual verification categories may require dual-officer review according to **configurable procurement policy and organizational authorization**:

```
┌────────────────────────────────────────────────────────┐
│ POLICY-CONFIGURABLE DUAL-APPROVAL CATEGORIES (EXAMPLES)│
├────────────────────────────────────────────────────────┤
│ • Debarment / Restricted-Vendor List Checks            │
│ • Statutory Exemption Manual Rulings                   │
│ • Financial Eligibility Overrides                      │
│ • Single-Source OEM Authorization Validations         │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ DUAL-APPROVAL WORKFLOW:                                │
├────────────────────────────────────────────────────────┤
│ • Primary Officer enters verification details & proof  │
│ • Task transitions to `PENDING_SECOND_OFFICER_REVIEW` │
│ • Secondary Officer reviews portal proof & co-signs    │
│ • Task completes and generates EvidenceRecord          │
└────────────────────────────────────────────────────────┘
```

---

## 5. Evidence Generation & Audit Traceability

Manual verifications generate standard `EvidenceRecord` objects linked to `OfficerDecision` records:

```json
{
  "evidence_id": "01J7MANUAL0000000000000001",
  "bidder_id": "01J7A8B9C0D1E2F3G4H5J6K7B1",
  "source_id": "SRC_DEBARMENT",
  "operating_mode": "MANUAL_FALLBACK",
  "retrieved_at": "2026-09-05T15:10:00Z",
  "freshness_status": "CURRENT",
  "provenance": {
    "verified_by_officer_id": "USR_OFFICER_442",
    "second_approver_officer_id": "USR_OFFICER_109",
    "inspected_portal_url": "https://eprocure.gov.in/eprocure/app?page=FrontEndDebrmentList",
    "portal_reference_number": "CPPP-DEB-REF-2026-0099",
    "attachment_file_sha256": "7c9e...11a4",
    "officer_notes": "Searched CPPP debarment database manually. Bidder entity ABC Heavy Industries Pvt Ltd is NOT listed."
  },
  "evidence_payload_hash": "3a1b...88c2",
  "requires_human_review": false
}
```
