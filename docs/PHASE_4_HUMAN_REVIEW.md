# Phase 4 — Human Review & Manual Fallback

## 1. Human Decision Authority
Automated evaluations generate recommendations (`COMPLIANT`, `NON_COMPLIANT`, `REQUIRES_REVIEW`). Legally final qualification and disqualification decisions are strictly reserved for human procurement officers.

## 2. Review Trigger Triggers
Human review tasks (`HumanReviewTask`) are automatically created for:
- Ambiguous identity matches between submission and government records.
- Missing mandatory evidence where facts cannot be verified.
- Conflicting government verification results.
- Stale verification data exceeding freshness thresholds.
- Verification technical transport failures.

## 3. Manual Fallback Workflow
When automated government endpoints are unavailable or unestablished:
1. Procurement Officer inspects physical/documentary proof.
2. Officer records source, business status, verification date, notes, and uploaded evidence reference.
3. System records `is_manual_fallback = True`, logs officer identity, and appends entry to the SHA-256 tamper-evident audit hash chain.
