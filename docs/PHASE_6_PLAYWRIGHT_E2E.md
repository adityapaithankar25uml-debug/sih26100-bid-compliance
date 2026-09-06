# Phase 6 — Playwright E2E Test Suite Specification

## 1. Test Foundation & Coverage
The Playwright test foundation located in `frontend/e2e/phase6-procurement.spec.ts` covers the complete procurement compliance workflow:

1. **Authentication & Authorized Demo Identity / Role-Aware UI:** Verifies login, backend JWT assignment, and role-adaptive UI navigation.
2. **Procurement Dashboard Render:** Verifies workload metrics, system principle banner, and audit status cards.
3. **Tender Catalog Navigation & Search:** Verifies catalog search filtering and version tags.
4. **Tender Workspace:** Verifies version amendment history and requirement specifications.
5. **Bid Submission Registry:** Verifies submission directory listing and bidder mapping.
6. **Bid Workspace & Compliance Matrix:** Verifies separation of compliance status (`PASS`, `FAIL`, `MISSING_EVIDENCE`) from risk.
7. **Government Verification Center:** Verifies dynamic rendering of government source adapters and `MOCK / DEMO` integration mode badges.
8. **Evidence Explorer & 9 Quality Dimensions:** Verifies independent presentation of all 9 quality dimensions.
9. **Advisory Risk Engine Panel:** Verifies non-linear risk score calculation and mandatory advisory notices.
10. **Human Review Task Queue:** Verifies task listing and resolution workflow.
11. **Tamper-Evident SHA-256 Audit Hash Chain Explorer:** Verifies audit log rendering and `Verify Audit Chain Integrity` action trigger.
