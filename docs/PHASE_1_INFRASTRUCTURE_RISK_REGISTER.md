# Phase 1 — Infrastructure Risk Register

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Risk Register Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification establishes the Task 10 Infrastructure Risk Register documenting operational, technical, deployment, and cloud infrastructure risks.

> **"Zero risk does not exist in infrastructure architecture. Risk management requires transparent identification, rigorous controls, continuous detection, and realistic residual risk evaluation."**

---

## 2. Infrastructure Risk Register Catalog

| Risk ID | Category | Risk Description | Likelihood | Impact | Mitigation Strategy | Residual Risk | Owner |
|---|---|---|---|---|---|---|---|
| **IRK-01** | Cloud Outage | Single AWS Availability Zone outage causes platform downtime | Medium | High | Multi-AZ RDS, Multi-AZ ECS task distribution | Low | Infrastructure Lead |
| **IRK-02** | Supply Chain | Malicious third-party Python package injected via PyPI | Low | High | Pinned lockfiles, `pip-audit`, Syft SBOM scanning | Low | Security Ops |
| **IRK-03** | Worker OOM | Oversized PDF disarming crashes Celery worker node RAM | Medium | Medium | Memory limits, worker container isolation, auto-restart | Low | Operations Lead |
| **IRK-04** | Secret Leak | Secret key committed to Git repository during development | Low | High | Secret scanners (`trufflehog`), pre-commit hooks | Low | Security Ops |
| **IRK-05** | Migration Lock | Schema migration locks PostgreSQL production tables during deployment | Low | Medium | Pre-migration snapshots, 5s DDL statement timeouts | Low | Database Admin |
| **IRK-06** | Egress Block | Outbound government gateway IP allowlist changed unexpectedly | Low | High | Static EIP NAT Gateways, health probes, MANUAL_FALLBACK | Low | Integration Lead |
| **IRK-07** | Backup Failure | S3 automated WAL backup fails silently due to permission error | Low | High | Daily restoration tests, Task 9 backup alarms | Low | Database Admin |
| **IRK-08** | Image CVE | Critical zero-day vulnerability in container base image | Medium | High | Daily ECR scanning, automated base image patching | Low | Security Ops |
| **IRK-09** | Rate Throttling | External AI API rate limit breaches during peak bid upload | Medium | Medium | AI Gateway fallback to secondary model or local model | Low | AI Lead |
| **IRK-10** | Storage Exhaust | S3 storage bucket quota exceeded during document archive | Low | Medium | Storage capacity alerts, policy-controlled retention purge | Low | Infrastructure Lead |
