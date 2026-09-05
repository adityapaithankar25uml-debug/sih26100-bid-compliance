# Phase 1 Architecture Principles (Architectural Constitution)

**Project:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
**Organization:** Ministry of Petroleum & Natural Gas / CPCL
**Phase:** Phase 1 — Architecture & Design
**Task:** Task 12 — Final Architecture Integration, Consistency, Traceability & Implementation Readiness Review
**Document Status:** DESIGN DRAFT / READ-ONLY VALIDATION READY

---

## 1. Executive Summary & Purpose

This document articulates the 10 foundational architecture principles governing the SIH26100 platform. These principles serve as the **Architectural Constitution** for Phase 2 engineering teams. Every design choice, module structure, API interface, and code implementation must align with these principles.

---

## 2. The 10 Core Architecture Principles

### PRINCIPLE 1: Human Authority & Accountability
$$\text{AI INTERPRETS} \longrightarrow \text{AUTHORIZED SOURCES VERIFY} \longrightarrow \text{RULES EVALUATE} \longrightarrow \text{EVIDENCE PROVES} \longrightarrow \text{HUMAN APPROVES}$$
- **Guidance:** Software automated evaluation provides evidence and recommendation; human Procurement Officers hold final legal authority and accountability for bid qualification decisions.

### PRINCIPLE 2: Deterministic Rule Authority
- **Guidance:** Compliance evaluations must be strictly deterministic, reproducible, and verifiable via versioned Python AST policy execution. Probabilistic models (LLMs/VLMs) extract facts but never evaluate policy rules.

### PRINCIPLE 3: End-to-End Evidence Provenance
- **Guidance:** Every compliance claim must trace back to concrete evidence: bounding boxes on source PDFs, cryptographically verified government API tokens, and deterministic AST execution traces. Unbacked assertions are invalid.

### PRINCIPLE 4: Fault-Tolerant Government Verification
- **Guidance:** Integration with official Indian government registers (GSTN, MCA21, UDIN) must assume external API volatility. Technical transport failures must degrade gracefully to `MANUAL_FALLBACK` and must never penalize the bidder.

### PRINCIPLE 5: Zero-Trust Security & Backend AuthZ
- **Guidance:** Rely on zero client trust. All authorization, scope checking, input sanitization, and document permission verifications are enforced authoritatively on the backend. The frontend is purely a presentation interface.

### PRINCIPLE 6: Immutability & Audit Lineage
- **Guidance:** Domain history, tender versions, policy rules, evidence records, officer decisions, and system activities must be recorded using append-only semantics and SHA-256 cryptographic hash chaining. Historical evaluation context must remain permanently reconstructible.

### PRINCIPLE 7: Multidimensional Status Isolation
- **Guidance:** Never collapse distinct operational dimensions into a single score. Compliance status, qualification outcome, AI confidence score, risk score, government verification state, and workflow execution status must remain strictly separated.

### PRINCIPLE 8: Stateless Compute & Container Portability
- **Guidance:** Application backend, Celery workers, AI gateway, and frontend components must remain strictly stateless OCI containers. Cloud infrastructure (e.g., AWS ECS Fargate) is a reference deployment model; code must remain 100% portable to any container runtime.

### PRINCIPLE 9: Decoupled Operational Observability
- **Guidance:** Logs, Prometheus metrics, and OpenTelemetry traces provide operational system health monitoring. They are operational telemetry and must never be confused with or used as authoritative compliance evidence.

### PRINCIPLE 10: Strict Design-Before-Code Governance
- **Guidance:** Architecture precedes implementation. No feature, API route, or database schema change may be implemented in Phase 2 without complete alignment with Phase 1 architectural baselines and formal change governance.
