# Phase 7 — Comprehensive Test Matrix

## 1. Summary of Test Coverage Matrix

The Phase 7 test matrix defines the explicit verification suite across all 25 system domain areas.

| # | Test Area | Layer | Required Test Data | Expected Result | Failure Condition | Deterministic | Standalone |
|---|---|---|---|---|---|---|---|
| **A** | Authentication | API / UI | Preseeded user identity (`ProcurementOfficer`) | Valid JWT token & dashboard navigation | 401 Unauthorized / Redirect to login | YES | YES |
| **B** | RBAC Controls | API / UI | Identity role tokens (`Bidder`, `Auditor`) | Restricted UI actions per role | Privilege escalation / Allowed forbidden route | YES | YES |
| **C** | Tender Lifecycle | API / UI | Seeded tender `TEN_01` | Tender metadata & version history visible | 404 Not Found / Schema mismatch | YES | YES |
| **D** | Bid Submission | API / UI | Seeded bid `SUB_01` | Submission status & bidder identity loaded | Empty submission list / missing fields | YES | YES |
| **E** | Document Upload | API / S3 | Mock PDF/DOCX file | File stored in MinIO with SHA-256 hash | S3 upload failure / Missing hash | YES | YES |
| **F** | Malware Validation | API | Simulated clean/infected file | File scanned & clean flag recorded | Infected file accepted | YES | YES |
| **G** | Extraction Engine | API / AI | Raw document text | Normalized structured facts extracted | Unparsed JSON / Extraction crash | YES | YES |
| **H** | OCR Fallback | API | Scanned document image | Text extracted via Tesseract/EasyOCR fallback | Empty text output | YES | YES |
| **I** | AI Gateway | API | Prompt & extraction schema | Structured Pydantic domain response | Unhandled LLM error / Direct decision | YES | YES |
| **J** | Government Adapters | API / Mock | 12 Government Source Registries | Status returned with `MOCK/DEMO` classification | Uncaught network timeout / Live claim | YES | YES |
| **K** | Evidence Engine | API | Extracted facts & source metadata | Evidence record with 9 quality dimensions | Missing evidence dimension / Invalid score | YES | YES |
| **L** | Compliance Engine | API | Requirements & Evidence | Deterministic Pass/Fail/Review matrix | Non-deterministic output / Rules bypass | YES | YES |
| **M** | Advisory Risk | API / UI | Risk signals & factor scores | Advisory risk score generated | Risk overriding deterministic rules | YES | YES |
| **N** | Human Review Queue | API / UI | Review tasks for discrepancy | Tasks routed to officer workspace | Unassigned task stuck in queue | YES | YES |
| **O** | Officer Decision | API / UI | Resolved review task | Decision recorded & audit block appended | Unauthorized decision / Missing audit | YES | YES |
| **P** | Manual Override | API / UI | Compliance rule override request | Override created with justification | Override without mandatory reason | YES | YES |
| **Q** | Four-Eyes Approval | API / UI | Threshold override request | Escalated to `SeniorReviewer` queue | Self-approval by original officer | YES | YES |
| **R** | Audit Hash Chain | API / UI | Mutating event | Cryptographic SHA-256 block chained | Broken hash chain / Tampered audit | YES | YES |
| **S** | Error Handling | API | Invalid request / Malformed JSON | RFC 7807 Problem Details JSON returned | Stack trace leak / Raw 500 HTML | YES | YES |
| **T** | Retry Mechanism | Async / API | Simulated transient error | Exponential backoff retry executed | Immediate unhandled crash | YES | YES |
| **U** | Idempotency | API | `X-Idempotency-Key` header | Duplicate operation suppressed; header returned | Duplicate entity creation | YES | YES |
| **V** | Async Workflow | Celery / Redis | Async document processing job | Job status `PENDING` -> `SUCCESS` | Stalled task / Lost worker | YES | YES |
| **W** | Job Cancellation | Async / API | Active async processing job | Job status updated to `CANCELLED` | Zombie process execution | YES | YES |
| **X** | Docker Full-Stack | Docker | `docker-compose.yml` | All services healthy & communicating | Container crash / Failed healthcheck | YES | YES |
| **Y** | Browser E2E Suite | Playwright | Seeded web application | All 12 Playwright tests pass | Navigation broken / UI element missing | YES | YES |
