# Phase 1 — Government Evidence & Provenance Architecture

## Overview

The **Evidence and Provenance Architecture** defines how the **SIH26100 Bid Compliance Verification Platform** transforms raw government adapter responses into immutable, tamper-evident `EvidenceRecord` domain objects.

It covers canonical field normalization, multi-tier identity comparison, source freshness evaluation, multi-source conflict resolution, and cryptographic provenance chain embedding.

---

## 1. Evidence-First Verification Principle

Every government verification outcome that influences bid qualification must yield a structured `EvidenceRecord`.

```
+-----------------------------------+
|  GovernmentVerificationResult     |
+-----------------------------------+
                  │
                  ▼
+-----------------------------------+
|      EVIDENCE GENERATOR           |
|  * Extract Normalized Fields      |
|  * Compute Field Match Matrix     |
|  * Evaluate Source Freshness      |
|  * Generate Response/Evidence Hash|
+-----------------------------------+
                  │
                  ▼
+-----------------------------------+
|         EvidenceRecord            |  (Immutable Storage)
|  * evidence_id: ULID              |
|  * bidder_id: ULID                |
|  * source_id: SRC_GSTN            |
|  * operating_mode: LIVE           |
|  * evidence_payload (JSONB)       |
|  * evidence_hash (SHA-256)        |
+-----------------------------------+
                  │
                  ▼
+-----------------------------------+
|  DETERMINISTIC COMPLIANCE ENGINE  |
+-----------------------------------+
```

---

## 2. Canonical Normalized Result Model

Regardless of origin (API Setu, official portal, mock adapter, manual fallback), all adapter responses are transformed into a canonical JSON model inside `GovernmentVerificationResult`:

```json
{
  "verification_result_id": "01J7A8B9C0D1E2F3G4H5J6K7L8",
  "verification_request_id": "01J7A8B9C0D1E2F3G4H5J6K7L0",
  "bidder_id": "01J7A8B9C0D1E2F3G4H5J6K7B1",
  "source_system": "SRC_GSTN",
  "source_type": "AUTHORIZED_API_AGGREGATOR",
  "adapter_id": "gst_verification_adapter",
  "adapter_version": "1.2.0",
  "operating_mode": "LIVE",
  "verification_type": "GSTIN_STATUS",
  "queried_identifier_type": "GSTIN",
  "queried_identifier_value_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "technical_status": "SUCCESS",
  "business_status": "VERIFIED",
  "verified_fields": {
    "legal_name": {
      "bidder_value": "ABC Heavy Industries Pvt Ltd",
      "source_value": "ABC HEAVY INDUSTRIES PRIVATE LIMITED",
      "match_status": "NORMALIZED_MATCH",
      "match_score": 0.98
    },
    "gstin_status": {
      "bidder_value": "ACTIVE",
      "source_value": "Active",
      "match_status": "EXACT_MATCH",
      "match_score": 1.0
    },
    "taxpayer_type": {
      "bidder_value": "REGULAR",
      "source_value": "Regular",
      "match_status": "EXACT_MATCH",
      "match_score": 1.0
    }
  },
  "source_timestamp": "2026-09-05T14:30:00Z",
  "retrieved_at": "2026-09-05T14:30:02Z",
  "valid_from": "2026-09-05T00:00:00Z",
  "valid_until": "2026-10-05T23:59:59Z",
  "freshness_status": "CURRENT",
  "source_reference": "REF-GST-2026-998811",
  "response_hash": "a4f8...91b2",
  "requires_human_review": false
}
```

---

## 3. Multi-Tier Field Matching & Identity Comparison Logic

Identity verification must determine whether bidder-submitted credentials represent the exact entity registered in government databases.

### 3.1 Field Match Taxonomy

| Match Status Code | Definition & Criteria | Match Score / Signal | Compliance Action |
| :--- | :--- | :--- | :--- |
| **`EXACT_MATCH`** | Character-for-character exact string match (case-insensitive, trimmed). | Exact (1.00) | Automatically accepted by rule engine. |
| **`NORMALIZED_MATCH`** | Match after legal entity suffix expansion (e.g., `"Pvt Ltd"` $\rightarrow$ `"Private Limited"`), punctuation removal, and whitespace folding. | High Similarity | Automatically accepted by rule engine. |
| **`ALIAS_MATCH`** | Match based on confirmed trade name or registered parent entity alias. | Alias Alignment | Accepted; logged with informational note. |
| **`MISMATCH`** | Material divergence in identifier digits, corporate name, or operational status. | Divergent | Triggers `requires_human_review=True`; escalated to Procurement Officer. |
| **`UNAVAILABLE`** | Field not present in government source payload. | N/A | Evaluated based on rule mandatoriness. |
| **`UNABLE_TO_VERIFY`** | Source service unavailable or record missing. | N/A | Evaluated as `NOT_VERIFIED`; manual fallback triggered. |

> [!IMPORTANT]
> **POLICY-CONTROLLED IDENTITY MATCHING:**
> Identity matching acceptance criteria are source-, identifier-, requirement-, and policy-specific and must be empirically validated and approved before operational use.
> Similarity scores are supporting signals only and do not independently establish legal identity.
> Where material identity ambiguity exists, the flow transitions: $\text{AMBIGUOUS_IDENTITY} \longrightarrow \text{HUMAN REVIEW}$.

---

## 4. Source Freshness & Validity Architecture

Verification data ages over time. The platform evaluates freshness dynamically across policy-controlled layers according to approved procurement rules:

```
┌────────────────────────────────────────────────────────┐
│ 1. APPLICABLE PROCUREMENT POLICY / TENDER REQUIREMENT  │
│    (Tender Document Clause e.g., "GST checked within 7D")│
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. SOURCE-DEFINED VALIDITY                            │
│    (Official Expiry / Valid-Until Date in Source Payload) │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 3. APPROVED CONFIGURABLE FALLBACK POLICY               │
│    (Registry Fallback Policy Window per Source Class)  │
└────────────────────────────────────────────────────────┘
```

> [!NOTE]
> **POLICY-CONTROLLED FRESHNESS:** Fallback freshness policies are explicitly configurable, policy-controlled, requirement-aware, and source-aware. If no approved freshness rule exists for a source, evidence freshness defaults to `UNKNOWN` and requires human review.

### 4.1 Freshness State Evaluation Matrix

$$\text{Age} = \text{Current UTC Time} - \text{RetrievedAt Timestamp}$$

```
                ┌────────────────────────────────────────┐
                │        EVALUATE EVIDENCE AGE           │
                └────────────────────────────────────────┘
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           ▼                         ▼                         ▼
┌────────────────────┐    ┌────────────────────┐    ┌────────────────────┐
│ Age ≤ Policy Window│    │ Age > Policy Window│    │ Expiry Date Past   │
├────────────────────┤    ├────────────────────┤    ├────────────────────┤
│ Status: CURRENT    │    │ Status: STALE      │    │ Status: EXPIRED    │
│ Action: Valid      │    │ Action: Auto-Refresh│    │ Action: Fail/Review│
└────────────────────┘    └────────────────────┘    └────────────────────┘
```

---

## 5. Multi-Source Conflict Resolution Model

When multiple government sources or bidder documents return contradictory information (e.g., GSTN reports active status while CPPP Debarment list reports blacklisting), the platform applies strict conflict resolution protocols:

```
[Source A: GST Active]  <--->  [Source B: Debarment Portal Blacklisted]
                                   │
                                   ▼
          ┌─────────────────────────────────────────────────┐
          │   MULTI-SOURCE CONFLICT DETECTION ENGINE       │
          └─────────────────────────────────────────────────┘
                                   │
       ┌───────────────────────────┴───────────────────────────┐
       ▼                                                       ▼
┌────────────────────────────────────────┐         ┌────────────────────────────────────────┐
│ 1. ABSOLUTE CONFLICT PRESERVATION      │         │ 2. NON-OVERWRITE GUARANTEE            │
│ Both Source A and Source B evidence    │         │ Historical records retain individual   │
│ records are retained in database.      │         │ raw response hashes and timestamps.    │
└────────────────────────────────────────┘         └────────────────────────────────────────┘
       │                                                       │
       └───────────────────────────┬───────────────────────────┘
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 3. CONFLICT MATERIALITY & ESCALATION EVALUATION                                  │
├──────────────────────────────────────────────────────────────────────────────────┤
│ • Material Conflict (Status/Debarment): Flag `requires_human_review=True`         │
│ • Non-Material Conflict (Minor Address formatting): Use highest authority source │
└──────────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 4. HUMAN PROCUREMENT OFFICER DECISION GATEWAY                                    │
│ Procurement Officer evaluates both evidence records and enters formal ruling.   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Immutable Evidence Storage & Provenance Envelope

Each generated `EvidenceRecord` wraps the verification payload inside an immutable provenance envelope:

```json
{
  "evidence_id": "01J7A8EVIDENCE0000000000001",
  "bidder_id": "01J7A8B9C0D1E2F3G4H5J6K7B1",
  "tender_id": "01J7A8B9C0D1E2F3G4H5J6K7T1",
  "requirement_id": "01J7A8B9C0D1E2F3G4H5J6K7R1",
  "verification_result_id": "01J7A8B9C0D1E2F3G4H5J6K7L8",
  "source_id": "SRC_GSTN",
  "operating_mode": "LIVE",
  "retrieved_at": "2026-09-05T14:30:02Z",
  "freshness_status": "CURRENT",
  "provenance": {
    "adapter_id": "gst_verification_adapter",
    "adapter_version": "1.2.0",
    "source_url_sanitized": "https://apisetu.gov.in/v1/gstn/search",
    "raw_response_sha256": "a4f8...91b2",
    "correlation_id": "c7a8-9988-4411-bba0",
    "execution_latency_ms": 420
  },
  "evidence_payload_hash": "9f8e...71c4",
  "created_at": "2026-09-05T14:30:03Z"
}
```
