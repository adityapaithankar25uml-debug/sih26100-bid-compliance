# Phase 4 — Testing Documentation

## 1. Test Suite Overview
Backend pytest suite `tests/test_verification_compliance.py` validates:
1. Government adapter contract & mock verification.
2. Technical transport failure vs business status decoupling.
3. Manual verification fallback recording.
4. AST rule engine security (blocking arbitrary code execution attempts).
5. Missing evidence deferral (ensuring missing evidence does not produce `FAIL`).
6. Make in India local content threshold calculation.
7. Full compliance engine evaluation & human review task creation.
8. Tamper-evident SHA-256 audit hash-chain integrity verification.

## 2. Smoke Test Execution
Automated smoke test `scripts/smoke_test_phase4.py` validates all 10 Phase 4 operational scenarios end-to-end.
