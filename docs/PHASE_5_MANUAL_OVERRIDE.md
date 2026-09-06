# Phase 5 — Non-Destructive Manual Override Governance

## 1. Non-Destructive Invariant
Manual overrides NEVER overwrite or mutate historical deterministic compliance evaluations in place. The original evaluation (e.g. `MISSING_EVIDENCE`, `FAIL`) remains permanently recorded in `ComplianceEvaluation` and `ComplianceRuleResult`.

## 2. Override Structure (`ManualOverride`)
- `officer_decision_id`: Foreign key to bound officer decision.
- `requirement_id`: Tender requirement being overridden.
- `previous_status`: Original deterministic rule status (e.g. `MISSING_EVIDENCE`).
- `new_status`: Overridden status (e.g. `PASS`).
- `override_reason_code`: Structured code (`NEW_EVIDENCE`, `SOURCE_CORRECTION`, `IDENTITY_CLARIFICATION`, `POLICY_EXCEPTION`, `DATA_CORRECTION`, `OFFICER_REVIEW`, `OTHER`).
- `override_reason`: Required text explanation by procurement officer.
- `supporting_evidence_refs_json`: References to supporting evidence documents.
- `requires_four_eyes`: Policy-controlled boolean flag.
- `four_eyes_status`: `PENDING_APPROVAL` | `APPROVED` | `REJECTED`.

## 3. Four-Eyes Approval Workflow
Where required by policy (`requires_four_eyes = True`):
1. **Officer A** submits override request (`status = PENDING_APPROVAL`).
2. **Officer B** (`SeniorReviewer` or `ComplianceOfficer`) reviews rationale and approves (`status = APPROVED`).
3. Both actions append separate verification events to the Tamper-Evident SHA-256 Audit Hash Chain.

## 4. Manual Override API Endpoints
The platform exposes protected REST endpoints governed by backend RBAC (`ProcurementOfficer`, `SeniorReviewer`, `ComplianceOfficer`, `SystemAdmin`):
- `POST /api/v1/bids/{submission_id}/manual-overrides`: Create non-destructive manual override.
- `GET /api/v1/bids/{submission_id}/manual-overrides`: Fetch manual overrides for a submission.
- `GET /api/v1/manual-overrides/{id}`: Fetch manual override by ID.
- `POST /api/v1/manual-overrides/{override_id}/approve`: Process four-eyes approval/rejection.

*Security Control:* `BIDDER` role attempts to invoke protected override endpoints are strictly rejected with `403 Forbidden`.
