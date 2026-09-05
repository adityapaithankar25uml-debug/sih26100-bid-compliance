# Phase 1 AI Provider Abstraction Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-018  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines the vendor-agnostic AI Gateway abstraction layer, 4 provider categories, routing strategies, and standardized request/response schema specifications. No FastAPI routers, Python AI gateway classes, model SDK installations, or backend source files are created.

---

## 1. Vendor-Agnostic AI Gateway Architecture

The platform backend communicates with AI providers exclusively through a vendor-agnostic internal interface (`AIGatewayInterface`). Business logic modules (Document Intelligence, Tender Understanding, Explanation Engine) MUST NOT import or call specific vendor SDKs directly.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              BUSINESS LOGIC MODULES                                     │
│     [Document Processing]   [Tender Understanding]   [Explanation Engine]               │
└───────────────────────────────────────────┬─────────────────────────────────────────────┘
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           INTERNAL VENDOR-AGNOSTIC AI GATEWAY                           │
│                          (Capability Router & Policy Enforcer)                          │
└───────┬──────────────────────────┬──────────────────────────┬───────────────────────────┘
        │                          │                          │                           │
        ▼                          ▼                          ▼                           ▼
┌──────────────┐           ┌──────────────┐           ┌──────────────┐           ┌──────────────┐
│  CATEGORY 1  │           │  CATEGORY 2  │           │  CATEGORY 3  │           │  CATEGORY 4  │
│ Commercial   │           │ Enterprise   │           │ Self-Hosted  │           │ Local Ollama │
│ Cloud Model  │           │ Cloud Model  │           │ Open-Weight  │           │ Instance     │
└──────────────┘           └──────────────┘           └──────────────┘           └──────────────┘
```

---

## 2. Four Provider Taxonomy Categories

| Category | Infrastructure Type | Target Deployment | Data Sensitivity Eligibility | Example Providers / Models |
| :--- | :--- | :--- | :--- | :--- |
| **Category 1** | Commercial Cloud LLM | Cloud Staging / Production | PUBLIC / RESTRICTED (Non-PII) | Gemini 1.5 Pro, Claude 3.5 Sonnet |
| **Category 2** | Enterprise Cloud Model | Govt Private Cloud / NIC | RESTRICTED / CONFIDENTIAL | Azure OpenAI Enterprise, Vertex AI |
| **Category 3** | Self-Hosted Open-Weight | On-Premise GPU Cluster | CONFIDENTIAL / HIGHLY_SENSITIVE | Qwen 2.5 72B / Llama 3.3 70B (vLLM) |
| **Category 4** | Local Ollama Instance | Local Workstation / Demo | OFFLINE / AIR-GAPPED / DEMO | Ollama Qwen 2.5 3B / Llama 3.2 3B |

> **Government Data Policy Rule:** No single AI provider is assumed to be automatically approved for production government procurement data. Data routing MUST strictly respect the data sensitivity classification established by the Pre-AI Privacy Gateway.

---

## 3. Standardized Provider Metadata Parameters

Every AI model registered in the AI Gateway configuration must define the following metadata parameters:

```json
{
  "provider_id": "SELF_HOSTED_VLLM_01",
  "provider_category": "CATEGORY_3_SELF_HOSTED",
  "model_identifier": "qwen2.5-72b-instruct",
  "model_version": "2024-09-v1.2",
  "deployment_location": "CPCL_ON_PREM_DATACENTER_CHENNAI",
  "data_handling_classification": "HIGHLY_SENSITIVE_APPROVED",
  "capabilities": {
    "structured_json_output": true,
    "vision_layout_understanding": true,
    "max_context_window": 131072,
    "supports_function_calling": false,
    "supports_embeddings": false
  },
  "performance_metrics": {
    "average_latency_ms": 850,
    "max_concurrent_requests": 32,
    "cost_per_1k_input_tokens_usd": 0.00,
    "cost_per_1k_output_tokens_usd": 0.00
  },
  "governance": {
    "is_active": true,
    "fallback_priority_order": 1,
    "circuit_breaker_error_threshold": 5
  }
}
```

---

## 4. Model Routing Strategy

The AI Gateway routes incoming task requests based on a deterministic priority matrix:

```
[Task Request] ──> (1. Capability Match) ──> (2. Data Sensitivity Check) ──> (3. Availability & Circuit Breaker) ──> [Dispatch Model]
```

### 4.1 Capability Matching
- **Complex Tender Requirement Extraction & Clause Mapping:** Requires models with context window $\ge 32\text{K}$ tokens and high reasoning capability (`qwen2.5-72b`, `claude-3-5-sonnet`, `gemini-1.5-pro`).
- **Document Classification & Structured Extraction:** Requires models supporting strict JSON schema enforcement (`qwen2.5-14b`, `gpt-4o-mini`, `ollama-qwen2.5-3b`).
- **Policy Search & Vector Embeddings:** Dedicated embedding models (`bge-large-en-v1.5`, `text-embedding-3-large`).

### 4.2 Sensitivity-Based Routing
- **`PUBLIC` / `COMMERCIAL_TERMS`:** Routed to Category 1, 2, 3, or 4 based on latency/cost.
- **`RESTRICTED` / `BIDDER_FINANCIALS`:** Routed to Category 2 (Enterprise Cloud) or Category 3 (Self-Hosted).
- **`CONFIDENTIAL` / `PII_CONTAINING` / `OFFICER_REMARKS`:** Routed EXCLUSIVELY to Category 3 (Self-Hosted On-Premise) or Category 4 (Local Ollama).

### 4.3 Fallback Chain Priority & Safety Gate

Before any candidate model receives a fallback workload, the AI Gateway executes an **Explicit Fallback Eligibility Gate** verifying:
1. Task capability match (e.g. structured JSON schema support, context window size).
2. Data sensitivity eligibility (e.g. `CONFIDENTIAL` data CANNOT fallback to Category 1 Cloud models).
3. Approved provider and model status in platform model registry.
4. Deployment / data-handling security classification.
5. Model version and organizational policy eligibility.

Only approved, policy-compliant models may receive the fallback workload. The system MUST NEVER silently route sensitive data to an unapproved external provider. All fallback decisions are logged to audit events.

```
[Primary Outage] ──> (Fallback Eligibility Gate) ──> [If Approved] ──> Dispatch Secondary Model
                                                ──> [If Denied]   ──> Trip Circuit Breaker / Manual Review
```

1. **Primary Model Outage / Timeout:** Fall back to secondary approved provider passing the Fallback Eligibility Gate.
2. **External Cloud Network Failure:** Fall back to Category 3 (Self-Hosted vLLM) or Category 4 (Local Ollama) if data sensitivity allows.
3. **Complete AI Provider Failure:** Trip circuit breaker to `OPEN` state and route request to Tier A/D deterministic/manual processing.

> **Quality & Security Protection Rule:** Cost or latency MUST NOT be the sole reason to select a weaker model for high-risk compliance interpretation tasks. Sensitive payloads MUST NOT bypass data localization rules during fallback.

---

## 5. Standardized Gateway API Contract Schemas

### 5.1 Abstract AI Request Schema (`AIGatewayRequest`)

```json
{
  "task_type": "STRUCTURED_FIELD_EXTRACTION",
  "task_id": "01HZX89J4K2P00000000000800",
  "required_capability": "STRUCTURED_JSON_OUTPUT",
  "data_sensitivity_level": "RESTRICTED",
  "system_prompt_version": "SP-EXTRACTION-FINANCIAL-v1.2",
  "user_prompt_template_version": "UP-TURNOVER-v2.0",
  "prompt_variables": {
    "document_type": "CA_TURNOVER_CERTIFICATE",
    "target_fields": ["annual_turnover_fy24", "annual_turnover_fy23", "net_worth"]
  },
  "input_document_reference": {
    "document_id": "01HZX89J4K2P00000000000150",
    "page_number": 3,
    "sanitized_text_chunk": "This is to certify that M/s ABC CPCL SUPPLIERS PRIVATE LIMITED turnover for FY 2023-24 is Rs 65.00 Crores..."
  },
  "json_schema_target": {
    "type": "object",
    "properties": {
      "annual_turnover_fy24": {"type": "number"},
      "annual_turnover_fy23": {"type": "number"},
      "net_worth": {"type": "number"}
    },
    "required": ["annual_turnover_fy24"]
  }
}
```

### 5.2 Abstract AI Response Schema (`AIGatewayResponse`)

```json
{
  "task_id": "01HZX89J4K2P00000000000800",
  "status": "SUCCEEDED",
  "provider_metadata": {
    "provider_id": "SELF_HOSTED_VLLM_01",
    "model_identifier": "qwen2.5-72b-instruct",
    "model_version": "2024-09-v1.2",
    "execution_time_ms": 640
  },
  "governance_metadata": {
    "system_prompt_version": "SP-EXTRACTION-FINANCIAL-v1.2",
    "schema_validation_passed": true,
    "pii_sanitization_applied": true,
    "confidence_score": 0.94
  },
  "structured_output": {
    "annual_turnover_fy24": 650000000.0,
    "annual_turnover_fy23": 580000000.0,
    "net_worth": 120000000.0
  },
  "raw_response_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "timestamp": "2026-09-05T23:48:00.000Z"
}
```
