# Phase 5 — Human Review Workspace Architecture

## 1. Overview
The Human Review Workspace provides procurement officers with a structured workspace to inspect, assign, and resolve compliance review items originating from AI extraction low-confidence flags, government verification conflicts, stale evidence, or policy review triggers.

## 2. Review Lifecycle
```
PENDING → IN_REVIEW → RESOLVED | REJECTED | ESCALATED
```

## 3. Human Review Task Model (`HumanReviewTask`)
- `bid_submission_id`: Bound submission identifier.
- `review_code`: Unique reference code (e.g. `REV_20260906143000`).
- `review_reason`: Explanation of why review was requested.
- `severity`: `CRITICAL` | `HIGH` | `MEDIUM` | `LOW`
- `priority`: `CRITICAL` | `HIGH` | `MEDIUM` | `LOW`
- `status`: `PENDING` | `IN_REVIEW` | `RESOLVED` | `REJECTED` | `ESCALATED`
- `assigned_officer_id`: Procurement officer assigned to review.
- `suggested_action`: AI/system recommended inspection steps.
- `resolution_summary`: Officer written summary upon resolution.
- `review_history_json`: Complete timeline of status transitions and assignments.

## 4. RBAC & Governance
Only authorized procurement roles (`ProcurementOfficer`, `SeniorReviewer`, `ComplianceOfficer`, `SystemAdmin`) can query, assign, or resolve human review tasks. Bidders (`Role.BIDDER`) receive `403 Forbidden`.
