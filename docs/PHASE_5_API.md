# Phase 5 — API Reference Specification

## 1. Overview
Base Path: `/api/v1`

## 2. Endpoints Catalog

### Evidence Ledger & Traceability
- `GET /evidence/{id}` — Fetch specific evidence record.
- `GET /evidence/{id}/trace` — Fetch evidence lineage graph for evidence record.
- `GET /bids/{submission_id}/evidence` — List all evidence records for submission.
- `GET /bids/{submission_id}/evidence-trace` — Fetch full evidence lineage graph for submission.

### Compliance Explanation ("Why?" View)
- `GET /bids/{submission_id}/explanation` — Fetch deterministic "Why PASS / FAIL / MISSING / REVIEW" explainability panel.

### Evaluation Snapshots
- `GET /bids/{submission_id}/evaluation-snapshots` — List historical evaluation snapshots for submission.
- `GET /evaluation-snapshots/{id}` — Fetch specific evaluation snapshot detail.

### Advisory Risk Engine
- `GET /bids/{submission_id}/risk-assessment` — Fetch advisory risk profile & factor signals.
- `POST /bids/{submission_id}/assess-risk` — Trigger advisory risk assessment recalculation.

### Human Review Workspace
- `GET /human-reviews` — Query review queue with `status_filter` and `priority_filter`.
- `GET /human-reviews/{id}` — Fetch specific human review task detail.
- `POST /human-reviews/{id}/assign` — Assign review task to procurement officer.
- `POST /human-reviews/{id}/resolve` — Resolve review task with officer decision & comments.

### Officer Decisions & Manual Overrides
- `GET /bids/{submission_id}/officer-decisions` — Fetch historical officer decisions for submission.
- `POST /bids/{submission_id}/officer-decisions` — Record formal qualification decision (`QUALIFIED`, `DISQUALIFIED`, `REQUIRES_CLARIFICATION`, `EVIDENCE_REQUESTED`).
- `GET /bids/{submission_id}/manual-overrides` — List manual overrides recorded for submission.
- `GET /manual-overrides/{id}` — Fetch manual override detail by ID.
- `POST /bids/{submission_id}/manual-overrides` — Record non-destructive manual override on requirement.
- `POST /manual-overrides/{override_id}/approve` — Process four-eyes approval/rejection by Senior Reviewer.
