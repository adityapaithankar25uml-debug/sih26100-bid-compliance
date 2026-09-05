# Phase 1 — Observability Access Control & Role-Based Telemetry Architecture

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 9 Telemetry Access Control Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the access control framework governing telemetry logs, performance metrics, distributed trace spans, operational dashboards, and audit verification endpoints. System observability cannot grant unrestricted access to operational logs or diagnostic views, as logs contain metadata regarding procurement tenders, officer actions, and system configurations.

The core observability access control principle is:
> **"Telemetry access MUST be role-restricted, capability-authorized, and organizational-context-filtered. Accessing diagnostic telemetry is itself a security-sensitive action that MUST be audited."**

---

## 2. Role-Based Telemetry Access Control Matrix

Access to observability artifacts is enforced across the five primary system roles:

| Telemetry Resource Area | ProcurementOfficer | SeniorReviewer | Auditor / Vigilance | SystemAdmin | ServiceWorker (Machine) |
|---|---|---|---|---|---|
| **Operational Health Metrics** | Read (Assigned Org) | Read (Assigned Org) | Read (All) | Read (All) | Write (Metrics API) |
| **System Dashboards (DB-01 to DB-03)** | Read (Org Filtered) | Read (Org Filtered) | Read (All) | Read (All) | No Access |
| **Workflow / Queue Telemetry (DB-04)**| Read (Assigned Bids)| Read (Org Filtered) | Read (All) | Read (All) | Write (Task Events) |
| **AI Operations Telemetry (DB-06)** | No Access | Read (Org Filtered) | Read (All) | Read (All) | Write (AI Events) |
| **Govt Adapter Telemetry (DB-07)** | No Access | Read (Org Filtered) | Read (All) | Read (All) | Write (Govt Events) |
| **Human Review Dashboards (DB-09)** | Read (Assigned Bids)| Read (Org Filtered) | Read (All) | Read (All) | No Access |
| **Security Event Logs (DB-10)** | No Access | No Access | Read (Security) | Read (All) | Write (Security Events) |
| **Audit Verification Dashboards (DB-11)**| No Access | No Access | **Full Read & Verify** | Read (Metadata Only) | Write (Audit Events) |
| **Raw JSON System Logs (`LogEvent`)** | No Access | No Access | Read (Audit Filtered)| Read (System Logs) | Write (App Logs) |
| **Distributed Trace Spans (`Span`)** | No Access | No Access | Read (Trace Spans) | Read (All Traces) | Write (Trace Spans) |

---

## 3. Organizational Context Filtering Rules

1. **Multi-Tenant Isolation:** When a Procurement Officer or Senior Reviewer views operational metrics or workflow dashboards, telemetry queries automatically append `tenant_org_id = user.tenant_org_id`. Officers cannot view metrics or job statuses belonging to other procurement divisions.
2. **Auditor Global View:** The `Auditor` role possesses cross-organizational read capabilities for compliance and vigilance oversight but remains strictly read-only across all endpoints.
3. **Auditable Diagnostic Access:** Accessing sensitive diagnostic views (such as raw log aggregators, distributed trace details, or security event logs) requires the `telemetry:read_diagnostics` capability and logs a `TELEMETRY_VIEWED` event in the application audit log.
