# Phase 1 — User Personas & Roles Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Personas & Roles Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & User Sphere Taxonomy

This specification defines the human user personas, permission scopes, workspace access boundaries, and task responsibilities for the platform, aligning strictly with Task 8 security identity spheres.

Machine identities (`SERVICE_WORKER`) execute automated background tasks and **DO NOT** possess human UI persona interfaces.

---

## 2. Authorized Persona Specifications

### 2.1 Persona 1: Procurement Officer (`PROCUREMENT_OFFICER`)
- **Role Summary:** Primary human operational user responsible for conducting bid compliance evaluations, reviewing evidence, resolving ambiguities, and recording authoritative qualification decisions.
- **Core Goals:** Evaluate technical and financial bid compliance efficiently, inspect evidence lineages, verify government registry findings, and record legally defensible qualification decisions.
- **UI Workspace Access:** Dashboard, Tender Workspace, Bidder Workspace, Compliance Matrix, Document Viewer, Human Review Workspace, Officer Decision Workspace.
- **Authority Boundaries:** Possesses sole authority to record initial `OfficerDecision` records (`QUALIFIED`, `NOT_QUALIFIED`, `PENDING_REVIEW`). Cannot alter historical audit logs or modify system rule definitions.

### 2.2 Persona 2: Senior Reviewer (`SENIOR_REVIEWER`)
- **Role Summary:** Supervisory officer responsible for reviewing high-value tenders, policy exceptions, manual overrides, four-eyes policy reviews, and contested qualification decisions.
- **Core Goals:** Ensure consistency across procurement decisions, validate officer manual overrides, review high-risk flags, and provide supervisory sign-off.
- **UI Workspace Access:** Senior Reviewer Dashboard, Exception & Conflict UI, Decision Workspace (Approval View), Compliance Matrix, Audit Explorer.
- **Authority Boundaries:** Approves or rejects officer override requests; provides supervisory concurrence for high-value tenders.

### 2.3 Persona 3: Auditor (`AUDITOR`)
- **Role Summary:** Independent oversight user (internal CPCL audit, CVC, CAG) responsible for inspecting procurement decision integrity, evidence provenance, and workflow history.
- **Core Goals:** Verify system transparency, confirm tamper-evident SHA-256 audit chain integrity, trace decisions back to original documents and rules, and ensure DPDP privacy compliance.
- **UI Workspace Access:** Audit Explorer UI, Evidence Lineage UI, Historical Evaluation Matrix (Read-Only Views across all workspaces).
- **Authority Boundaries:** Strictly **READ-ONLY**. Cannot record decisions, alter workflow states, execute overrides, or modify system configurations.

### 2.4 Persona 4: System Administrator (`SYSTEM_ADMIN`)
- **Role Summary:** Operational administrator managing platform deployment configuration, user accounts, integration adapters, feature flags, and system health.
- **Core Goals:** Maintain operational availability, configure government adapter integration modes, manage RBAC role assignments, monitor telemetry, and handle break-glass procedures.
- **UI Workspace Access:** System Admin Workbench, Integration Configuration UI, Feature Flag Panel, Observability Dashboards, Operational Access Logs.
- **Authority Boundaries:** Manages system configuration and operational health. **STRICTLY PROHIBITED** from recording bidder qualification decisions or mutating compliance evidence.

---

## 3. Persona Workspace Access Matrix

| Workspace / UI Function | `PROCUREMENT_OFFICER` | `SENIOR_REVIEWER` | `AUDITOR` | `SYSTEM_ADMIN` |
|---|---|---|---|---|
| **Procurement Dashboard** | Full Access | Supervisory View | Read-Only | System Metrics |
| **Tender & Bid Workspace** | Full Access | Full Access | Read-Only | Read-Only Metadata |
| **Compliance Matrix** | Full Access | Full Access | Read-Only | Read-Only |
| **Document Viewer & Extraction** | Review & Edit Extractions | Supervisory View | Read-Only | Read-Only Metadata |
| **Government Verification UI** | Trigger Verification / Review | Supervisory View | Read-Only | Adapter Status & Config |
| **Human Review Workspace** | Resolve Review Tasks | Review & Approve Overrides | Read-Only | Read-Only |
| **Officer Decision Workspace** | Record Primary Decision | Supervisory Concurrence | Read-Only | Prohibited |
| **Audit Explorer** | View Tender Audit | View Tender Audit | Full Audit Explorer | Infrastructure Logs |
| **System Admin & Config UI** | Prohibited | Prohibited | Prohibited | Full Administrative Access |
