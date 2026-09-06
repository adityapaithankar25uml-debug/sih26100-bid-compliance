# Phase 7 — End-to-End Test Strategy & Quality Assurance Plan

## 1. Objectives & Scope

The Phase 7 testing strategy validates the end-to-end integration of the SIH26100 platform. It ensures:
- Full API consistency between frontend Next.js pages and FastAPI endpoints.
- End-to-end execution of the 16-step flagship procurement compliance scenario.
- Deterministic behavior of AI extraction, government mock adapters, evidence creation, compliance rules, advisory risk, human review, four-eyes policy, and audit hash chain.
- Independence of `X-Correlation-ID` (request correlation) and `X-Idempotency-Key` (duplicate request prevention).

---

## 2. Test Execution Layers

```
                               ┌───────────────────────────┐
                               │  Playwright CLI E2E Tests  │ (Browser E2E, 12 scenarios)
                               └─────────────┬─────────────┘
                                             │
                               ┌─────────────▼─────────────┐
                               │  Playwright MCP Sanity    │ (Interactive UI validation)
                               └─────────────┬─────────────┘
                                             │
                               ┌─────────────▼─────────────┐
                               │ Pytest Integration Suite │ (Backend API, RBAC, Core 56 tests)
                               └─────────────┬─────────────┘
                                             │
                               ┌─────────────▼─────────────┐
                               │  Docker Full-Stack Check  │ (Container health & communication)
                               └───────────────────────────┘
```

---

## 3. Flagship E2E Scenario Specification

The flagship test (`frontend/e2e/phase7-flagship-integration.spec.ts`) executes a deterministic, 16-step procurement compliance workflow:

1. **Authentication**: Authenticate as `ProcurementOfficer` via Demo Identity Portal.
2. **Dashboard**: Load Command Center and verify operational metrics.
3. **Tender Selection**: Select seeded tender `TEN_01`.
4. **Tender Requirements**: Inspect extracted requirement specifications.
5. **Bid Selection**: Select seeded bid submission `SUB_01`.
6. **Document Extraction**: Inspect bidder document processing status.
7. **Government Verification**: Inspect Government Verification Center with explicit `MOCK / DEMO` badges.
8. **Evidence Lineage**: Verify 9 evidence quality dimensions and lineage graph.
9. **Compliance Matrix**: Evaluate deterministic compliance matrix results.
10. **Advisory Risk**: Review advisory risk signals (Advisory, non-authoritative).
11. **Human Review Queue**: Open human review queue and inspect pending tasks.
12. **Officer Decision**: Record officer decision and review item resolution.
13. **Manual Override & Four-Eyes**: Test override thresholds and senior reviewer approval requirement.
14. **Audit Hash Chain**: Open Audit Explorer and execute `Verify Audit Chain Integrity` (SHA-256 hash chain verification).
15. **System Invariants**: Verify AI remains non-authoritative and human officer holds final decision authority.
16. **Navigation Integrity**: Confirm smooth workspace navigation across all 14 application routes.

---

## 4. Test Environment Requirements & Isolation

- **Seed Data**: Deterministic seeded entities (`TEN_01`, `SUB_01`, `BID_01`).
- **Live Government API Isolation**: No live government credentials or external API calls required during test execution. All adapters use deterministic local mock responses.
- **Port Allocations**: Frontend (`3000`), Backend (`8000`), Postgres (`5432`), Redis (`6379`), MinIO (`9000`).
