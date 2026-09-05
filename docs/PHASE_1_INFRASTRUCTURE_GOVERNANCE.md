# Phase 1 — Infrastructure Governance & Operational Ownership Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Governance Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines infrastructure ownership, operational change governance, IaC repository maintenance, and compliance alignment.

---

## 2. Infrastructure Ownership RACI Matrix

| Infrastructure Domain | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|---|---|---|---|---|
| **VPC & Network Topology** | Infrastructure Lead | Lead Architect | SecOps | Engineering Team |
| **Database & PgBouncer** | Database Admin | Lead Architect | Compliance Lead | Procurement Ops |
| **Container & CI/CD Pipeline**| DevOps Lead | SecOps | Core App Team | Department Lead |
| **Secrets & KMS Encryption** | SecOps | Lead Architect | Database Admin | Auditor |
| **Disaster Recovery & Backups**| Operations Lead | Lead Architect | Lead Auditor | Procurement Ops |

---

## 3. Operational Governance Cadence

1. **Monthly Infrastructure Security Review:** Review IAM roles, security group ingress rules, and container vulnerability scan logs.
2. **Quarterly Backup Restore & DR Drill:** Execute synthetic disaster recovery failover and database restoration verification in staging.
3. **Annual Compliance Alignment Review:** Verify infrastructure alignment with updated government procurement IT guidelines and CPCL organizational policies.
