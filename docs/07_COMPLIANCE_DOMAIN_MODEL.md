# 07 — Compliance Domain Model

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05

---

## 1. Compliance Status Model

### 1.1 Status Definitions

| Status | Code | Meaning | Color | Action Required |
|--------|------|---------|-------|----------------|
| **PASS** | `PASS` | Requirement fully satisfied with verified evidence | 🟢 Green | None |
| **FAIL** | `FAIL` | Requirement not satisfied or evidence contradicts | 🔴 Red | Disqualification consideration or clarification |
| **REVIEW** | `REVIEW` | Evidence exists but requires human judgment | 🟡 Yellow | Procurement officer must review |
| **MISSING** | `MISSING` | Required evidence not submitted | 🟠 Orange | Request document from bidder |
| **EXPIRED** | `EXPIRED` | Evidence exists but validity period has lapsed | 🟤 Brown | Request updated document |
| **CONFLICT** | `CONFLICT` | Multiple sources provide contradictory information | 🟣 Purple | Investigation required |
| **NOT_VERIFIED** | `NOT_VERIFIED` | Evidence submitted but could not be verified against authoritative source | ⚪ Gray | Attempt re-verification or manual check |
| **NOT_APPLICABLE** | `N/A` | Requirement does not apply to this bidder/tender | ⬜ White | None |

### 1.2 Status Transitions

```
                    ┌──────────┐
                    │ MISSING  │
                    └────┬─────┘
                         │ document uploaded
                         ▼
                ┌────────────────┐
                │ NOT_VERIFIED   │
                └───────┬────────┘
                        │ verification attempted
            ┌───────────┼───────────┐
            ▼           ▼           ▼
     ┌──────────┐ ┌──────────┐ ┌──────────┐
     │   PASS   │ │  REVIEW  │ │   FAIL   │
     └──────────┘ └────┬─────┘ └──────────┘
                       │ officer reviews
               ┌───────┼───────┐
               ▼               ▼
        ┌──────────┐    ┌──────────┐
        │   PASS   │    │   FAIL   │
        └──────────┘    └──────────┘

Special transitions:
  Any status → EXPIRED  (when date validity check fails)
  Any status → CONFLICT (when cross-source inconsistency detected)
  Any status → NOT_APPLICABLE (when applicability rule excludes requirement)
```

---

## 2. Domain Entities

### 2.1 Tender

```
Tender {
  id: UUID
  title: String
  reference_number: String
  organization: String  // e.g., "CPCL"
  department: String
  category: Enum(GOODS, SERVICES, WORKS)
  estimated_value: Decimal
  currency: String  // "INR"
  publish_date: DateTime
  submission_deadline: DateTime
  opening_date: DateTime
  status: Enum(DRAFT, ACTIVE, EVALUATION, CLOSED, CANCELLED)
  documents: [TenderDocument]
  requirements: [Requirement]
  corrigenda: [Corrigendum]
  make_in_india_applicable: Boolean
  make_in_india_policy_version: String  // e.g., "2017-amended-2024-07-19"
  local_content_threshold: Decimal  // tender-specific override
  created_by: UserID
  created_at: DateTime
  updated_at: DateTime
}
```

### 2.2 Requirement

```
Requirement {
  id: UUID
  tender_id: UUID
  category: Enum(
    FINANCIAL,
    TECHNICAL,
    LEGAL,
    STATUTORY,
    EXPERIENCE,
    LOCAL_CONTENT,
    DECLARATION,
    DOCUMENT,
    OEM,
    ELIGIBILITY,
    OTHER
  )
  title: String  // e.g., "Minimum Annual Turnover"
  description: String
  mandatory: Boolean
  threshold_type: Enum(
    MINIMUM,
    MAXIMUM,
    EXACT,
    RANGE,
    BOOLEAN,
    DOCUMENT_REQUIRED,
    TEXT_MATCH,
    DATE_VALIDITY,
    CUSTOM
  )
  threshold_value: String  // "50000000" or "true" or "2023-04-01..2026-03-31"
  threshold_unit: String  // "INR", "years", "%", null
  evidence_type: Enum(
    DOCUMENT,
    GOVERNMENT_VERIFICATION,
    SELF_DECLARATION,
    CALCULATION,
    MULTIPLE
  )
  source_clause: String  // "Section 4.1.2, Page 12"
  source_page: Integer
  extraction_method: Enum(AI_EXTRACTED, MANUAL, TEMPLATE)
  extraction_confidence: Float  // 0.0 - 1.0
  confirmed_by: UserID  // null until officer confirms
  confirmed_at: DateTime
  rule_version: String  // for policy-based rules
  applicability_condition: String  // optional: when this requirement applies
  created_at: DateTime
  updated_at: DateTime
}
```

### 2.3 Bidder

```
Bidder {
  id: UUID
  tender_id: UUID
  legal_name: String
  trade_name: String
  pan: String  // validated format
  gstin: String  // validated format
  cin: String  // optional, validated format
  udyam_number: String  // optional, validated format
  dipp_number: String  // optional, Startup India
  entity_type: Enum(
    PROPRIETORSHIP,
    PARTNERSHIP,
    LLP,
    PRIVATE_LIMITED,
    PUBLIC_LIMITED,
    PSU,
    COOPERATIVE,
    TRUST,
    OTHER
  )
  msme_classification: Enum(MICRO, SMALL, MEDIUM, NOT_MSME, UNKNOWN)
  local_supplier_class: Enum(CLASS_I, CLASS_II, NON_LOCAL, UNKNOWN)
  contact_email: String
  contact_phone: String
  registered_address: String
  status: Enum(PENDING, UNDER_EVALUATION, QUALIFIED, DISQUALIFIED, CLARIFICATION_REQUESTED)
  documents: [BidderDocument]
  verifications: [Verification]
  evaluations: [ComplianceEvaluation]
  risk_profile: RiskProfile
  decision: Decision  // null until officer decides
  created_at: DateTime
  updated_at: DateTime
}
```

### 2.4 BidderDocument

```
BidderDocument {
  id: UUID
  bidder_id: UUID
  file_name: String
  file_type: String  // MIME type
  file_size: Integer
  file_hash: String  // SHA-256
  storage_path: String  // encrypted storage reference
  
  classification: Enum(
    PAN_CARD,
    GST_CERTIFICATE,
    UDYAM_CERTIFICATE,
    INCORPORATION_CERTIFICATE,
    FINANCIAL_STATEMENT,
    OEM_AUTHORIZATION,
    EXPERIENCE_CERTIFICATE,
    WORK_ORDER,
    COMPLETION_CERTIFICATE,
    LOCAL_CONTENT_DECLARATION,
    INTEGRITY_PACT,
    POWER_OF_ATTORNEY,
    EMD_PROOF,
    PF_REGISTRATION,
    ESIC_REGISTRATION,
    STARTUP_CERTIFICATE,
    NSIC_CERTIFICATE,
    BIS_LICENCE,
    ISO_CERTIFICATE,
    SELF_DECLARATION,
    OTHER
  )
  classification_method: Enum(AI_CLASSIFIED, MANUAL, BIDDER_LABELLED)
  classification_confidence: Float  // 0.0 - 1.0
  
  extracted_fields: [ExtractedField]
  validity_start: Date  // if applicable
  validity_end: Date  // if applicable
  is_expired: Boolean
  
  uploaded_at: DateTime
  uploaded_by: UserID
}
```

### 2.5 ExtractedField

```
ExtractedField {
  id: UUID
  document_id: UUID
  field_name: String  // e.g., "pan_number", "registration_date", "annual_turnover"
  field_value: String
  field_type: Enum(STRING, NUMBER, DATE, BOOLEAN, CURRENCY)
  confidence: Float  // 0.0 - 1.0
  source_page: Integer
  source_region: BoundingBox  // {x, y, width, height} on page
  extraction_method: Enum(AI_OCR, AI_NLP, MANUAL, COMPUTED)
  model_version: String
  needs_review: Boolean  // true if confidence < threshold
  reviewed_by: UserID
  reviewed_at: DateTime
  original_value: String  // preserved if human corrects
  created_at: DateTime
}
```

### 2.6 Verification

```
Verification {
  id: UUID
  bidder_id: UUID
  domain: Enum(
    PAN,
    GST,
    MCA,
    UDYAM,
    EPFO,
    ESIC,
    STARTUP_INDIA,
    NSIC,
    DIGILOCKER,
    DEBARMENT,
    BIS,
    OTHER
  )
  identifier: String  // The value being verified
  mode: Enum(LIVE, SANDBOX, MOCK, MANUAL)
  
  status: Enum(
    VERIFIED,
    NOT_VERIFIED,
    EXPIRED,
    ERROR,
    UNAVAILABLE,
    PENDING
  )
  
  request_timestamp: DateTime
  response_timestamp: DateTime
  response_data: JSON  // Structured response from source
  raw_response: String  // Raw API response (encrypted)
  error_message: String  // if status is ERROR
  
  source_system: String  // e.g., "developer.gst.gov.in", "mock-service"
  source_mode_label: String  // Clearly labels if mock
  cache_ttl: Integer  // seconds
  cache_expires_at: DateTime
  
  verified_by: UserID  // for MANUAL mode
  verification_notes: String  // for MANUAL mode
  
  created_at: DateTime
}
```

### 2.7 ComplianceEvaluation

```
ComplianceEvaluation {
  id: UUID
  bidder_id: UUID
  requirement_id: UUID
  
  status: Enum(PASS, FAIL, REVIEW, MISSING, EXPIRED, CONFLICT, NOT_VERIFIED, NOT_APPLICABLE)
  
  evidence: [EvidenceLink]  // links to documents, verifications, extracted fields
  
  rule_id: String  // reference to the rule that produced this result
  rule_version: String
  rule_input: JSON  // what data was fed to the rule
  rule_output: JSON  // what the rule produced
  
  severity: Enum(CRITICAL, HIGH, MEDIUM, LOW, INFO)
  
  ai_explanation: String  // AI-generated explanation
  ai_confidence: Float
  ai_model_version: String
  
  officer_override: Boolean
  officer_override_status: Enum(PASS, FAIL, REVIEW)  // if overridden
  officer_override_rationale: String
  officer_override_by: UserID
  officer_override_at: DateTime
  
  created_at: DateTime
  updated_at: DateTime
}
```

### 2.8 EvidenceLink

```
EvidenceLink {
  id: UUID
  evaluation_id: UUID
  evidence_type: Enum(DOCUMENT, VERIFICATION, EXTRACTED_FIELD, CROSS_REFERENCE, OFFICER_NOTE)
  evidence_id: UUID  // reference to the source evidence
  evidence_summary: String  // brief description
  relevance: String  // why this evidence is relevant
}
```

### 2.9 RiskProfile

```
RiskProfile {
  bidder_id: UUID
  
  compliance_score: Float  // 0-100: % of mandatory requirements met
  evidence_confidence: Float  // 0-100: quality of supporting evidence
  risk_score: Float  // 0-100: aggregate risk level (higher = more risky)
  
  risk_classification: Enum(LOW, MEDIUM, HIGH, CRITICAL)
  
  critical_failures: Integer  // count of FAIL on mandatory requirements
  conflicts_detected: Integer
  missing_documents: Integer
  expired_documents: Integer
  unverified_items: Integer
  
  score_breakdown: JSON  // detailed contribution of each factor
  
  calculated_at: DateTime
  calculation_version: String  // scoring algorithm version
}
```

### 2.10 Decision

```
Decision {
  id: UUID
  bidder_id: UUID
  tender_id: UUID
  
  decision: Enum(QUALIFY, DISQUALIFY, SEEK_CLARIFICATION)
  rationale: String  // mandatory free-text rationale by officer
  
  decided_by: UserID
  decided_at: DateTime
  
  approved_by: UserID  // if multi-level approval required
  approved_at: DateTime
  
  evidence_snapshot: UUID  // reference to frozen evidence state at decision time
  risk_profile_snapshot: JSON  // risk profile at decision time
  
  audit_trail: [AuditEntry]
}
```

---

## 3. Why Not a Single Percentage Score?

A single percentage score is **insufficient and potentially dangerous** for procurement compliance evaluation. Here's why:

### Problem with Single Score

| Scenario | Single Score | Reality |
|----------|-------------|---------|
| Bidder meets 9/10 requirements (90%) but fails mandatory PAN verification | 90% ✅ | Should be CRITICAL — PAN is mandatory |
| Bidder meets all requirements but evidence is all self-declared, nothing verified | 100% ✅ | Evidence confidence should be LOW |
| Bidder has minor document formatting issues on 3 requirements | 70% ❌ | These may be easily resolvable; risk is LOW |

### Recommended Three-Dimensional Model

#### Dimension 1: Compliance Score (0–100)
- **What it measures:** Percentage of requirements met (weighted by severity)
- **Calculation:** `(Σ passed_requirements × weight) / (Σ all_applicable_requirements × weight) × 100`
- **Note:** A single FAIL on a CRITICAL requirement forces classification to CRITICAL regardless of score

#### Dimension 2: Evidence Confidence (0–100)
- **What it measures:** How trustworthy and verifiable the supporting evidence is
- **Factors:**
  - Government-verified data: HIGH confidence
  - AI-extracted with high confidence: MEDIUM-HIGH
  - Self-declared documents: MEDIUM
  - Missing verification: LOW
- **Calculation:** Weighted average of per-evidence confidence scores

#### Dimension 3: Risk Score (0–100)
- **What it measures:** Aggregate risk from anomalies, conflicts, and concerns
- **Factors:**
  - Cross-source conflicts detected
  - Anomalous patterns (e.g., identical documents across bidders)
  - Missing critical verifications
  - Expired documents
  - Debarment/blacklisting matches
- **Calculation:** Risk factor accumulation with severity weighting

### Risk Classification Matrix

| Compliance Score | Evidence Confidence | Risk Score | Classification |
|-----------------|--------------------|-----------:|---------------|
| ≥ 90 | ≥ 80 | ≤ 20 | 🟢 LOW |
| ≥ 70 | ≥ 60 | ≤ 40 | 🟡 MEDIUM |
| ≥ 50 | ≥ 40 | ≤ 60 | 🟠 HIGH |
| < 50 | < 40 | > 60 | 🔴 CRITICAL |
| Any | Any | Any CRITICAL failure | 🔴 CRITICAL |

**Note:** Any single FAIL on a mandatory requirement automatically escalates to CRITICAL regardless of aggregate scores.

---

## 4. Make in India Compliance Model

### 4.1 Policy Reference
**Order:** Public Procurement (Preference to Make in India) Order, 2017  
**Latest Amendment:** July 19, 2024  
**Issuing Authority:** DPIIT (Department for Promotion of Industry and Internal Trade)

### 4.2 Classification Rules

```
LocalContentRules {
  policy_version: "PPP-MII-2017-R20240719"
  
  classifications: {
    CLASS_I: {
      label: "Class-I Local Supplier"
      min_local_content: 50  // percent
      description: "Goods/services with ≥50% local content"
    },
    CLASS_II: {
      label: "Class-II Local Supplier"
      min_local_content: 20  // percent
      max_local_content: 49.99
      description: "Goods/services with ≥20% and <50% local content"
    },
    NON_LOCAL: {
      label: "Non-Local Supplier"
      max_local_content: 19.99
      description: "Goods/services with <20% local content"
    }
  }
  
  exclusions_from_local_content: [
    "Imported items sourced locally from resellers/distributors",
    "License fees, royalties, or technical charges paid outside India",
    "Products that are merely repackaged, refurbished, or rebranded"
  ]
  
  verification_requirements: [
    "Cost break-up from bidder",
    "Cost of locally-sourced imported items (inclusive of taxes)",
    "Fees paid for technical expertise sourced from outside India",
    "OEM certificate for resellers regarding country of origin"
  ]
  
  weighted_average_rule: "For multi-item contracts, local content is calculated as weighted average of all items"
  
  gte_threshold: 20000000000  // Rs. 200 Crore — below this, no GTE without approval
  
  nodal_ministry_overrides: true  // Nodal ministries may set higher thresholds
}
```

### 4.3 Policy Versioning Requirement
- The system MUST store which policy version was applied for each evaluation
- When a new amendment is issued, rules MUST be updated but historical evaluations MUST retain the version they were evaluated under
- The system MUST support multiple active policy versions (different tenders may be under different versions based on their publication date)

---

## 5. Corrigendum Domain Model

```
Corrigendum {
  id: UUID
  tender_id: UUID
  corrigendum_number: Integer  // 1, 2, 3...
  title: String
  document: TenderDocument
  publish_date: DateTime
  
  changes: [CorrigendumChange]
  
  affected_requirements: [UUID]  // requirement IDs impacted
  affected_bidders: [UUID]  // bidder IDs whose evaluations need re-evaluation
  
  impact_analysis: String  // AI-generated impact summary
  impact_confirmed_by: UserID
  impact_confirmed_at: DateTime
  
  created_at: DateTime
}

CorrigendumChange {
  id: UUID
  corrigendum_id: UUID
  change_type: Enum(REQUIREMENT_ADDED, REQUIREMENT_MODIFIED, REQUIREMENT_REMOVED, DEADLINE_CHANGED, THRESHOLD_CHANGED, SCOPE_CHANGED, OTHER)
  original_text: String
  changed_text: String
  source_clause: String
  ai_detected: Boolean
  ai_confidence: Float
}
```
