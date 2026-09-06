# Phase 4 — Known Limitations & Scope Boundaries

## 1. Mock Integration Mode
Default development environment operates under `MOCK` and `MANUAL_FALLBACK` modes. Production live API credentials for government portals (GSTN, Income Tax, MCA) are not configured.

## 2. No Autonomous Disqualification
The system generates deterministic compliance evaluations and recommendations but strictly does not execute autonomous legal disqualifications or contract awards.

## 3. Celery / Redis Asynchronous Execution Boundary
Async Celery worker execution for background verification polling requires a running Redis broker and Celery worker process.
