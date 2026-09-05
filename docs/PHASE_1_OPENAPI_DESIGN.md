# Phase 1 OpenAPI 3.1 Specification Design Document

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-016  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document provides an OpenAPI 3.1.0 architectural specification design for future Phase 2 code generation. No application controllers, routes, or code files are created.

---

## 1. OpenAPI 3.1.0 Structural Header

```yaml
openapi: 3.1.0
info:
  title: SIH 26100 GeM Bid Compliance Verification Platform API
  description: Auditable, evidence-backed, AI-assisted bid compliance evaluation system for CPCL procurement.
  version: 1.0.0
  contact:
    name: CPCL Procurement Engineering Team
    email: procurement-support@cpcl.gov.in
servers:
  - url: https://api.bidcompliance.cpcl.gov.in/api/v1
    description: Production API Server
  - url: http://localhost:8000/api/v1
    description: Local Staging / Hackathon Demo Server
```

---

## 2. Reusable Security Schemes

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: OAuth 2.0 JWT Access Token passed in Authorization header.

security:
  - BearerAuth: []
```

---

## 3. Reusable Core Component Schemas

### 3.1 RFC 7807 Error Schema (`ProblemDetails`)
```yaml
components:
  schemas:
    ProblemDetails:
      type: object
      required:
        - type
        - title
        - status
        - detail
        - instance
        - code
        - correlation_id
        - timestamp
      properties:
        type:
          type: string
          format: uri
        title:
          type: string
        status:
          type: integer
        detail:
          type: string
        instance:
          type: string
        code:
          type: string
        correlation_id:
          type: string
          format: uuid
        timestamp:
          type: string
          format: date-time
        invalid_params:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
              reason:
                type: string
```

### 3.2 Asynchronous Job Status Schema (`JobStatusEnvelope`)
```yaml
    JobStatusEnvelope:
      type: object
      required:
        - job_id
        - status
        - job_type
        - status_endpoint
        - created_at
      properties:
        job_id:
          type: string
          example: "01HZX89J4K2P00000000000001"
        status:
          type: string
          enum: [PENDING, PROCESSING, COMPLETED, FAILED]
        job_type:
          type: string
          example: "DOCUMENT_OCR_EXTRACTION"
        progress_percentage:
          type: integer
          minimum: 0
          maximum: 100
        result_resource_url:
          type: string
        status_endpoint:
          type: string
        created_at:
          type: string
          format: date-time
```

### 3.3 Provenance Tag Schema (`ProvenanceTag`)
```yaml
    ProvenanceTag:
      type: string
      enum:
        - "[LIVE_VERIFIED]"
        - "[SANDBOX_VERIFIED]"
        - "[MOCK_SIMULATED]"
        - "[MANUAL_VERIFIED]"
      description: Mandatory visual provenance classification tag rendered on all evaluation data.
```

### 3.4 Evidence Record Schema (`EvidenceRecordSchema`)
```yaml
    EvidenceRecordSchema:
      type: object
      required:
        - evidence_id
        - requirement_code
        - evidence_type
        - provenance_tag
        - evidence_sha256
        - created_at
      properties:
        evidence_id:
          type: string
          format: uuid
        requirement_code:
          type: string
        evidence_type:
          type: string
          enum: [DOCUMENT_OCR, GOVT_API, MANUAL_PROOF]
        provenance_tag:
          $ref: '#/components/schemas/ProvenanceTag'
        document_reference:
          type: object
          properties:
            file_name:
              type: string
            page_number:
              type: integer
            bounding_box:
              type: object
              properties:
                x0: { type: number }
                y0: { type: number }
                x1: { type: number }
                y1: { type: number }
        evidence_sha256:
          type: string
          pattern: '^[a-f0-9]{64}$'
        created_at:
          type: string
          format: date-time
```

### 3.5 Officer Decision Schema (`OfficerDecisionSchema`)
```yaml
    OfficerDecisionSchema:
      type: object
      required:
        - decision_id
        - submission_id
        - officer_user_id
        - decision_choice
        - justification_rationale
        - snapshot_hash
        - decision_timestamp
      properties:
        decision_id:
          type: string
          format: uuid
        submission_id:
          type: string
          format: uuid
        officer_user_id:
          type: string
        decision_choice:
          type: string
          enum: [QUALIFY, DISQUALIFY, SEEK_CLARIFICATION]
        justification_rationale:
          type: string
          minLength: 10
        snapshot_hash:
          type: string
          pattern: '^[a-f0-9]{64}$'
        decision_timestamp:
          type: string
          format: date-time
```

---

## 4. Reusable Response Envelopes

```yaml
  responses:
    UnauthorizedError:
      description: Missing or invalid JWT access token.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'

    ForbiddenError:
      description: User role lacks RBAC permission for action.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'

    ValidationError:
      description: Parameter or Pydantic validation failure.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProblemDetails'

    JobAccepted:
      description: Asynchronous background job accepted.
      headers:
        Location:
          schema:
            type: string
          description: Polling URI for job status.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/JobStatusEnvelope'
```
