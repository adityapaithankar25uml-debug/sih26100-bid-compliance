# Phase 1 — Network Architecture & Subnet Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Network Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the network architecture, VPC CIDR allocations, subnet tiering, routing tables, security groups, and outbound integration boundaries for the platform.

The core network security rule is:
> **"Network boundaries strictly isolate public ingress from private application logic, worker tasks, databases, and external government API boundaries. Database and storage tiers have ZERO direct outbound internet access."**

---

## 2. VPC Subnet Allocation Topology

```mermaid
graph TD
    subgraph VPC_CIDR ["VPC: 10.100.0.0/16 (Multi-AZ Deployment)"]
        subgraph Public_Tier ["Public Subnet Tier (10.100.1.0/24 & 10.100.2.0/24)"]
            ALB["ALB (AZ-a / AZ-b)"]
            NAT["NAT Gateway (AZ-a / AZ-b)"]
        end

        subgraph Private_App_Tier ["Private Application Subnet Tier (10.100.10.0/23 & 10.100.12.0/23)"]
            FastAPI["FastAPI ECS Tasks"]
            NextUI["Next.js ECS Tasks"]
            AIGw["AI Gateway ECS Tasks"]
        end

        subgraph Private_Worker_Tier ["Private Worker Subnet Tier (10.100.20.0/23 & 10.100.22.0/23)"]
            CeleryCore["Celery Execution Workers"]
            CeleryDoc["Document Processing Workers"]
        end

        subgraph Private_Data_Tier ["Private Data Subnet Tier (10.100.30.0/24 & 10.100.31.0/24)"]
            PostgreSQL[(\"PostgreSQL Primary & Replica\")]
            RedisCluster[(\"Redis In-Memory Cluster\")]
            S3Endpoints["VPC S3 Gateway Endpoint"]
        end
    end

    Public_Tier --> Private_App_Tier
    Private_App_Tier --> Private_Worker_Tier
    Private_App_Tier --> Private_Data_Tier
    Private_Worker_Tier --> Private_Data_Tier
```

---

## 3. Security Group & Firewall Isolation Matrix

| Security Group ID | Group Name | Allowed Ingress Sources | Allowed Ingress Ports | Allowed Egress Destinations |
|---|---|---|---|---|
| **sg-01** | `alb-public-sg` | Public Internet / Edge CloudFront | TCP 443 (HTTPS) | `fastapi-app-sg`, `nextjs-app-sg` on TCP 8000/3000 |
| **sg-02** | `fastapi-app-sg` | `alb-public-sg` | TCP 8000 | `postgres-db-sg`, `redis-cache-sg`, `nat-egress-sg` |
| **sg-03** | `nextjs-app-sg` | `alb-public-sg` | TCP 3000 | `fastapi-app-sg` on TCP 8000 |
| **sg-04** | `celery-worker-sg`| `fastapi-app-sg` (Internal RPC) | None (Outbound Pull) | `postgres-db-sg`, `redis-cache-sg`, `nat-egress-sg` |
| **sg-05** | `postgres-db-sg` | `fastapi-app-sg`, `celery-worker-sg` | TCP 5432 | None (Zero Outbound Egress) |
| **sg-06** | `redis-cache-sg` | `fastapi-app-sg`, `celery-worker-sg` | TCP 6379 | None (Zero Outbound Egress) |
| **sg-07** | `nat-egress-sg` | `fastapi-app-sg`, `celery-worker-sg` | Internal Subnet IPs | External Government Gateways & AI APIs (TCP 443) |

---

## 4. Egress Gateway & Traffic Control

1. **Controlled Outbound Egress:** Outbound traffic from private subnets to external government portals (MCA, GSTN, Udyam) and AI providers passes through dedicated NAT Gateways with static IP allocations for allowlisting.
2. **VPC Endpoints:** Traffic to AWS S3, Secrets Manager, and KMS uses private VPC Endpoints (`com.amazonaws.region.s3`, `kms`, `secretsmanager`), bypassing the public internet entirely.
