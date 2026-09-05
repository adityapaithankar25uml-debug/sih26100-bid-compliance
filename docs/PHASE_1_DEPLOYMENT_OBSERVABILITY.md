# Phase 1 — Deployment Observability Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Deployment Observability Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification integrates the Task 9 Observability Architecture into the deployment and release lifecycle. It defines release telemetry events, deployment health verification metrics, rollback triggers, and deployment audit tracking.

---

## 2. Deployment Telemetry Event Schema (`DeploymentEvent`)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "DeploymentEvent",
  "type": "object",
  "required": [
    "timestamp",
    "deployment_id",
    "environment",
    "service_name",
    "image_tag",
    "git_commit_sha",
    "deployment_action",
    "deployment_actor",
    "deployment_status"
  ],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "deployment_id": { "type": "string" },
    "environment": { "type": "string", "enum": ["LOCAL", "DEVELOPMENT", "TEST_STAGING", "PRODUCTION"] },
    "service_name": { "type": "string", "example": "fastapi-backend" },
    "image_tag": { "type": "string", "example": "v1.1.0" },
    "git_commit_sha": { "type": "string", "example": "18af4d6..." },
    "deployment_action": { "type": "string", "enum": ["START_DEPLOY", "CANARY_SHIFT", "HEALTH_CHECK_PASS", "HEALTH_CHECK_FAIL", "ROLLBACK_TRIGGERED", "DEPLOY_COMPLETE"] },
    "deployment_actor": { "type": "string", "example": "cicd-runner-prod-01" },
    "deployment_status": { "type": "string", "enum": ["IN_PROGRESS", "SUCCESS", "FAILED", "ROLLED_BACK"] }
  }
}
```

---

## 3. Deployment Health Metrics & Rollback Triggers

| Metric Name | Metric Type | Rollback Trigger Threshold | Automated Action |
|---|---|---|---|
| `deployment_http_5xx_error_rate` | Gauge (%) | HTTP 5xx rate $> 2.0\%$ during release window | Automated rollback to Blue container tasks |
| `deployment_p95_latency_ms` | Gauge (ms) | p95 request latency $> 1,500$ ms for 3 minutes | Automated rollback to Blue container tasks |
| `deployment_readiness_probe_failures` | Counter | Failed readiness checks $> 3$ consecutive probes | Abort deployment before ALB traffic shift |
| `deployment_db_migration_errors` | Counter | Any DDL migration error or lock timeout | Rollback code tasks; alert Lead Database Admin |
