# Phase 1 Data Flow Specifications & Diagrams

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-004  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 establishes research and architecture inputs; government integrations requiring authorization remain subject to official onboarding/approval.

---

## Flow A: Complete System Architecture Overview

```mermaid
flowchart TD
    subgraph UI ["Presentation Layer (Next.js / React)"]
        A1["Procurement Officer Workbench"]
        A2["Split-Screen PDF Bounding-Box Viewer"]
        A3["Audit & Decision Dashboard"]
    end

    subgraph API ["Application API Layer (FastAPI)"]
        B1["Auth & RBAC Middleware"]
        B2["Tender API Router"]
        B3["Bidder API Router"]
        B4["Evaluation Router"]
    end

    subgraph CORE ["Domain Engine Core"]
        C1["Tender Requirement Intelligence"]
        C2["Document Intelligence & OCR"]
        C3["Deterministic Rule Engine"]
        C4["Make in India Policy Engine"]
        C5["3D Risk & Scoring Engine"]
    end

    subgraph GW ["Integration Gateway"]
        D1["Government Verification Gateway"]
        D2["Adapter Router (LIVE / MOCK / MANUAL)"]
    end

    subgraph AI ["AI Processing Layer"]
        E1["AI Provider Wrapper"]
        E2["Sanitization & Schema Guard"]
        E3["Gemini / OpenAI / Ollama"]
    end

    subgraph DATA ["Storage & Evidence Layer"]
        F1[("PostgreSQL DB")]
        F2[("MinIO Object Storage")]
        F3[("Redis Cache")]
        F4["Immutable Audit Log (SHA-256 Chain)"]
    end

    A1 -->|REST API| B1
    B1 --> B2 & B3 & B4
    B2 --> C1
    B3 --> C2
    B4 --> C3 & C5
    C1 & C2 --> E1
    E1 --> E2 --> E3
    C3 --> C4 & D1
    D1 --> D2
    C3 & C5 --> F1 & F4
    C2 --> F2
    D2 --> F3
```

---

## Flow B: Tender Ingestion & Requirement Intelligence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Officer as Procurement Officer
    participant UI as Next.js Web UI
    participant API as FastAPI Backend
    participant DocMgr as Document Management
    participant Storage as MinIO Storage
    participant AI as AI Provider Wrapper
    participant RuleEng as Compliance Ontology
    participant DB as PostgreSQL DB

    Officer->>UI: Upload Tender NIT PDF
    UI->>API: POST /tenders/upload (File Stream)
    API->>DocMgr: Ingest Document (Validate Magic Bytes + SHA-256)
    DocMgr->>Storage: Store Raw PDF
    DocMgr-->>API: File ID & Hash
    API->>AI: Extract Requirement Criteria (Text Stream)
    AI->>AI: Sanitize & Force Pydantic Schema
    AI-->>API: Proposed Requirements (Turnover, Exp, MII, EMD)
    API->>UI: Display Extracted Requirements Workbench
    Officer->>UI: Review & Modify/Confirm Requirements
    UI->>API: POST /tenders/{id}/confirm-rules
    API->>RuleEng: Parameterize Confirmed Requirements Schema
    API->>DB: Save Active Tender Requirements State
    API-->>UI: Confirmation Success & Activated Rule Set
```

---

## Flow C: Bidder Document Verification & Field Extraction Flow

```mermaid
sequenceDiagram
    autonumber
    actor Bidder as Bidder / Officer Upload
    participant UI as Next.js Web UI
    participant API as FastAPI Backend
    participant DocIntel as Document Intelligence
    participant Storage as MinIO Storage
    participant AI as AI Provider Wrapper
    participant DB as PostgreSQL DB

    Bidder->>UI: Batch Upload Bidder Documents (Cover 1 & Cover 2)
    UI->>API: POST /bidders/{id}/documents/batch
    API->>Storage: Store Files (Encrypted Blob Storage)
    API->>DocIntel: Trigger Ingestion Pipeline
    DocIntel->>AI: Classify Document Types (GST, PAN, CA Audit, OEM Cert)
    AI-->>DocIntel: Document Classifications & Confidence
    DocIntel->>AI: Extract Fields & Coordinates (OCR)
    AI-->>DocIntel: Extracted Fields + Token Coordinates [x0, y0, x1, y1]
    DocIntel->>DB: Save Extracted Fields & Bounding Boxes
    DocIntel-->>API: Extraction Complete Event
    API-->>UI: Update Bidder Profile with Extracted Data & Confidence Indicators
```

---

## Flow D: Multi-Tier Government Verification Gateway Flow

```mermaid
flowchart TD
    A["Verification Trigger (Identifier: GSTIN / PAN / CIN)"] --> B{"Check Gateway Router"}
    B -->|Check Configured Mode| C{"Mode Selection"}
    
    C -->|LIVE Mode| D["Execute Production Government API (Protean / GSP)"]
    C -->|SANDBOX Mode| E["Execute Staging Sandbox API (DigiLocker / Setu)"]
    C -->|MOCK Mode| F["Execute Local Hackathon Mock Gateway"]
    C -->|MANUAL Mode| G["Route to Officer Manual Document Workflow"]

    D --> H{"Response Success?"}
    E --> H
    F --> I["Return Pre-configured Response [MOCK_SIMULATED]"]
    G --> J["Officer Uploads Verification Proof [MANUAL_VERIFIED]"]

    H -->|Yes| K["Return API Payload [LIVE_VERIFIED / SANDBOX_VERIFIED]"]
    H -->|No / Timeout| L["Trigger Resilience Fallback (Circuit Breaker)"]
    L --> M["Status: NOT_VERIFIED / MANUAL_FALLBACK"]

    I & J & K & M --> N["Cache Result in Redis with TTL"]
    N --> O["Record Timestamped Verification Artifact in DB"]
```

---

## Flow E: Deterministic Compliance Evaluation Flow

```mermaid
flowchart TD
    subgraph INPUT ["Input Ingestion"]
        A1["Verified Bidder Metrics"]
        A2["Extracted Document Data"]
        A3["Confirmed Tender Requirement Schema"]
    end

    subgraph EXEC ["Deterministic Execution Pipeline"]
        B1["PAN-GSTIN Checksum & Slicing Match"]
        B2["Turnover & Financial Threshold Comparison"]
        B3["Experience Years Numeric Comparison"]
        B4["Make in India Local Content % Calculation"]
        B5["Debarment & Blacklist Match Check"]
    end

    subgraph STATUS ["Status Assignment Matrix"]
        C1{"All Criteria Satisfied?"}
        C2["Status: PASS"]
        C3{"Mandatory Failure?"}
        C4["Status: FAIL (Escalate Risk = 100)"]
        C5["Status: REVIEW / MISSING / CONFLICT"]
    end

    subgraph OUTPUT ["3D Score Computation"]
        D1["Compliance Score (0-100)"]
        D2["Evidence Confidence (0-100)"]
        D3["Risk Score (0-100)"]
    end

    INPUT --> EXEC
    B1 & B2 & B3 & B4 & B5 --> C1
    C1 -->|Yes| C2
    C1 -->|No| C3
    C3 -->|Yes| C4
    C3 -->|No| C5
    C2 & C4 & C5 --> OUTPUT
```

---

## Flow F: Evidence Generation & Provenance Chain Flow

```mermaid
sequenceDiagram
    autonumber
    participant RuleEng as Compliance Rule Engine
    participant EvLedger as Evidence Ledger Module
    participant DocIntel as Document Intelligence
    participant GW as Verification Gateway
    participant Audit as Audit Logger
    participant DB as PostgreSQL DB

    RuleEng->>EvLedger: Create Evidence Record for Requirement
    EvLedger->>DocIntel: Fetch Field Source Location
    DocIntel-->>EvLedger: Return Page Number & Bounding-Box [x0, y0, x1, y1]
    EvLedger->>GW: Fetch Verification Payload Reference
    GW-->>EvLedger: Return API Timestamp & Mode Payload
    EvLedger->>EvLedger: Generate SHA-256 Hash of Evidence Payload
    EvLedger->>DB: Store Linked Evidence Record
    EvLedger->>Audit: Append Evidence Block to Hash Chain
    Audit-->>RuleEng: Return Confirmed Evidence Reference ID
```

---

## Flow G: Officer Decision & Manual Override Flow

```mermaid
sequenceDiagram
    autonumber
    actor Officer as Senior Procurement Officer
    participant UI as Next.js Web UI
    participant PDF as Split PDF Viewer
    participant API as FastAPI Backend
    participant DecModule as Decision Workflow
    participant Audit as Audit Trail Logger
    participant DB as PostgreSQL DB

    Officer->>UI: Inspect Bidder Evaluation Profile
    UI->>PDF: Render Source PDF with Bounding Box Highlight
    Officer->>UI: Select Manual Override Action (e.g. FAIL -> PASS)
    UI->>UI: Prompt Mandatory Rationale Entry
    Officer->>UI: Input Rationale Text & Click Confirm Override
    UI->>API: POST /evaluations/{id}/override (Action + Rationale)
    API->>DecModule: Process Override State Transition
    DecModule->>DB: Save Overridden Status + Officer User ID + Rationale
    DecModule->>Audit: Append Signed Override Block to SHA-256 Log Chain
    Audit-->>API: Override Event Sealed
    API-->>UI: Render Overridden Status Badge & Record Decision
```

---

## Flow H: Failure & Degraded-Mode Resilience Flow

```mermaid
flowchart TD
    A["Verification Request to External Government API"] --> B{"Circuit Breaker State?"}
    
    B -->|OPEN (Tripped)| C["Bypass External Network Call"]
    B -->|CLOSED (Normal)| D["Dispatch HTTP Request (Timeout = 10s)"]

    D --> E{"HTTP Response Status"}
    E -->|200 OK| F["Parse Data & Update Success Count"]
    E -->|5xx Error / Timeout / Connection Failed| G["Increment Failure Counter"]

    G --> H{"Failure Count >= Threshold (5)?"}
    H -->|Yes| I["Trip Circuit Breaker to OPEN State"]
    H -->|No| J["Log API Error Event"]

    C & I & J --> K["Fallback Execution: Transition Status to NOT_VERIFIED / MANUAL_FALLBACK"]
    K --> L["Preserve Error Trace Artifact in DB"]
    L --> M["Notify Procurement Officer: Manual Document Verification Required"]
    M --> N["System Continues Independent Evaluation Tasks (Zero Crash)"]
```
