# SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Problem Statement:** SIH26100  
**Ministry / Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Theme:** Smart Automation | **Category:** Software  
**PS Requirement Coverage:** Comprehensive  
**Status:** SIH 2026 Submission & Presentation Ready  

---

## 1. Executive Summary & Core Architectural Axiom

The **SIH26100 Platform** is an enterprise-designed, evidence-first procurement compliance verification solution engineered for public procurement workflows on government portals like GeM (Government e-Marketplace).

### The Core Architectural Axiom
> **AI extraction is advisory. Deterministic compliance rules evaluate structured facts. Evidence and provenance support the evaluation. The authorized human officer retains final procurement decision authority.**

```
  [1. AI Extractions] ──> [2. 12 Govt Registries] ──> [3. Deterministic Rules]
                                                               │
  [6. Audit Hash Chain] <── [5. Human Officer Decision] <── [4. Advisory Risk Engine]
```

### Key System Guarantees:
- **Deterministic Compliance Rule Evaluation:** AI is used solely for document intelligence. Qualification rules are evaluated by pure boolean Python code (`actual >= required`).
- **Human Officer Authority:** Only authorized Procurement Officers can qualify or disqualify a bidder.
- **12 Statutory Registries:** Supports GST, Udyam/MSME, PAN, EPFO, ESIC, MCA, DPIIT Startup India, NSIC, OEM Authorization, DigiLocker, Central Debarment List, and GeM Profile via normalized integration adapters.
- **Non-Destructive Overrides & Four-Eyes Policy:** Manual rule overrides preserve point-in-time `EvaluationSnapshot` records. High-impact overrides enforce dual-officer approval (`PENDING_FOUR_EYES`).
- **Tamper-Evident SHA-256 Audit Hash Chain:** Every system event is serialized as canonical JSON and linked block-by-block with SHA-256 hashes for hash-chain integrity verification.

---

## 2. Mandatory Prototype Disclosures & Transparency

> **Government Integration Disclosure:**  
> For this SIH prototype, government registry responses are simulated through normalized integration adapters. The architecture is designed for authorized production connections, but no live government credentials or live government verification access are being claimed in this prototype. Furthermore, technical transport timeouts never result in automatic bidder rejection—they gracefully generate human review tasks.

> **Data Privacy Disclosure:**  
> The prototype includes deterministic detection and redaction patterns for configured sensitive data categories before external AI processing.

> **Audit System Disclosure:**  
> The audit mechanism verifies hash-chain integrity but does not itself constitute a PKI digital signature or legal non-repudiation mechanism.

---

## 3. Master Governance Documentation Vault (`docs/`)

The platform includes a complete documentation vault in `docs/`:

1. [`PHASE_8_SIH_TRACEABILITY.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_SIH_TRACEABILITY.md): Full PS requirement-to-implemented-capability mapping table.
2. [`PHASE_8_FINAL_SOLUTION_ARCHITECTURE.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_FINAL_SOLUTION_ARCHITECTURE.md): Comprehensive 8-layer architecture & core axiom breakdown.
3. [`PHASE_8_DEMO_SCRIPT.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_DEMO_SCRIPT.md): Step-by-step judge demonstration guide (7–10 minutes).
4. [`PHASE_8_JUDGE_TALKING_POINTS.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_JUDGE_TALKING_POINTS.md): Defense guide for key technical, security, and legal topics.
5. [`PHASE_8_INNOVATION_AND_DIFFERENTIATORS.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_INNOVATION_AND_DIFFERENTIATORS.md): 16 structural differentiators matrix.
6. [`PHASE_8_IMPACT_AND_METRICS.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_IMPACT_AND_METRICS.md): Operational impact, prototype benchmarks & production KPIs.
7. [`PHASE_8_SECURITY_PRIVACY_BRIEF.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_SECURITY_PRIVACY_BRIEF.md): Multi-layered security, RBAC, PII scrubber & prompt injection defense.
8. [`PHASE_8_AI_EXPLANATION.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_AI_EXPLANATION.md): Plain-language visual flow for non-technical judges.
9. [`PHASE_8_JUDGE_QA.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_JUDGE_QA.md): 30 detailed Q&A entries for difficult judge questions.
10. [`PHASE_8_LIMITATIONS_AND_PRODUCTION_ROADMAP.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_LIMITATIONS_AND_PRODUCTION_ROADMAP.md): Transparent prototype disclosures & 4-stage onboarding roadmap.
11. [`PHASE_8_PPT_CONTENT.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_PPT_CONTENT.md): Slide-by-slide content & speaker notes for 12 presentation slides.
12. [`PHASE_8_PROJECT_STRUCTURE.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_PROJECT_STRUCTURE.md): Repository structure guide.
13. [`PHASE_8_FINAL_SIH_CHECKLIST.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_FINAL_SIH_CHECKLIST.md): Itemized readiness checklist across 19 categories.
14. [`PHASE_8_FINAL_READINESS_REPORT.md`](file:///d:/PROJECTS/Bidder_AI/sih26100-bid-compliance/docs/PHASE_8_FINAL_READINESS_REPORT.md): Executive summary & readiness determination.

---

## 4. Technology Stack

- **Backend Framework:** FastAPI (Python 3.10+), Pydantic v2, SQLAlchemy 2.0, Alembic
- **Frontend Framework:** Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide Icons
- **Database Storage:** PostgreSQL 16 (Relational Metadata & Audit Store)
- **Cache & Async Queue:** Redis 7 & Celery
- **Object Vault:** MinIO Object Storage (Secure S3-compatible document storage)
- **Containerization:** Docker & Docker Compose
- **Test Automation:** Pytest (56 backend unit/integration tests) & Playwright (12 E2E suite tests)

---

## 5. How to Run Locally

### Prerequisites
- Python 3.10+
- Node.js 18+ / 20+
- Docker & Docker Compose (Optional)

### Step 1: Start Backend API Server
```bash
cd backend
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
*Note: Database tables and demonstration seed data (`TENDER-CPCL-2026-001`, `SUB-2026-CPCL-001`, demo users) will automatically initialize on startup.*

### Step 2: Start Frontend Web Portal
```bash
cd frontend
npm install
npm run dev
```
Open your browser and navigate to `http://localhost:3000`.

### Step 3: Authenticate & Explore
1. Go to `http://localhost:3000/login`.
2. Click **"Authenticate as ProcurementOfficer (Rajesh Kumar)"**.
3. Explore `/dashboard`, `/tenders`, `/bids/SUB_01`, `/verification`, `/evidence`, `/risk`, `/human-review`, and `/audit`.

---

## 6. Running Automated Verification Suites

### Run Backend Pytest Suite (56 Tests)
```bash
cd backend
python -m pytest
```

### Run Frontend Typecheck, Lint & Production Build
```bash
cd frontend
npx tsc --noEmit
npm run lint
npm run build
```

### Run Playwright E2E Integration Suite (12 Tests)
```bash
cd frontend
npx playwright test --workers=1
```

---

## 7. Containerized Docker Deployment

Validate configuration and start 5-service stack:
```bash
docker compose config
docker compose up -d --build
```
Containers started: `postgres`, `redis`, `minio`, `backend`, `frontend`.

---

## 8. License & Project Rights

Developed for **Smart India Hackathon (SIH) 2026** — Problem Statement **SIH26100**.  
All rights reserved for Ministry of Petroleum & Natural Gas / CPCL judging and evaluation.
