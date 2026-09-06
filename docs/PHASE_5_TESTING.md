# Phase 5 — Testing & Quality Assurance Plan

## 1. Test Architecture
Phase 5 testing covers evidence ledger creation, evidence quality assessment, traceability graph, "Why?" explainability, advisory risk engine, human review workspace, officer decisions, non-destructive manual overrides, four-eyes approval, evaluation snapshots, audit hash-chain integrity, RBAC security, and end-to-end smoke verification.

## 2. Test Execution Commands
- **Backend Full Test Suite**: `cd backend && python -m pytest tests -v`
- **Phase 5 Specific Tests**: `cd backend && python -m pytest tests/test_phase5_evidence_risk_human_review.py -v`
- **Phase 5 End-to-End Smoke Test**: `cd backend && python scripts/smoke_test_phase5.py`
- **Frontend Build**: `cd frontend && npm run build`
- **Docker Compose Configuration**: `docker compose config`
