# Phase 5 — Human Officer Decision Model & Workflow

## 1. Principle of Human Authority
**“AI interprets. Authorized sources verify. Rules evaluate. Evidence proves. Risk prioritizes. Human decides. Audit remembers.”**

Human procurement officers remain the final decision authority over bidder qualification decisions.

## 2. Decision States (`OfficerDecision`)
- `QUALIFIED`: Bidder satisfies all mandatory procurement criteria.
- `DISQUALIFIED`: Bidder fails one or more mandatory qualification criteria.
- `REQUIRES_CLARIFICATION`: Formal clarification requested from bidder.
- `EVIDENCE_REQUESTED`: Additional supporting documentation requested.

## 3. Evaluation Snapshot Integration
Before recording any officer decision, the system automatically constructs a point-in-time `EvaluationSnapshot` capturing:
- Full compliance rule results and explanations.
- All government verification statuses and raw response hashes.
- Verified facts and provenance references.
- Advisory risk score and factor signals.
- SHA-256 snapshot hash.

## 4. Audit Chain Linkage
Every `OfficerDecision` emits an auditable domain event appended to the **TAMPER-EVIDENT SHA-256 AUDIT HASH CHAIN**.
