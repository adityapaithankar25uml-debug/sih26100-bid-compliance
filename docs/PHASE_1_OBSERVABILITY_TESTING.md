# Phase 1 — Telemetry Validation & Observability Testing Strategy Architecture

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 9 Observability Testing Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the observability testing strategy and telemetry validation framework for the SIH26100 platform. Operational observability, logging redaction, distributed trace propagation, and alert rules must be systematically tested to ensure telemetry reliability during production operations.

The governing observability testing principle is:
> **"Observability testing protocols validate log schema compliance, redaction effectiveness, trace context propagation, and alert accuracy. All testing protocols are framed as future implementation and operational testing specifications."**

---

## 2. Seventeen Telemetry Validation Test Categories

| Test Category ID | Test Category Name | Test Scope & Objective | Test Protocol & Verification Method | Target Acceptance Criteria |
|---|---|---|---|---|
| **OT-01** | **Logging Schema Validation** | Verify all application logs conform to `LogEvent` JSON schema. | Automated log validator checking mandatory JSON fields in log streams. | 100% of emitted logs conform to `LogEvent` schema. |
| **OT-02** | **Sensitive Data Redaction** | Verify Pre-Log Privacy Proxy scrubs passwords, tokens, and PII. | Submitting synthetic log inputs containing test passwords and PAN numbers. | Zero unredacted passwords or PII in output log streams. |
| **OT-03** | **Correlation Propagation** | Verify `correlationId` propagates across async Celery tasks. | Invoking API request and inspecting task log entries across worker nodes. | 100% of child log events match parent `correlationId`. |
| **OT-04** | **Distributed Trace Propagation**| Verify W3C `traceparent` headers propagate through gateway to adapters. | Inspecting distributed trace spans across API, worker, AI, and Govt gateways. | Complete trace span graph constructed without broken parent IDs. |
| **OT-05** | **Metric Correctness** | Verify metric counters increment correctly during API and job execution. | Executing N synthetic API requests and checking Prometheus `/metrics` values. | Metric counters match exact HTTP transaction counts. |
| **OT-06** | **Alert Rule Correctness** | Verify alert rules fire when metric thresholds are breached. | Simulating 5xx error spikes and 504 timeouts in staging test environment. | Firing alert generated within 3 minutes; runbook link valid. |
| **OT-07** | **Dashboard Authorization** | Verify role-based authorization rules on visual dashboard endpoints. | Invoking dashboard routes under `ProcurementOfficer` vs `Auditor` roles. | Unauthorized dashboards return 403 Forbidden; org data filtered. |
| **OT-08** | **Telemetry Retention Cleanups**| Verify automated retention cleanup jobs purge expired log indices. | Triggering mock retention cleanup job in staging environment. | Expired indices purged; locked `LegalHold` tenders preserved. |
| **OT-09** | **Failure Classification** | Verify system failure codes (`FL-01` to `FL-16`) logged accurately. | Injecting artificial timeouts and malformed JSON payloads in test runner. | Failure categories correctly tagged in log events. |
| **OT-10** | **Queue Monitoring Validation** | Verify `celery_queue_depth` metrics match actual Redis queue sizes. | Injecting 100 test jobs into Redis queue and checking gauge metric. | Metric gauge matches exact Redis queue depth. |
| **OT-11** | **AI Telemetry Validation** | Verify `AITelemetryEvent` captures model ID, tokens, and prompt hash. | Executing mock AI extraction calls and inspecting AI log streams. | All AI provenance attributes recorded accurately. |
| **OT-12** | **Govt Integration Telemetry** | Verify separation of 504 transport timeouts from business `UNMATCHED` results. | Injecting simulated 504 timeouts into government adapter mock. | Transport failure logged; compliance status NOT set to `FAIL`. |
| **OT-13** | **Compliance Trace Validation** | Verify AST calculation trace logging for rule evaluation runs. | Executing rule engine tests and inspecting diagnostic calculation traces. | Diagnostic trace logs exact AST comparison logic. |
| **OT-14** | **Audit Linkage Validation** | Verify `LogEvent` records capture valid `audit_event_id` references. | Triggering manual officer override and checking log cross-references. | Log event includes committed PostgreSQL `audit_event_id`. |
| **OT-15** | **Security Telemetry Tests** | Verify security alerts generated for rate-limit breaches and virus detects. | Submitting virus test file (EICAR) and triggering rate-limit floods. | Security telemetry events emitted instantly. |
| **OT-16** | **Incident Correlation Tests** | Verify incident telemetry aggregates logs/traces during simulated SEV-1 alerts.| Simulating DB outage and verifying incident timeline aggregation. | Incident timeline snapshot generated cleanly. |
| **OT-17** | **Observability Resilience** | Verify API stays responsive when log aggregator is unreachable. | Terminating log aggregator container in staging environment. | API continues processing transactions; drops non-critical logs cleanly. |

---

## 3. Future Implementation Notice
All testing protocols, validation scripts, and automated test runners described in this specification represent **Future Testing Specifications**. Zero test execution code is implemented in Task 9.
