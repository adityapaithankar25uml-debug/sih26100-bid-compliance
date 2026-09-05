# Phase 1 — Infrastructure Security & Defense-in-Depth Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 10 Infrastructure Security Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines infrastructure defense-in-depth controls, security group rules, network segmentation, vulnerability management, and threat mitigations, integrating the Task 8 Security Architecture.

---

## 2. Infrastructure Defense-in-Depth Layers

```mermaid
graph TD
    subgraph Layer_1 ["Layer 1: Edge & Perimeter Defense"]
        AWS_WAF["AWS WAF (SQLi, XSS, Rate Limiting Rules)"]
        AWS_Shield["AWS Shield DDoS Protection"]
    end

    subgraph Layer_2 ["Layer 2: Network Segmentation"]
        VPC_Isolation["Multi-Tier Private Subnets (No Public DB Access)"]
        SG_Firewalls["Strict Security Group Rules"]
    end

    subgraph Layer_3 ["Layer 3: Workload & Runtime Security"]
        Distroless_Containers["Distroless Hardened Containers (Non-Root)"]
        Sandbox_CDR["Isolated Untrusted Document CDR Sandbox"]
    end

    subgraph Layer_4 ["Layer 4: Data Protection & KMS"]
        KMS_Enc["AWS KMS Envelope Storage Encryption"]
        KMS_Secrets["AWS Secrets Manager Vault"]
    end

    Layer_1 --> Layer_2 --> Layer_3 --> Layer_4
```

---

## 3. Infrastructure Security Standards & Prohibitions

1. **Zero Public Storage / Databases:** S3 buckets, PostgreSQL instances, and Redis clusters MUST NOT possess public IP addresses or public ACL permissions.
2. **Zero Plaintext Secrets:** Hardcoded passwords, API tokens, or KMS private keys in Git repositories, Dockerfiles, or log outputs are strictly prohibited.
3. **No Unqualified Compliance Claims:** Software architecture and infrastructure designs do not claim unverified certifications ("100% secure", "zero vulnerabilities", "ISO certified", "OWASP certified").
