# Phase 1 — Compliance Rule Model Specification

## Overview

The **Compliance Rule Model Specification** defines the structural data contracts, entity attributes, versioning semantics, and taxonomy models for rules and tender requirements within the **SIH26100 Bid Compliance Verification Platform**.

This model reuses domain entities established in Phase 1 Task 2 (`TenderRequirement`, `RequirementRuleMap`, `ComplianceRule`, `PolicyVersion`) without introducing duplicate or parallel entity definitions.

---

## 1. Domain Entity Architecture & Mapping

```
+------------------------------------+        1:N        +------------------------------------+
|         TenderRequirement          | ----------------> |        RequirementRuleMap          |
+------------------------------------+                   +------------------------------------+
                  │                                                         │
                  │ N:1                                                     │ N:1
                  v                                                         v
+------------------------------------+                   +------------------------------------+
|           TenderVersion            |                   |           ComplianceRule           |
+------------------------------------+                   +------------------------------------+
                                                                            │
                                                                            │ N:1
                                                                            v
                                                         +------------------------------------+
                                                         |           PolicyVersion            |
                                                         +------------------------------------+
```

---

## 2. Requirement Taxonomy (15 Controlled Categories)

Tender requirements are classified into 15 controlled functional categories:

| Category Key | Category Name | Description / Example Procurement Scope |
| :--- | :--- | :--- |
| **`ELIGIBILITY`** | Legal Eligibility | Incorporation status, legal entity type, non-conviction declarations. |
| **`STATUTORY`** | Statutory Compliance | Factory Act, Shops & Establishment Act, Labor Law compliance. |
| **`TAX`** | Tax Compliance | GSTIN active registration, PAN validity, Income Tax filing under Sec 206AB. |
| **`MSME`** | MSME / Udyam Benefits | Micro/Small enterprise classification, EMD/Tender fee exemption eligibility. |
| **`LOCAL_CONTENT`** | Make in India / Local Content| Class-I / Class-II local supplier qualification, local content percentage. |
| **`STARTUP`** | Startup India Benefits | DPIIT recognition, statutory relaxation in turnover/experience. |
| **`EXPERIENCE`** | Prior Work Experience | Similar contract completion certificates, monetary value thresholds. |
| **`FINANCIAL`** | Financial Standing | Average annual turnover, net worth, solvency certificate, liquidity ratio. |
| **`TECHNICAL`** | Technical Specifications | Equipment parameters, ISO certifications, quality assurance standards. |
| **`DOCUMENTARY`** | Document Submissions | Signed tender document presence, integrity of uploaded PDF schedules. |
| **`OEM_AUTHORIZATION`**| OEM Authorization | Manufacturer Authorization Form (MAF) letters, territory rights. |
| **`DEBARMENT`** | Blacklisting / Suspension | Multi-registry debarment checks (CPPP, GeM, CPCL holiday lists). |
| **`SOCIAL_SECURITY`** | Labor Social Security | EPFO ECR monthly filing regularity, ESIC employer contribution payments. |
| **`TENDER_SPECIFIC`** | Custom Tender Clauses | Project-specific clauses defined by CPCL procurement committee. |
| **`OTHER`** | Auxiliary Requirements | General administrative submissions, site visit acknowledgments. |

---

## 3. Rule Type Taxonomy (15 Controlled Types)

Compliance rules execute condition logic classified across 15 composable rule types:

| Rule Type Key | Type Description | Evaluation Inputs & Mechanics |
| :--- | :--- | :--- |
| **`BOOLEAN`** | Simple True/False Evaluation | Checks boolean facts (e.g., `declaration_signed == True`). |
| **`THRESHOLD`** | Minimum/Maximum Value | Numeric threshold check (e.g., `turnover >= required_turnover`). |
| **`RANGE`** | Bounded Numeric Interval | Range verification (e.g., `min_val <= parameter <= max_val`). |
| **`DATE`** | Chronological Comparison | Date ordering (e.g., `certificate_expiry_date > tender_closing_date`). |
| **`ENUMERATION`** | Allowed Category Matching | Enum check (e.g., `gst_status IN ['ACTIVE', 'REGULAR']`). |
| **`SET_MEMBERSHIP`** | Array Containment Check | Verifies if required item exists in a set of submitted items. |
| **`DOCUMENT_PRESENCE`**| Required Document Check | Verifies presence of mandatory uploaded document types. |
| **`DOCUMENT_VALIDITY`**| Signature/Integrity Check | Verifies digital signature, PDF integrity, or QR code validity. |
| **`FIELD_MATCH`** | String Comparison | Compares bidder value vs. source value (Exact, Normalized, Alias). |
| **`CROSS_DOCUMENT_CONSISTENCY`**| Cross-Document Alignment | Verifies consistency across multiple documents (e.g., PAN in GST vs. Income Tax). |
| **`GOVERNMENT_VERIFICATION`**| Govt Source Match | Evaluates normalized `GovernmentVerificationResult` status. |
| **`CALCULATION`** | Mathematical Formula | Computes derived values (e.g., `average_turnover = sum(3_years) / 3`). |
| **`AGGREGATION`** | Multi-Requirement Aggregate| Combines child requirement outcomes into composite status. |
| **`CONDITIONAL`** | If-Then-Else Branching | Evaluates rules based on conditional prerequisites (e.g., If MSME then Exempt EMD). |
| **`COMPOSITE`** | Tree of Nested Rules | Logical AST combining AND/OR child rule conditions. |

---

## 4. Entity Attribute Specifications

### 4.1 `TenderRequirement` Attributes
* `requirement_id`: ULID string (Primary Key)
* `tender_id`: ULID string (Foreign Key $\rightarrow$ `Tender`)
* `tender_version_id`: ULID string (Foreign Key $\rightarrow$ `TenderVersion`)
* `clause_number`: String (e.g., `"Clause 4.2.1"`)
* `title`: String
* `description`: Text
* `category`: Category Enum (`TAX`, `FINANCIAL`, `LOCAL_CONTENT`, etc.)
* `is_mandatory`: Boolean (`True` = mandatory requirement; `False` = optional)
* `applicability_condition_ast`: JSON object (AST condition governing requirement applicability)
* `effective_date`: ISO 8601 Date string
* `evaluation_priority`: Integer (Order of evaluation)
* `human_review_required`: Boolean

### 4.2 `ComplianceRule` Attributes
* `rule_id`: ULID string (Primary Key)
* `rule_code`: String (e.g., `"RULE-GST-ACTIVE-STATUS"`)
* `version`: Integer (Version sequence 1, 2, 3...)
* `rule_type`: Type Enum (`THRESHOLD`, `FIELD_MATCH`, `GOVERNMENT_VERIFICATION`, etc.)
* `description`: Text
* `policy_version_id`: ULID string (Foreign Key $\rightarrow$ `PolicyVersion`)
* `condition_ast`: JSON object (Safe, non-executable AST condition tree)
* `required_fact_keys`: Array of strings (e.g., `["gstin_status", "legal_name"]`)
* `output_status_on_pass`: Enum (`PASS`)
* `output_status_on_fail`: Enum (`FAIL`, `REQUIRES_HUMAN_REVIEW`)
* `severity_class`: Enum (`DISQUALIFYING_IF_PROVEN`, `MATERIAL_REVIEW`, `NON_MATERIAL_REVIEW`, `INFORMATIONAL`)
* `explainability_template`: Text (Jinja-style template rendered for evaluation traces)
* `is_active`: Boolean
* `created_at`: ISO 8601 Timestamp

### 4.3 `RequirementRuleMap` Attributes
* `mapping_id`: ULID string (Primary Key)
* `requirement_id`: ULID string (Foreign Key $\rightarrow$ `TenderRequirement`)
* `rule_id`: ULID string (Foreign Key $\rightarrow$ `ComplianceRule`)
* `evaluation_order`: Integer
* `is_active`: Boolean
