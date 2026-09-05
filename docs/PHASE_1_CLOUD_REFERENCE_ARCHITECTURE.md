# Phase 1 — Cloud Reference Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Cloud Reference Architecture Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the cloud reference architecture for deploying the SIH26100 platform on cloud infrastructure (using AWS as a conceptual reference framework). 

> **"This specification represents a conceptual reference architecture. No cloud resources, VPCs, compute clusters, or databases are provisioned or deployed in Task 10."**

---

## 2. Conceptual Cloud Topology Diagram

```mermaid
flowchart TD
    subgraph Edge_Protection ["1. Edge Protection Layer"]
        CF["AWS CloudFront / Edge CDN"]
        WAF["AWS WAF (Web Application Firewall)"]
        Shield["AWS Shield DDoS Defense"]
    end

    subgraph Public_Subnets ["2. Public Subnet Tier (DMZ)"]
        ALB["Application Load Balancer (ALB)"]
        NAT["NAT Gateways (AZ-a / AZ-b)"]
    end

    subgraph Private_App_Subnets ["3. Private Application Tier (Isolated)"]
        ECS_API["Amazon ECS (FastAPI Backend Tasks)"]
        ECS_UI["Amazon ECS (Next.js Frontend Tasks)"]
        ECS_AIGw["Amazon ECS (Pre-AI Privacy Gateway)"]
    end

    subgraph Private_Worker_Subnets ["4. Private Worker Tier (No Ingress)"]
        Celery_Core["Celery Background Worker Pool"]
        Celery_OCR["Celery Document OCR Worker Pool"]
        Quarantine_Sandbox["Quarantined Document Parsing Worker Pool"]
    end

    subgraph Private_Data_Subnets ["5. Private Data & Storage Tier (Strict DB Security)"]
        RDS_PG[(\"Amazon RDS PostgreSQL (pgvector + Audit Chain)\")]
        Elasticache[(\"Amazon ElastiCache Redis (Queue & Cache)\")]
        S3_Docs[(\"Amazon S3 (Encrypted Evidence & Document Bucket)\")]
        KMS["AWS KMS (Key Management Service)"]
        Secrets["AWS Secrets Manager"]
    end

    Edge_Protection --> Public_Subnets
    Public_Subnets --> Private_App_Subnets
    Private_App_Subnets --> Private_Worker_Subnets
    Private_App_Subnets --> Private_Data_Subnets
    Private_Worker_Subnets --> Private_Data_Subnets
```

---

## 3. Core Cloud Infrastructure Components Mapping

| Component | AWS Reference Service | Conceptual Configuration & Policy |
|---|---|---|
| **Edge & Firewall** | AWS WAF + CloudFront | Rate limiting, SQLi/XSS rule sets, GeM IP restrictions, Secure TLS termination |
| **Ingress Load Balancing** | Application Load Balancer (ALB) | Dual-AZ deployment, private target groups, health check probes (`/health/readiness`) |
| **Application Compute** | AWS ECS (Fargate) | Serverless container execution, non-root user, read-only root filesystems, task execution roles |
| **Async Background Compute** | AWS ECS (Fargate Task Workers) | Auto-scaling worker tasks based on Redis queue depth, isolated task execution roles |
| **Relational Database** | AWS RDS PostgreSQL 16+ | Multi-AZ deployment, `pgvector` extension enabled, AES-256 storage encryption, automated backups |
| **In-Memory Cache & Queue** | AWS ElastiCache for Redis | Multi-node cluster mode, transit encryption (TLS), auth token verification, daily snapshots |
| **Object Storage** | AWS S3 Bucket Family | Dedicated evidence buckets, KMS-SSE encryption, object versioning enabled, legal hold support |
| **Secret Management** | AWS Secrets Manager + KMS | Automated secret rotation, KMS envelope encryption, task IAM role access policies |
| **Monitoring & Telemetry** | AWS CloudWatch + OpenTelemetry | Container Insights, log group retention policies, metric alarms, X-Ray trace ingestion |

---

## 4. Cloud Infrastructure Security Boundary

1. **Zero Direct Internet Exposure:** PostgreSQL, Redis, Celery workers, and S3 buckets reside exclusively in private data subnets with zero public IP addresses.
2. **KMS Envelope Encryption:** Data at rest across S3 buckets, RDS storage, and Secrets Manager is encrypted using customer-managed KMS keys.
3. **Task IAM Least Privilege:** ECS task roles are strictly scoped; the API task cannot access S3 raw document quarantine buckets, and OCR workers cannot modify PostgreSQL audit tables directly.
