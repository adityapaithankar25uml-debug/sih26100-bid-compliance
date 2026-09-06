# Phase 5 — System Data Flow Architecture

## 1. End-to-End Data Flow Sequence
1. **Document & Fact Ingestion (Phase 3/4)**: Submission documents uploaded, OCR/text parsed, and normalized compliance facts generated via government adapters.
2. **Deterministic Compliance Rule Evaluation (Phase 4)**: Rules evaluated against AST expressions and versioned policy configuration.
3. **Evidence Ledger Registration (Phase 5)**: `EvidenceRecord` items generated with explicit 7-dimensional evidence quality metrics.
4. **Advisory Risk Assessment (Phase 5)**: Non-linear risk engine evaluates 12 categories and outputs advisory risk profile & factor signals.
5. **Human Review Queue Routing (Phase 5)**: `MISSING_EVIDENCE`, `REVIEW_REQUIRED`, or high-risk signals automatically create `HumanReviewTask` in officer queue.
6. **Officer Workspace Inspection (Phase 5)**: Officer reviews evidence lineage graph, "Why?" explainability panel, and risk factor signals.
7. **Officer Decision & Non-Destructive Override (Phase 5)**: Officer records formal decision (`QUALIFIED`/`DISQUALIFIED`) and overrides individual rule statuses if justified.
8. **Evaluation Snapshot & Audit Chain Logging (Phase 5)**: Immutable evaluation snapshot stored with SHA-256 hash, and domain event appended to Tamper-Evident SHA-256 Audit Hash Chain.
