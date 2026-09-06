# Phase 4 — Government Verification Implementation Architecture

## 1. Overview
The Phase 4 Government Verification subsystem establishes normalized, adapter-driven verification across 12 primary government registries. It acts as the bridge between extracted document facts and authoritative government verification standards, enforcing the axiom:

> *"AI interprets. Authorized sources verify. Rules evaluate. Evidence proves. Human approves."*

## 2. Core Separation of Technical & Business Status
Every verification attempt strictly decouples:
- **Technical Status**: `SUCCESS`, `TIMEOUT`, `RATE_LIMITED`, `UNAVAILABLE`, `AUTH_FAILED`, `VALIDATION_ERROR`
- **Business Verification Status**: `VERIFIED`, `NOT_VERIFIED`, `NOT_FOUND`, `INACTIVE`, `CANCELLED`, `DEBARRED`, `NOT_DEBARRED`, `CONFLICTING`, `UNKNOWN`, `STALE`

### Technical Failure Non-Penalization Invariant
Technical transport failures (e.g., API timeout or connection error) yield `UNAVAILABLE` / `NOT_VERIFIED` / `UNKNOWN`. They are strictly guaranteed **NEVER** to convert into business compliance failures (`FAIL`).

## 3. Integration Modes & Labeling
Each source operates under explicit integration modes:
- `MOCK`: Synthetic mock data for local/offline execution.
- `SANDBOX`: Test environment connected to sandbox government APIs.
- `LIVE`: Authoritative production API mode (requires production credentials).
- `MANUAL_FALLBACK`: Human procurement officer verification.

> [!IMPORTANT]
> The system explicitly labels mock data as `MOCK` and strictly prevents mock verifications from displaying as `GOVERNMENT VERIFIED` in the UI.

## 4. Government Source Registries
12 verification categories are registered:
1. **GST**: Tax registration, active status, return compliance.
2. **UDYAM**: MSME classification, enterprise status.
3. **PAN**: Taxpayer identity & name matching.
4. **MCA**: Corporate identity (CIN) & company status.
5. **EPFO**: Employee Provident Fund establishment registration.
6. **ESIC**: Employee State Insurance registration.
7. **STARTUP_INDIA**: DPIIT startup recognition status.
8. **NSIC**: Single point registration certificate.
9. **OEM_AUTH**: Manufacturer authorization certificate.
10. **DEBARMENT**: GeM/CPPP administrative blacklisting status.
11. **GEM_PROFILE**: GeM seller profile & rating.
12. **DIGILOCKER**: Consent-based document verification.
