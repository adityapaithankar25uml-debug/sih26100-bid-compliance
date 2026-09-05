# Phase 1 — Government Integration Failure & Resilience Architecture

## Executive Architectural Axiom

> [!CRITICAL]
> **TECHNICAL TRANSPORT FAILURE IS NEVER COMPLIANCE FAILURE.**
> System outages, network timeouts, HTTP 5xx errors, rate limits, and DNS failures represent **technical transport failures**. They must **NEVER** be recorded as a compliance `FAIL` or result in automated bidder `DISQUALIFICATION`.
> Technical failures transition the verification request to `REQUIRES_MANUAL_VERIFICATION`, preserving bidder rights while triggering officer workflow fallback.

---

## 1. Technical Transport Status vs. Business Verification Result

The architecture maintains a strict, un-collapsible separation between **Technical Status** (how the HTTP/network transport performed) and **Business Status** (what the government record established):

```
                        ┌────────────────────────────────────────┐
                        │      ADAPTER EXECUTION COMPLETED       │
                        └────────────────────────────────────────┘
                                             │
                  ┌──────────────────────────┴──────────────────────────┐
                  ▼                                                     ▼
┌───────────────────────────────────┐                 ┌───────────────────────────────────┐
│     TECHNICAL TRANSPORT STATUS    │                 │    BUSINESS VERIFICATION RESULT   │
├───────────────────────────────────┤                 ├───────────────────────────────────┤
│ • SUCCESS                         │                 │ • VERIFIED                        │
│ • TIMEOUT                         │                 │ • NOT_VERIFIED                    │
│ • CONNECTION_FAILURE              │                 │ • RECORD_NOT_FOUND                │
│ • DNS_FAILURE                     │                 │ • EXPIRED                         │
│ • HTTP_5XX_SERVER_ERROR           │                 │ • CANCELLED / REVOKED             │
│ • RATE_LIMITED (HTTP 429)         │                 │ • INVALID                         │
│ • AUTHENTICATION_FAILURE          │                 │ • MISMATCH                        │
│ • AUTHORIZATION_FAILURE           │                 │ • INSUFFICIENT_DATA               │
│ • CIRCUIT_OPEN                    │                 │ • NOT_APPLICABLE                  │
│ • SOURCE_UNAVAILABLE              │                 └───────────────────────────────────┘
└───────────────────────────────────┘
```

---

## 2. Resilience Patterns & Operational Policies

To ensure platform robustness during government gateway maintenance or regional network degradation, adapters incorporate five resilience patterns:

```
[Request] ──► [Idempotency Key Check] ──► [Rate Limiter] ──► [Circuit Breaker] ──► [Retry Mechanism] ──► [Government Source]
```

### 2.1 Exponential Backoff with Decorrelated Jitter
Retries for transient transport errors (e.g., HTTP 502/503/504 or network socket timeouts) use exponential backoff with full jitter to avoid thundering herd phenomena:

$$t_{\text{sleep}} = \text{Random}(0, \, \min(t_{\text{max}}, \, t_{\text{base}} \times 2^{\text{attempt}}))$$

* Default Base Delay ($t_{\text{base}}$): 1000 ms
* Default Max Delay ($t_{\text{max}}$): 16000 ms
* Maximum Retries: 3 attempts

### 2.2 Circuit Breaker Specification
Adapters maintain stateful circuit breakers to prevent cascading system load when an external portal crashes:

```
[CLOSED STATE] (Normal Ops)
      │
      │ 5 Consecutive Failures / 50% Failure Rate over 1-min Window
      ▼
[OPEN STATE] (Fast-Fail Mode: Fast-Route Requests to MANUAL_FALLBACK)
      │
      │ 60-Second Cooldown Timer Expires
      ▼
[HALF-OPEN STATE] (Probe Mode: Send 1 Test Request)
      ├───────────────────────────┐
      ▼ (Test Succeeds)           ▼ (Test Fails)
[CLOSED STATE]             [OPEN STATE] (Reset Cooldown Timer)
```

### 2.3 Rate Limiting & Concurrency Control
* **Token Bucket Rate Limiting:** Enforced per adapter (e.g., GSTN adapter capped at 60 requests/minute to match GSP quota).
* **Celery Queue Concurrency:** Dedicated worker pools prevent external portal lookups from starving core document parsing queues.

---

## 3. Comprehensive Failure Scenario Matrix

The table below defines system behavior across 17 distinct operational failure scenarios:

| # | Failure Scenario | Technical Status | Business Status | Retryable? | Fallback Action | Compliance Effect | Human Review? | Audit Event |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Upstream Portal Outage | `SOURCE_UNAVAILABLE` | `NOT_APPLICABLE` | Yes (Delayed) | Queue for retry / Officer Manual Fallback | `PENDING_VERIFICATION` | No (unless persistent) | `AUDIT_GOVT_SOURCE_UNAVAILABLE` |
| 2 | Read/Connect Timeout | `TIMEOUT` | `NOT_APPLICABLE` | Yes (Jitter) | Retry max 3x; then Manual Fallback | `PENDING_VERIFICATION` | No (until fallback) | `AUDIT_GOVT_TIMEOUT` |
| 3 | Upstream 401/403 Error | `AUTHENTICATION_FAILURE`| `NOT_APPLICABLE` | No | Alert SysAdmin; route to Manual Fallback | `REQUIRES_HUMAN_REVIEW` | Yes | `AUDIT_GOVT_AUTH_FAILED` |
| 4 | Missing Bidder Consent | `AUTHORIZATION_REQUIRED`| `NOT_APPLICABLE` | No | Notify Bidder to grant consent | `REQUIRES_BIDDER_ACTION` | No | `AUDIT_GOVT_CONSENT_REQUIRED` |
| 5 | HTTP 429 Rate Limit | `RATE_LIMITED` | `NOT_APPLICABLE` | Yes (Backoff)| Backoff algorithm; then Manual Fallback | `PENDING_VERIFICATION` | No | `AUDIT_GOVT_RATE_LIMITED` |
| 6 | Syntax Regex Invalid | `INVALID_INPUT` | `INVALID` | No | Reject dispatch; flag bidder error | `NON_COMPLIANT` | Yes | `AUDIT_GOVT_INVALID_IDENTIFIER` |
| 7 | Record Not Found (200 OK)| `SUCCESS` | `RECORD_NOT_FOUND` | No | Flag missing government registration | `REQUIRES_HUMAN_REVIEW` | Yes | `AUDIT_GOVT_RECORD_NOT_FOUND` |
| 8 | Expired Gateway Creds | `AUTHENTICATION_FAILURE`| `NOT_APPLICABLE` | No | Alert SysAdmin; route to Manual Fallback | `PENDING_VERIFICATION` | Yes | `AUDIT_GOVT_CREDS_EXPIRED` |
| 9 | Stale Cached Record | `SUCCESS` | `VERIFIED` | No | Evict cache; trigger live refresh | `PENDING_VERIFICATION` | No | `AUDIT_GOVT_CACHE_EVICTED` |
| 10 | Malformed JSON Payload | `PARSE_ERROR` | `NOT_APPLICABLE` | No | Quarantine payload; Manual Fallback | `PENDING_VERIFICATION` | Yes | `AUDIT_GOVT_MALFORMED_RESPONSE` |
| 11 | Schema Structure Changed | `SCHEMA_ERROR` | `NOT_APPLICABLE` | No | Quarantine payload; alert dev team | `PENDING_VERIFICATION` | Yes | `AUDIT_GOVT_SCHEMA_MISMATCH` |
| 12 | Conflicting Source Data | `SUCCESS` | `MISMATCH` | No | Preserve both; flag material conflict | `REQUIRES_HUMAN_REVIEW` | Yes | `AUDIT_GOVT_CONFLICT_DETECTED` |
| 13 | Duplicate Request | `DUPLICATE_IGNORED` | `VERIFIED` | No | Return existing request result | Neutral | No | `AUDIT_GOVT_DUPLICATE_IGNORED` |
| 14 | Adapter Unimplemented | `ADAPTER_DISABLED` | `NOT_APPLICABLE` | No | Route request to Manual Fallback | `PENDING_VERIFICATION` | Yes | `AUDIT_GOVT_ADAPTER_DISABLED` |
| 15 | Sandbox Mode Request | `SUCCESS` | `VERIFIED` | No | Return synthetic response (Tagged Sandbox)| `SANDBOX_VERIFIED` | No | `AUDIT_GOVT_SANDBOX_EXECUTED` |
| 16 | Evidence DB Write Error | `STORAGE_FAILURE` | `NOT_APPLICABLE` | Yes (DB Retry)| Retry DB transaction; log emergency alert | `SYSTEM_ERROR` | Yes | `AUDIT_GOVT_STORAGE_FAILED` |
| 17 | Audit Logging Failure | `AUDIT_FAILURE` | `NOT_APPLICABLE` | No | Halt transaction execution (Safety Stop) | `SYSTEM_ERROR` | Yes | `AUDIT_EMERGENCY_HALT` |
