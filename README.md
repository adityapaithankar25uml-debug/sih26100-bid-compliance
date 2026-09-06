# SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / CPCL  
**Phase:** Phase 2 — Implementation Foundation & Core Platform  
**Mode:** SIH Submission MVP Core Platform Baseline  
**Branch:** `phase-2-implementation` (Derived from frozen `phase-1-architecture` baseline)

---

## 1. Executive Summary & Core Architectural Axiom

The system is an **AI-assisted procurement compliance verification platform** designed for GeM procurement workflows within CPCL / Ministry of Petroleum & Natural Gas.

The architectural foundation operates on a strict non-authoritative AI principle:

```
AI INTERPRETS
        ↓
AUTHORIZED SOURCES VERIFY
        ↓
RULES EVALUATE
        ↓
EVIDENCE PROVES
        ↓
HUMAN APPROVES
```

### Key Invariants:
- **AI is Non-Authoritative:** AI models extract document structure and propose candidate facts; they do NOT evaluate compliance rules or make qualification decisions.
- **Backend Authorization is Authoritative:** Security and role permissions (`ProcurementOfficer`, `SeniorReviewer`, `Auditor`, `SystemAdmin`, `ServiceWorker`) are enforced strictly server-side.
- **MISSING_EVIDENCE ≠ FAIL:** Absence of verified evidence marks evaluation as `MISSING_EVIDENCE` / `REQUIRES_HUMAN_REVIEW` and never automatically disqualifies a bidder.
- **Tamper-Evident Audit Hash Chain:** Audit logs employ SHA-256 canonical event payload hashing and hash-chain block linkage for historical auditability.
- **Human Approval:** Qualification decisions belong exclusively to authorized human procurement officers.

---

## 2. Required Technology Baseline

- **Backend:** Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, PyJWT, Passlib (Argon2id/bcrypt)
- **Database:** PostgreSQL 16 (JSONB structured metadata)
- **Async & Queue:** Redis 7
- **Object Storage:** MinIO (Local S3-compatible storage)
- **Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide Icons
- **Containerization:** Docker & Docker Compose
- **Testing:** pytest & httpx

---

## 3. Local Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+ / 20+
- Docker & Docker Compose

### 1. Environment Configuration
Copy `.env.example` to create your local `.env` configuration:
```bash
cp .env.example .env
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
# On Windows PowerShell:
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

pip install -e .[dev]
```

### 3. Run Database Migrations & Synthetic Seed Data
```bash
# Execute Alembic migrations
alembic upgrade head

# Seed synthetic demonstration data
python -m app.db.seed
```

### 4. Run Backend Server
```bash
uvicorn app.main:app --reload --port 8000
```
- OpenAPI Documentation: `http://localhost:8000/docs`
- Health Probe: `http://localhost:8000/api/v1/health`
- Readiness Probe: `http://localhost:8000/api/v1/readiness`

### 5. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
- Access Frontend Application: `http://localhost:3000`

---

## 4. Docker Compose Setup

To launch the complete application stack (Backend, Frontend, PostgreSQL, Redis, MinIO) locally using Docker:

```bash
docker compose up --build -d
```

### Service Endpoints:
- **Frontend Application:** `http://localhost:3000`
- **Backend REST API & Swagger:** `http://localhost:8000/docs`
- **MinIO Storage Console:** `http://localhost:9001` (Credentials: `minioadmin` / `minioadmin`)
- **PostgreSQL Database:** `localhost:5432` (`sih26100_db`)
- **Redis Queue:** `localhost:6379`

To stop all services:
```bash
docker compose down
```

---

## 5. Automated Pytest Verification Suite

The backend includes unit and integration tests covering ULID generation, database models, REST APIs, RBAC authorization, and tamper-evident audit hash chain verification:

```bash
cd backend
python -m pytest
```

### Verification Checks Included:
1. `test_health.py`: Liveness (`/api/v1/health`) and readiness (`/api/v1/readiness`) probes.
2. `test_ulid.py`: 26-character Base32 Crockford ULID generator & format validation.
3. `test_models.py`: SQLAlchemy domain entity mappings and foreign key constraints.
4. `test_tenders_api.py`: Tender creation, TenderVersion immutability, and requirement binding.
5. `test_bidders_api.py`: Bidder registration and submission creation bound to specific TenderVersion.
6. `test_auth_rbac.py`: Authentication login and backend-authoritative role permission guards.
7. `test_audit_hash_chain.py`: Audit event canonical payload hashing, block chain verification, and **tamper detection test**.

---

## 6. Current Phase 2 Scope & Limitations

### Implemented in Phase 2:
- Backend application foundation & REST API structure (`/api/v1`)
- Database models for all 26 core Phase 1 domain entities
- Alembic database migration scripts
- Base32 Crockford 26-character ULID generator
- Backend-authoritative RBAC & isolated development auth provider
- Tamper-Evident Audit Hash Chain with SHA-256 canonical hashing & verification
- Redis connection probe & MinIO S3 storage abstraction
- Next.js 14 App Router frontend with deep navy / government blue UI
- Executive Procurement Dashboard, Tender Catalog, Bid Submissions, and Audit Chain Explorer
- Local Docker Compose environment
- Pytest backend test suite (10/10 tests passing)

### Intentionally Not Implemented in Phase 2 (Reserved for Later Phases):
- Full document extraction and OCR pipeline
- Full AI model gateway and prompt execution
- Live government portal integration (currently architectural mock/sandbox adapters)
- Full deterministic rule DSL evaluation execution
- Full Celery workflow DAG orchestrator
