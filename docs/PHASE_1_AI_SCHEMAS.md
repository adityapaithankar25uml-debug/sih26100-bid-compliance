# Phase 1 AI Schemas Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-023  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document provides formal JSON Schema specifications for structured AI task payloads. No FastAPI models, Pydantic Python classes, or code files are created.

---

## 1. Document Classification Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.bidcompliance.cpcl.gov.in/v1/DocumentClassificationSchema.json",
  "title": "DocumentClassificationSchema",
  "type": "object",
  "required": ["document_id", "predicted_doc_type", "confidence_score", "page_range"],
  "properties": {
    "document_id": { "type": "string", "format": "uuid" },
    "predicted_doc_type": {
      "type": "string",
      "enum": [
        "CA_TURNOVER_CERTIFICATE",
        "GST_REGISTRATION_CERTIFICATE",
        "UDYAM_REGISTRATION_CERTIFICATE",
        "PAN_CARD",
        "EMD_PAYMENT_RECEIPT",
        "DEBARMENT_AFFIDAVIT",
        "TECHNICAL_SPECIFICATION_SHEET",
        "PAST_EXPERIENCE_ORDER",
        "ISO_CERTIFICATE",
        "OTHER_UNCLASSIFIED"
      ]
    },
    "confidence_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "page_range": {
      "type": "object",
      "required": ["start_page", "end_page"],
      "properties": {
        "start_page": { "type": "integer", "minimum": 1 },
        "end_page": { "type": "integer", "minimum": 1 }
      }
    }
  }
}
```

---

## 2. Extracted Fields Envelope Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.bidcompliance.cpcl.gov.in/v1/ExtractedFieldsEnvelopeSchema.json",
  "title": "ExtractedFieldsEnvelopeSchema",
  "type": "object",
  "required": ["extraction_id", "source_document_id", "extracted_fields"],
  "properties": {
    "extraction_id": { "type": "string" },
    "source_document_id": { "type": "string", "format": "uuid" },
    "extracted_fields": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["field_name", "extracted_value", "confidence_score", "page_number", "bounding_box"],
        "properties": {
          "field_name": { "type": "string" },
          "extracted_value": { "type": ["string", "number", "boolean", "null"] },
          "unit": { "type": ["string", "null"] },
          "confidence_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
          "page_number": { "type": "integer", "minimum": 1 },
          "bounding_box": {
            "type": "object",
            "required": ["x0", "y0", "x1", "y1"],
            "properties": {
              "x0": { "type": "number" },
              "y0": { "type": "number" },
              "x1": { "type": "number" },
              "y1": { "type": "number" }
            }
          }
        }
      }
    }
  }
}
```

---

## 3. Tender Requirement Candidate List Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.bidcompliance.cpcl.gov.in/v1/TenderRequirementCandidateListSchema.json",
  "title": "TenderRequirementCandidateListSchema",
  "type": "object",
  "required": ["tender_version_id", "candidate_requirements"],
  "properties": {
    "tender_version_id": { "type": "string", "format": "uuid" },
    "candidate_requirements": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["requirement_code", "category", "description", "is_mandatory", "suggested_rule_id"],
        "properties": {
          "requirement_code": { "type": "string" },
          "category": {
            "type": "string",
            "enum": ["FINANCIAL_TURNOVER", "PAST_EXPERIENCE", "STATUTORY_COMPLIANCE", "EMD_REQUIREMENT", "LOCAL_CONTENT"]
          },
          "description": { "type": "string" },
          "threshold_value": { "type": ["number", "string", "null"] },
          "unit": { "type": ["string", "null"] },
          "is_mandatory": { "type": "boolean" },
          "suggested_rule_id": { "type": "string" }
        }
      }
    }
  }
}
```

---

## 4. Anomaly Signal List Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://schemas.bidcompliance.cpcl.gov.in/v1/AnomalySignalListSchema.json",
  "title": "AnomalySignalListSchema",
  "type": "object",
  "required": ["submission_id", "anomaly_signals"],
  "properties": {
    "submission_id": { "type": "string", "format": "uuid" },
    "anomaly_signals": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["signal_code", "severity", "description", "affected_document_ids"],
        "properties": {
          "signal_code": { "type": "string" },
          "severity": { "type": "string", "enum": ["HIGH", "MEDIUM", "LOW"] },
          "description": { "type": "string" },
          "affected_document_ids": {
            "type": "array",
            "items": { "type": "string", "format": "uuid" }
          }
        }
      }
    }
  }
}
```
