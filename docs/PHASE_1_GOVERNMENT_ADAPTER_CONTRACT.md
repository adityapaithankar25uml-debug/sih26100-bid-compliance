# Phase 1 — Government Adapter Contract Specification

## Overview

The **Government Adapter Contract** defines the conceptual interface and operational lifecycle for all government integration adapters within the **SIH26100 Bid Compliance Verification Platform**.

The adapter pattern abstracts source-specific REST, SOAP, XML, or HTML details into a unified internal contract. This ensures the downstream **Deterministic Compliance Engine** receives normalized data regardless of whether the source is MeitY API Setu, an official government portal sandbox, a local synthetic mock, or an officer-submitted manual verification record.

---

## 1. Core Principles of Adapter Abstraction

1. **Provider Independence:** Downstream compliance logic must never depend on vendor-specific JSON/XML schemas or raw HTTP header structures.
2. **Encapsulation of Transport Details:** Authentication headers, API tokens, mTLS certificates, signature parameters, rate limiting logic, and payload parsing are isolated within individual adapter implementations.
3. **Strict Type Contracts:** Input parameters and returned outputs must conform to rigid structural models defined in application metadata schemas.
4. **Idempotency Guarantee:** Adapters must produce consistent normalized responses when presented with identical input parameters and source snapshots.
5. **No Direct External Tool Calling by AI:** Adapters are executed exclusively by the `GovernmentVerificationOrchestrator`. AI models cannot invoke, configure, or alter adapter execution.

---

## 2. Conceptual Interface Contract (`BaseGovernmentAdapter`)

All government verification adapters conceptually satisfy the following interface contract:

```python
# Conceptual Specification - Interface Contract (Design Only)
class BaseGovernmentAdapter(ABC):
    
    @property
    @abstractmethod
    def adapter_id(self) -> str:
        """Unique functional key for adapter registry (e.g., 'gst_verification_adapter')."""
        pass

    @property
    @abstractmethod
    def adapter_version(self) -> str:
        """SemVer identifier for the adapter implementation (e.g., '1.2.0')."""
        pass

    @property
    @abstractmethod
    def source_id(self) -> str:
        """Target government source identifier from Source Registry (e.g., 'SRC_GSTN')."""
        pass

    @abstractmethod
    def get_capabilities(self) -> AdapterCapabilities:
        """Discovers operational capabilities, supported modes, and requirements."""
        pass

    @abstractmethod
    def validate_identifier(self, identifier_type: str, identifier_value: str) -> IdentifierValidationResult:
        """Validates syntax, checksum, and structure of queried identifiers before dispatch."""
        pass

    @abstractmethod
    def execute_verification(
        self, 
        request: VerificationRequestPayload, 
        context: ExecutionContext
    ) -> NormalizedVerificationResponse:
        """Executes the verification request across target source or active operating mode."""
        pass

    @abstractmethod
    def check_health(self) -> AdapterHealthStatus:
        """Evaluates health, latency, and transport connectivity for operational monitoring."""
        pass
```

---

## 3. Data Transfer Specifications (Inputs & Outputs)

### 3.1 `AdapterCapabilities`
Defines operational metadata exposed by the adapter:
* `adapter_id`: String (e.g., `"gst_adapter"`)
* `supported_operating_modes`: List of modes (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`)
* `supported_identifier_types`: List of identifier keys (e.g., `["GSTIN", "PAN"]`)
* `requires_bidder_consent`: Boolean
* `requires_mTLS`: Boolean
* `supports_freshness_override`: Boolean
* `rate_limit_per_minute`: Integer

### 3.2 `IdentifierValidationResult`
Determines if an input string is structurally suitable for query dispatch:
* `is_valid`: Boolean
* `identifier_type`: String (e.g., `"GSTIN"`)
* `normalized_value`: String (uppercase, trimmed, regex-validated)
* `validation_error_code`: String (e.g., `"INVALID_GSTIN_CHECKSUM"`, or `None`)
* `validation_message`: String

### 3.3 `VerificationRequestPayload`
Standardized input package passed into an adapter:
* `request_id`: ULID string
* `attempt_number`: Integer (1-indexed)
* `bidder_id`: ULID string
* `tender_id`: ULID string
* `requirement_id`: ULID string
* `operating_mode`: Mode enum (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`)
* `queried_identifier_type`: Identifier key (e.g., `"UDYAM_REGISTRATION_NUMBER"`)
* `queried_identifier_value`: Sanitized identifier string
* `bidder_supplied_metadata`: Dictionary of submitted details (e.g., Legal Name, MSME Category)
* `consent_token`: Optional string for user/bidder delegated authorization

### 3.4 `NormalizedVerificationResponse`
Canonical output returned by adapters to the orchestrator:
* `verification_result_id`: ULID string
* `request_id`: ULID string
* `attempt_id`: ULID string
* `adapter_id`: String
* `adapter_version`: String
* `source_id`: String
* `operating_mode`: Mode enum (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`)
* `technical_status`: Technical status enum (e.g., `SUCCESS`, `TIMEOUT`, `HTTP_500_ERROR`)
* `business_status`: Business verification status enum (e.g., `VERIFIED`, `MISMATCH`, `RECORD_NOT_FOUND`)
* `verified_fields`: Dictionary of field comparison records:
  * Key: Field Name (e.g., `"legal_name"`)
  * Value: `FieldComparisonRecord` (`bidder_value`, `source_value`, `match_status`, `match_score`)
* `source_timestamp`: ISO 8601 timestamp string from response header/payload
* `retrieved_at`: ISO 8601 server timestamp
* `valid_from`: Optional ISO 8601 date string
* `valid_until`: Optional ISO 8601 date string
* `source_reference_number`: Official source/reference identifier (e.g., transaction reference, certificate number, portal reference, notice number)
* `raw_payload_hash`: SHA-256 hash of raw response (excluding secrets)
* `requires_human_review`: Boolean flag indicating material discrepancy or ambiguity
* `provenance_envelope`: `ProvenanceMetadata` object

---

## 4. Operational Methods & Lifecycle Contracts

### 4.1 Identifier Syntax Validation Matrix
Before dispatching external network calls, adapters validate inputs using deterministic regex patterns:

```
[Incoming Request] 
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ Pattern Validation (Regex)                             │
├────────────────────────────────────────────────────────┤
│ • GSTIN: ^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$ │
│ • PAN:   ^[A-Z]{5}[0-9]{4}[A-Z]{1}$                   │
│ • Udyam: ^UDYAM-[A-Z]{2}-[0-9]{2}-[0-9]{7}$           │
│ • CIN:   ^[LU][0-9]{5}[A-Z]{2}[0-9]{4}[PTC][0-9]{6}$  │
└────────────────────────────────────────────────────────┘
       │
       ├──────────────────────────┐
       ▼ (Valid)                  ▼ (Invalid Syntax)
[Proceed to Dispatch]     [Fast-Fail: INVALID_IDENTIFIER_SYNTAX]
```

### 4.2 Error Classification Contract
Adapters must classify all transport and protocol exceptions into normalized domain categories:

```
                  ┌──────────────────────────────────────────────┐
                  │          EXTERNAL ADAPTER EXECUTION          │
                  └──────────────────────────────────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
┌────────────────────────────────────┐       ┌────────────────────────────────────┐
│      TRANSPORT/SYSTEM ERROR        │       │       APPLICATION/DATA ERROR       │
├────────────────────────────────────┤       ├────────────────────────────────────┤
│ • TIMEOUT (DNS/Connect/Read)       │       │ • RECORD_NOT_FOUND (200 OK payload)│
│ • CONNECTION_FAILURE (TCP Reset)   │       │ • MISMATCH (Field divergence)      │
│ • HTTP_5XX_SERVER_ERROR            │       │ • EXPIRED (Certificate/Filing date)│
│ • RATE_LIMITED (HTTP 429)          │       │ • INVALID_IDENTIFIER_FORMAT        │
│ • AUTHENTICATION_FAILURE (401/403) │       │ • CANCELLED / REVOKED STATUS       │
└────────────────────────────────────┘       └────────────────────────────────────┘
                   │                                           │
                   ▼                                           ▼
      [Retryable Transport Flow]                 [Non-Retryable Domain Result]
```

---

## 5. Provenance & Metadata Extraction Requirements

Every adapter must construct an immutable `ProvenanceMetadata` record containing:

1. **Source Origin Metadata:** Source identifier, exact request URL (sanitized), HTTP method, and response status code.
2. **Cryptographic Hashes:** SHA-256 hash of the exact raw response body received from the government gateway.
3. **Execution Traceability:** Adapter class name, version string, correlation ID (`X-Correlation-ID`), and runtime latency in milliseconds.
4. **Environment Stamp:** Active operating mode (`LIVE`, `SANDBOX`, `MOCK`, `MANUAL_FALLBACK`) and host server identifier.

---

## 6. Adapter Registry & Dynamic Resolution

Adapters register with the central `GovernmentSourceRegistry` during application boot:

```python
# Conceptual Design - Adapter Registration
registry.register_adapter(
    source_id="SRC_GSTN",
    adapter_class=GSTVerificationAdapter,
    supported_modes=["LIVE", "SANDBOX", "MOCK", "MANUAL_FALLBACK"]
)
```

At runtime, the `GovernmentVerificationOrchestrator` resolves the appropriate adapter based on requested `source_id` and operational configuration. If an adapter is unequipped for a requested mode, the orchestrator routes the request to `MANUAL_FALLBACK`.
