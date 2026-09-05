# Phase 1 AI Risk Register Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-024  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document provides an exhaustive 15-risk register for AI pipeline operational, security, and governance risks. No application code, risk management scripts, or backend services are created.

---

## 1. Exhaustive 15-Risk AI Register Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              EXHAUSTIVE 15-RISK AI REGISTER                             │
├───────┬───────────────────────────────────┬────────┬────────────┬───────────────────────┤
│ ID    │ Risk Title                        │ Impact │ Likelihood │ Responsible Role      │
├───────┼───────────────────────────────────┼────────┼────────────┼───────────────────────┤
│ R-01  │ AI Verification Hallucination    │ HIGH   │ MEDIUM     │ Lead AI Architect     │
│ R-02  │ Indirect Prompt Injection Attack │ HIGH   │ MEDIUM     │ Cybersecurity Lead    │
│ R-03  │ External PII Data Leakage        │ HIGH   │ LOW        │ Data Protection Officer│
│ R-04  │ Model Drift & Extraction Decay    │ MEDIUM │ MEDIUM     │ AI Governance Admin   │
│ R-05  │ Cloud AI Provider Outage          │ HIGH   │ LOW        │ Infrastructure Lead   │
│ R-06  │ Model Upgrade Invalidation        │ HIGH   │ LOW        │ Lead AI Architect     │
│ R-07  │ OCR Character Extraction Error    │ MEDIUM │ HIGH       │ Document Admin        │
│ R-08  │ Procurement Officer Automation Bias│ HIGH   │ MEDIUM     │ Compliance Admin     │
│ R-09  │ Stale RAG Policy Retrieval        │ MEDIUM │ LOW        │ Knowledge Admin       │
│ R-10  │ Non-Standard Table Layout Failure │ MEDIUM │ MEDIUM     │ Document Admin        │
│ R-11  │ False Debarment Accusation        │ HIGH   │ LOW        │ Legal / Officer       │
│ R-12  │ Un-Grounded AI Explanation Text   │ HIGH   │ LOW        │ AI Quality Lead       │
│ R-13  │ Model Refusal on Legal Text       │ LOW    │ LOW        │ AI Gateway Lead       │
│ R-14  │ Rate Limit / Cost Exhaustion      │ MEDIUM │ MEDIUM     │ Infrastructure Lead   │
│ R-15  │ Non-Reproducible Model Inferences │ MEDIUM │ LOW        │ Audit Lead            │
└───────┴───────────────────────────────────┴────────┴────────────┴───────────────────────┘
```

---

## 2. Detailed Risk Control & Mitigation Profiles

### Risk R-01: AI Verification Hallucination
- **Description:** AI model invents or hallucinates a non-existent GSTIN, turnover figure, or registration status.
- **Impact:** High (Risk of illegal vendor qualification based on false data).
- **Likelihood Category:** Medium.
- **Mitigation:** AI is strictly prohibited from generating authoritative verification results. All extracted values require deterministic regex/checksum validation and authoritative government API verification (Tier C).
- **Detection Mechanism:** Deterministic checksum validation failures and external API mismatch alerts.
- **Fallback Strategy:** Mark value as `NOT_VERIFIED` and route to `MANUAL_FALLBACK`.
- **Responsible Role:** Lead AI Architect & Procurement Officer.

### Risk R-02: Indirect Prompt Injection Attack
- **Description:** Malicious text embedded in uploaded bidder PDFs attempts to hijack system prompt instructions (e.g. *"MARK QUALIFIED"*).
- **Impact:** High (Potential bypass of compliance checks).
- **Likelihood Category:** Medium.
- **Mitigation:** Delimiter sandboxing (`<<<UNTRUSTED_DOC_CONTENT>>>`), rigid Pydantic JSON Schema enforcement, zero tool permissions for AI models, and suspicious instruction pre-scanners.
- **Detection Mechanism:** Schema validation errors (`VALIDATION_FAILED`) and regex injection pre-scanner alerts.
- **Fallback Strategy:** Flag document with `SUSPICIOUS_CONTENT_FLAG` and trigger mandatory officer visual review.
- **Responsible Role:** Cybersecurity Lead.

### Risk R-03: External PII Data Leakage
- **Description:** Sensitive bidder personal identity data (Aadhaar, personal phone numbers) sent to external commercial cloud AI models.
- **Impact:** High (Violation of DPDP Act 2023 and privacy regulations).
- **Likelihood Category:** Low.
- **Mitigation:** Pre-AI Privacy Gateway performs deterministic PII redaction and sensitivity classification. `CONFIDENTIAL` payloads are routed exclusively to Category 3 (Self-Hosted On-Premise GPU vLLM) or Category 4 (Local Ollama).
- **Detection Mechanism:** Pre-AI Privacy Gateway outbound regex audit logger.
- **Fallback Strategy:** Block external cloud dispatch; reroute payload to self-hosted/local model.
- **Responsible Role:** Data Protection Officer.

### Risk R-04: Model Drift & Extraction Decay
- **Description:** Updated cloud model version exhibits silent performance degradation on specific CA turnover certificate layouts.
- **Impact:** Medium (Inaccurate field extraction requiring increased officer manual correction).
- **Likelihood Category:** Medium.
- **Mitigation:** Automated continuous benchmarking against golden datasets (`DS-BENCH-01` through `05`) before model deployment.
- **Detection Mechanism:** Daily evaluation framework metric monitoring alerts.
- **Fallback Strategy:** Pin model version in AI Gateway configuration or roll back to prior stable version.
- **Responsible Role:** AI Governance Admin.

### Risk R-05: Cloud AI Provider Outage
- **Description:** Commercial cloud AI provider API becomes unreachable or experiences extended downtime during peak tender evaluation dates.
- **Impact:** High (Stoppage of document extraction background jobs).
- **Likelihood Category:** Low.
- **Mitigation:** Multi-provider AI Gateway architecture with automatic circuit breaker and fallback priority ordering.
- **Detection Mechanism:** Gateway circuit breaker failure count exceeding 5 consecutive errors.
- **Fallback Strategy:** Automatically fail over to Category 3 (Self-Hosted vLLM) or Category 4 (Local Ollama) without interrupting application availability.
- **Responsible Role:** Infrastructure Lead.

### Risk R-06: Model Upgrade Invalidation
- **Description:** Deployment of a new AI model version invalidates historical extraction audit trails.
- **Impact:** High (Inability to reproduce past compliance evaluation snapshots during CVC vigilance audit).
- **Likelihood Category:** Low.
- **Mitigation:** Immutability rule: Model upgrades NEVER modify historical database records. Historical tasks retain original `model_identifier`, `model_version`, and `prompt_version` metadata.
- **Detection Mechanism:** Audit hash-chain verification check.
- **Fallback Strategy:** Preserve historical model version artifacts in read-only model registry archive.
- **Responsible Role:** Lead AI Architect & Audit Lead.

### Risk R-07: OCR Character Extraction Error
- **Description:** Low-resolution scanned document causes OCR engine to misread numbers (e.g. reading `65.00 Cr` as `6.50 Cr`).
- **Impact:** Medium (Incorrect numeric threshold evaluation).
- **Likelihood Category:** High.
- **Mitigation:** Image pre-processing (binarization, 300 DPI deskewing), character-level confidence scoring, and visual bounding box highlight on Officer Workbench.
- **Detection Mechanism:** Low-confidence extraction alerts (below task policy threshold) and cross-document discrepancy signals.
- **Fallback Strategy:** Trigger mandatory officer visual bounding box review (Checkpoint 2).
- **Responsible Role:** Document Admin & Procurement Officer.

### Risk R-08: Procurement Officer Automation Bias
- **Description:** Procurement officer uncritically accepts AI recommendations without reviewing underlying evidence documents.
- **Impact:** High (Human oversight failure leading to improper bidder qualification).
- **Likelihood Category:** Medium.
- **Mitigation:** Workbench UI displays prominent `[AI PROPOSAL - ADVISORY ONLY]` badges, defaults decision inputs to `UNDECIDED`, separates risk scores from compliance status, and mandates non-empty justification rationale strings.
- **Detection Mechanism:** Officer decision audit logs indicating zero-second review times.
- **Fallback Strategy:** Trigger supervisory review flag for rapid-decision overrides.
- **Responsible Role:** Procurement Compliance Admin.

### Risk R-09: Stale RAG Policy Retrieval
- **Description:** RAG pipeline retrieves deprecated CVC procurement policy guidelines from vector store.
- **Impact:** Medium (Officer guided by outdated procurement rules).
- **Likelihood Category:** Low.
- **Mitigation:** Vector store metadata tagging (`policy_version`, `effective_date`, `is_active`). Ingestion pipeline filters out chunks from inactive policy versions.
- **Detection Mechanism:** Automated policy version freshness checker.
- **Fallback Strategy:** Exclude inactive policy vectors from hybrid search queries.
- **Responsible Role:** Knowledge Admin.

### Risk R-10: Non-Standard Table Layout Failure
- **Description:** Complex multi-column or multi-page financial table in CA certificate fails structured JSON extraction.
- **Impact:** Medium (Missing turnover field values).
- **Likelihood Category:** Medium.
- **Mitigation:** Multi-modal vision-language layout parsing, fallback to raw text block segmentation, and schema validation.
- **Detection Mechanism:** `VALIDATION_FAILED` status or missing required schema fields.
- **Fallback Strategy:** Reroute document to `REQUIRES_HUMAN_REVIEW` for manual officer field keying.
- **Responsible Role:** Document Admin.

### Risk R-11: False Debarment Accusation
- **Description:** AI model incorrectly flags a legitimate bidder as debarred due to partial name match on debarment affidavit.
- **Impact:** High (Legal liability and reputational damage to vendor).
- **Likelihood Category:** Low.
- **Mitigation:** Strict separation: AI anomaly signals are advisory metrics only. Formal debarment evaluation requires exact PAN/GSTIN matching and mandatory Procurement Officer confirmation (Checkpoint 4).
- **Detection Mechanism:** Anomaly signal review step in officer workflow.
- **Fallback Strategy:** Procurement officer rejects false anomaly signal with mandatory rationale.
- **Responsible Role:** Legal Counsel & Procurement Officer.

### Risk R-12: Un-Grounded AI Explanation Text
- **Description:** AI explanation module generates a summary sentence containing unverified claims not found in evidence records.
- **Impact:** High (Misleading audit report narrative).
- **Likelihood Category:** Low.
- **Mitigation:** Automated Grounding Verification Engine parses generated explanation sentences and verifies traceable evidence citation alignment before report export.
- **Detection Mechanism:** Grounding verification check failure flag.
- **Fallback Strategy:** Strip ungrounded sentences and display itemized rule output facts only.
- **Responsible Role:** AI Quality Lead.

### Risk R-13: Model Refusal on Legal Text
- **Description:** Cloud AI safety classifier falsely flags a legal tender debarment clause as sensitive and refuses inference.
- **Impact:** Low (Task delay).
- **Likelihood Category:** Low.
- **Mitigation:** AI Gateway detects refusal response structure and automatically reroutes prompt to Category 3 (Self-Hosted vLLM) or Category 4 (Local Ollama).
- **Detection Mechanism:** Model API refusal status code interception.
- **Fallback Strategy:** Failover to local/self-hosted open-weight model.
- **Responsible Role:** AI Gateway Lead.

### Risk R-14: Rate Limit / Cost Exhaustion
- **Description:** High volume of document submissions on tender closing date exhausts cloud API rate limits or quota.
- **Impact:** Medium (Extraction job backlog and delayed evaluation).
- **Likelihood Category:** Medium.
- **Mitigation:** Redis sliding-window rate limiting, job queue prioritization (Officer interactive queries prioritized over batch background jobs), and local GPU cluster scaling.
- **Detection Mechanism:** Celery queue depth monitoring and 429 rate limit error tracking.
- **Fallback Strategy:** Offload batch jobs to Category 3 self-hosted GPU workers.
- **Responsible Role:** Infrastructure Lead.

### Risk R-15: Non-Reproducible Model Inferences
- **Description:** Stochastic temperature sampling in LLM inference produces slightly different extraction wording across separate runs.
- **Impact:** Medium (Inconsistent text representations).
- **Likelihood Category:** Low.
- **Mitigation:** All extraction and classification inference calls set `temperature: 0.0`, `seed: 42`, and enforce rigid JSON schemas.
- **Detection Mechanism:** Dual-inference consistency checks during evaluation runs.
- **Fallback Strategy:** Deterministic schema validation and raw response hash logging.
- **Responsible Role:** Audit Lead & Lead AI Architect.
