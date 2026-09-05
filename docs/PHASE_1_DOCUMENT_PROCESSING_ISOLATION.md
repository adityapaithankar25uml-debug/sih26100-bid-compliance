# Phase 1 — Document Processing Isolation Architecture

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Document Isolation Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the isolated document processing architecture for parsing, OCR, and disarming untrusted uploaded tender documents (PDFs, images, Office docs).

The foundational security rule for document processing is:
> **"All uploaded bidder documents are untrusted content vectors. Document parsing, OCR extraction, and disarming execute inside isolated sandbox containers with zero network access and strict resource boundaries."**

---

## 2. Document Processing Sandbox Isolation Topology

```mermaid
sequenceDiagram
    autonumber
    participant Bidder as Bidder / User
    participant API as FastAPI Ingestion API
    participant S3Quarantine as S3 Raw Quarantine Bucket
    participant Worker as Isolated CDR Sandbox Worker
    participant ClamAV as ClamAV Scanner Engine
    participant S3Clean as S3 Disarmed Clean Bucket

    Bidder->>API: 1. Upload Bid Document (PDF / ZIP)
    API->>S3Quarantine: 2. Store Raw File (Object Metadata: untrusted_content=TRUE)
    API->>Worker: 3. Dispatch Sandbox Parsing Task
    
    Note over Worker: Zone 2 Sandbox Container (Zero Network Egress)
    Worker->>S3Quarantine: 4. Fetch Raw File Stream
    Worker->>ClamAV: 5. Execute Malware Scan
    Alt Malware Virus Detected
        ClamAV-->>Worker: Malicious File Alert
        Worker->>S3Quarantine: Delete File & Log Security Event
    Else File Clean
        ClamAV-->>Worker: Scan Passed
        Worker->>Worker: 6. Parse PDF Structure & Flatten Macros / Disarm
        Worker->>S3Clean: 7. Store Disarmed PDF & Extracted Plaintext
    End
```

---

## 3. Sandbox Container Isolation Rules

| Security Layer | Sandbox Isolation Parameter | Architectural Enforce Mechanism |
|---|---|---|
| **Network Isolation** | **Zero Outbound Egress** | Document-processing workloads operate in a network-isolated execution boundary with no outbound network access by default; implementation may use runtime-specific network isolation such as disabled networking |
| **Filesystem Isolation** | **Read-Only Root Filesystem** | Mount root `/` as read-only; use ephemeral `tmpfs` RAM-disk for `/tmp` scratch |
| **Resource Limits** | **Strict CPU & Memory Caps** | Workload containers execute under defined CPU/RAM caps; auto-kill on `OOMKilled` threshold breach |
| **Process Privileges** | **Non-Root & Capability Hardening** | Containers should run as non-root identities and drop unnecessary Linux capabilities; exact UID/GID and capability configuration are implementation-specific and validated through security testing |
| **Execution Timeout** | **Hard Task Deadline** | Celery task timeout hard kill enforced per document page/file processing task |
| **Original Evidence Preservation** | **Immutability Protection** | Original raw file hash is recorded in `EvidenceRecord` before processing |

---

## 4. Derived Text Sanitization & Untrusted Tagging

1. **Untrusted Metadata Tag:** All extracted text, OCR outputs, and table structures carry an immutable attribute `untrusted_content_source = TRUE`.
2. **Pre-AI Injection Filtering:** Extracted text passes through the Pre-AI Privacy Gateway for prompt injection pattern scanning before LLM processing.
