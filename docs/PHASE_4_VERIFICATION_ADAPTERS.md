# Phase 4 — Verification Adapters Documentation

## 1. Adapter Registry Architecture
The `GovernmentAdapterRegistry` manages 12 pluggable adapters implementing `BaseGovernmentAdapter`.

```
GovernmentAdapterRegistry
 ├── GSTAdapter
 ├── UdyamAdapter
 ├── PANAdapter
 ├── MCAAdapter
 ├── EPFOAdapter
 ├── ESICAdapter
 ├── StartupIndiaAdapter
 ├── NSICAdapter
 ├── OEMAuthAdapter
 ├── DebarmentAdapter
 ├── GeMProfileAdapter
 └── DigiLockerAdapter
```

## 2. Readiness Taxonomy
Each adapter reports its operational readiness:
- `CONFIRMED_DOCUMENTATION`
- `PRODUCTION_ACCESS_NOT_ESTABLISHED`
- `SANDBOX_AVAILABLE`
- `MOCK_ONLY`
- `MANUAL_FALLBACK_REQUIRED`
- `NOT_AVAILABLE`

## 3. Mock Fixtures & Identity Match Scoring
For development and demonstration without live credentials, adapters execute deterministic mock verifications against synthetic test data:
- Exact identifier match yields `MATCHED` (1.0 confidence score).
- Soft legal name comparison determines `MATCHED`, `PARTIAL_MATCH`, or `AMBIGUOUS`.
- Synthetic test prefixes (e.g. `33TIMEOUT...`) trigger mock technical timeouts for boundary testing.
