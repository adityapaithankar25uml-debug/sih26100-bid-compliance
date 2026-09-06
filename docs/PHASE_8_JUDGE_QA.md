# Phase 8 — Comprehensive Judge Q&A & Defense Compendium

This document provides exact, authoritative answers to 30 technical, operational, and legal questions likely to be asked by SIH judges.

---

## 30 Judge Q&A Entries

### Q1: Why don't you train your own custom LLM from scratch?
**Answer:** Training a custom LLM from scratch is inefficient for document extraction. Base LLMs already possess strong natural language processing capabilities. We utilize lightweight provider abstraction to route prompts to enterprise models or local open-source LLMs while enforcing schema validation and deterministic rule evaluation.

### Q2: Why not just use OpenAI/Gemini directly in the application frontend?
**Answer:** Directly calling public LLM APIs from a web frontend exposes API keys, bypasses PII redaction, and violates data security boundaries. Our architecture routes document processing through a secure backend AI Gateway with pattern-based PII scrubbing and structured schema validation.

### Q3: Are your government registry integrations live?
**Answer:** For this SIH prototype, government registry responses are simulated through normalized integration adapters. The architecture is designed for authorized production connections, but no live government credentials or live government verification access are being claimed in this prototype.

### Q4: What happens if a government registry portal is temporarily offline during bid evaluation?
**Answer:** Transport failure safety is built into our adapter architecture. API timeouts or server errors return a `TECHNICAL_FAILURE` status and generate a task in the Human Review Queue. A technical portal outage **never** results in automatic bidder rejection.

### Q5: How are hallucinations prevented during compliance checking?
**Answer:** AI extraction is advisory. Deterministic compliance rules evaluate structured facts. Evidence and provenance support the evaluation. The authorized human officer retains final procurement decision authority. The AI model extracts facts into rigid JSON schemas, and rule evaluation is performed by compiled Python code using boolean logic.

### Q6: Can an AI model incorrectly disqualify a bidder?
**Answer:** No. Under our architecture, AI outputs are purely advisory structured facts. Only deterministic rules or authorized human officers can qualify or disqualify a bidder.

### Q7: What prevents an unauthorized modification of audit records in the database?
**Answer:** Our audit system uses a **Tamper-Evident SHA-256 Audit Hash Chain**. Every event payload is hashed sequentially with the previous event's hash (`prev_hash`). If a database row is modified, re-running chain integrity verification immediately flags the broken block link and triggers a tamper warning.

### Q8: Is your audit hash chain a legal PKI digital signature?
**Answer:** No. The audit mechanism verifies hash-chain integrity but does not itself constitute a PKI digital signature or legal non-repudiation mechanism.

### Q9: Is this prototype ready for live production deployment today?
**Answer:** No, and we are completely transparent about this. The prototype has a complete architecture, verified test coverage, and a fully functional UI. Production deployment requires authorized onboarding, identity integration, infrastructure deployment, and independent security certification.

### Q10: Why should procurement departments consider your platform over simple document comparison software?
**Answer:** Simple document comparison software only performs keyword matching. SIH26100 provides a unified Bidder 360 identity model, 12 statutory government verification adapters, a 9-dimension evidence model, advisory risk scoring, four-eyes policy safeguards, and a tamper-evident audit hash chain.

### Q11: How does your system handle corrigendums or specification changes issued after tender publication?
**Answer:** The platform supports tender specification versioning (`TenderVersion`). When a corrigendum is published, a new specification version baseline is created. Bids are evaluated against the exact specification version active at submission time.

### Q12: How does the Four-Eyes Policy work?
**Answer:** When a Procurement Officer manually overrides a rule result, the system checks four-eyes threshold rules. High-impact overrides are marked as `PENDING_FOUR_EYES`, requiring a second senior officer (`SeniorReviewer`) to review and approve the action.

### Q13: What happens if a bidder submits a Make in India (MII) self-declaration with low local content?
**Answer:** The deterministic compliance engine checks the declared local content percentage against the minimum threshold. If the value is below threshold, it generates a deterministic `FAIL` or routes the item to Human Review for verification.

### Q14: How does your system handle PII (Personally Identifiable Information)?
**Answer:** The prototype includes deterministic detection and redaction patterns for configured sensitive data categories (such as Aadhaar numbers, personal phone numbers, and private bank accounts) before external AI processing.

### Q15: What is the role of the Advisory Risk Engine?
**Answer:** The Risk Engine aggregates anomaly signals into a risk score. It helps officers prioritize which bids to review first in high-volume tenders.

### Q16: Can the Advisory Risk Engine automatically reject a bid?
**Answer:** No. Risk scores are strictly advisory for prioritization and queue routing. Under our architectural rules, risk scores cannot automatically qualify or disqualify a bidder.

### Q17: What technology stack is used in the platform?
**Answer:** Next.js 14 (React 18, TypeScript, Tailwind) on the frontend; FastAPI (Python 3.10+, Pydantic v2) on the backend; PostgreSQL 16 for database storage; Redis 7 for caching; Celery for async task queues; and MinIO for document object storage.

### Q18: How do you handle multi-page PDF documents?
**Answer:** PyMuPDF extracts page text and tabular structures. Extracted snippets maintain page number citations so officers can jump directly to the relevant page to verify a financial table.

### Q19: What happens if two government registries provide conflicting identity information?
**Answer:** The system creates an `IDENTITY_MISMATCH` signal in the Advisory Risk Engine, elevates the bid's risk score, and generates a task in the Human Review Queue for manual officer clarification.

### Q20: Can an officer modify an evaluation result without leaving a trace?
**Answer:** No. Manual overrides are non-destructive. The system captures a point-in-time `EvaluationSnapshot` with a SHA-256 hash before saving the override in a separate `ManualOverride` table, logging canonical audit events for both.

### Q21: What role does MinIO play in document security?
**Answer:** MinIO provides S3-compatible object storage. Uploaded PDFs are stored in an isolated bucket (`sih26100-documents`) with ULID storage references to prevent direct path traversal or unauthorized URL guessing.

### Q22: How does the system validate file uploads?
**Answer:** Upload validation checks file extensions and magic-bytes (`%PDF-`, PNG/JPG headers). Uploaded files are placed in `QUARANTINED` status and scanned before processing.

### Q23: Why do government registry cards show "MOCK MODE"?
**Answer:** For this SIH prototype, government registry responses are simulated through normalized integration adapters. The architecture is designed for authorized production connections, but no live government credentials or live government verification access are being claimed in this prototype.

### Q24: How does your platform support the "Make in India" initiative?
**Answer:** The system specifically extracts MII local content declarations, verifies local content percentages against tender thresholds, and validates OEM authorization codes.

### Q25: Can the platform run on private cloud infrastructure?
**Answer:** Yes. The entire stack—FastAPI, Next.js, PostgreSQL, Redis, MinIO, and enterprise LLM engines—can be deployed on an authorized government-approved cloud environment.

### Q26: How does the platform assist in audit defense?
**Answer:** By providing deterministic rule evaluations, four-eyes policy controls, and a tamper-evident audit hash chain, every evaluation step is recorded with evidence citations.

### Q27: How long does it take to run your automated test suite?
**Answer:** Our backend Pytest suite (56 passed, 0 failed) executes in ~19 seconds. Our Playwright E2E integration test suite (12 passed, 0 failed) executes in ~47 seconds.

### Q28: How does your frontend enforce role security?
**Answer:** Frontend navigation is contextually derived from JWT token claims issued by the backend. Privilege escalation is prevented because backend API endpoints authoritatively enforce role dependencies (`require_roles`).

### Q29: What is the main innovation of your Evidence Engine?
**Answer:** Evaluating evidence across **9 independent quality dimensions**—including source authority, freshness, hash validity, and identity linkage—rather than treating all document text as equally reliable.

### Q30: What is your closing message to the judging panel?
**Answer:** SIH26100 provides an evidence-first, deterministic, human-authoritative architecture that modernizes public procurement for CPCL and GeM while upholding complete legal accountability and audit integrity.
