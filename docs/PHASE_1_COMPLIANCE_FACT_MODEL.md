# Phase 1 — Compliance Fact Model Specification

## Overview

The **Compliance Fact Model Specification** defines the normalized data structures, provenance envelopes, and status classifications for input facts consumed by the deterministic rule engine in the **SIH26100 Bid Compliance Verification Platform**.

Every compliance determination is evaluated against an immutable, type-safe dictionary of `NormalizedFact` objects.

---

## 1. Fact Provenance Architecture & 10 Fact Sources

A `NormalizedFact` is never an un-sourced raw value. It encapsulates the origin, extraction method, timestamp, and underlying `EvidenceRecord` reference across 10 distinct fact sources:

```
┌────────────────────────────────────────────────────────┐
│ FACT SOURCES                                           │
├────────────────────────────────────────────────────────┤
│ 1. Bidder-Submitted Document                           │
│ 2. AI-Extracted Document Field (ExtractedField)        │
│ 3. Government Verification Result                      │
│ 4. Immutable EvidenceRecord                            │
│ 5. Tender Metadata                                     │
│ 6. TenderVersion Attributes                            │
│ 7. PolicyVersion Parameters                            │
│ 8. BidSubmission Telemetry                             │
│ 9. Manually Verified Officer Fact                      │
│ 10. Derived Deterministic Fact (Calculated)            │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ NORMALIZED FACT FACTORY                                │
├────────────────────────────────────────────────────────┤
│ • Validates DataType & Type Conversions                │
│ • Binds SHA-256 Evidence Hashes                        │
│ • Assigns Fact Status & Provenance Envelope            │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ NormalizedFact Object                                  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Fact Status Taxonomy (9 Controlled States)

Facts are assigned an explicit status prior to rule evaluation:

| Status Code | Description / Condition | Engine Evaluation Handling |
| :--- | :--- | :--- |
| **`AVAILABLE`** | Fact present and extracted; awaiting verification. | Processed by rule engine. |
| **`VERIFIED`** | Fact verified against government source or officer workflow. | High-confidence input; eligible for `PASS`/`FAIL`. |
| **`UNVERIFIED`** | Fact present in bidder document, but unconfirmed by external source. | Yields `NOT_VERIFIED` intermediate result. |
| **`MISSING`** | Fact absent from bidder submission and document extractions. | Yields `MISSING_EVIDENCE` intermediate result. |
| **`STALE`** | Fact timestamp exceeds applicable policy freshness window. | Yields `STALE` intermediate result; triggers refresh. |
| **`CONFLICTING`** | Multi-source discrepancy detected for this fact value. | Yields `CONFLICTING` intermediate result. |
| **`INVALID`** | Fact value fails type parsing or checksum validation. | Yields `INVALID_FACT` intermediate result. |
| **`UNKNOWN`** | Fact state cannot be determined due to missing metadata. | Yields `REQUIRES_HUMAN_REVIEW`. |
| **`NOT_APPLICABLE`** | Fact not required for this bidder classification. | Filtered by applicability engine. |

> [!CRITICAL]
> **MISSING IS NOT FAIL:**
> A fact with status `MISSING`, `UNVERIFIED`, `STALE`, or `CONFLICTING` does **NOT** equal a compliance `FAIL`. Only a verified fact evaluating a rule condition to `False` produces `FAIL`. Non-verified facts yield intermediate states requiring officer review.

---

## 3. `NormalizedFact` Schema Specification

Each fact object conforms to the following schema:

```json
{
  "fact_key": "bidder_annual_turnover_inr",
  "value": 150000000.00,
  "data_type": "CURRENCY",
  "currency_code": "INR",
  "unit": "INR",
  "status": "VERIFIED",
  "source_type": "EVIDENCE_RECORD",
  "evidence_reference_id": "01J7A8EVIDENCE0000000000001",
  "evidence_hash": "a4f8b91c...8821a90e",
  "extracted_at": "2026-09-05T14:20:00Z",
  "verified_at": "2026-09-05T14:30:02Z",
  "valid_from": "2026-04-01T00:00:00Z",
  "valid_until": "2027-03-31T23:59:59Z",
  "provenance": {
    "document_id": "01J7DOC0000000000000000001",
    "page_number": 4,
    "bounding_box": [120, 340, 480, 380],
    "extraction_confidence": 0.99,
    "extractor_model": "SP-FIN-EXTRACTION-v1.0"
  }
}
```

---

## 4. Derived & Calculated Fact Engine

Complex rules often evaluate derived metrics (e.g., 3-year average turnover, debt-to-equity ratio). Derived facts are constructed deterministically prior to rule evaluation:

$$\text{AverageTurnover} = \frac{\text{Turnover}_{Y1} + \text{Turnover}_{Y2} + \text{Turnover}_{Y3}}{3}$$

Every derived fact retains explicit references to its primitive component facts in its `provenance` metadata.
