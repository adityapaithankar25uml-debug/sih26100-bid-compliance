# Phase 8 — Project Structure & Repository Layout Guide

## Repository Root Directory Tree

```
sih26100-bid-compliance/
├── backend/                        # FastAPI Python Backend Application
│   ├── alembic/                    # Database Migrations (Immutable Alembic Lineage)
│   │   ├── versions/               # Historical Alembic migration versions
│   │   └── env.py                  # Alembic environment config
│   ├── app/                        # Application Core Source Code
│   │   ├── api/                    # API Routing Layer
│   │   │   ├── v1/                 # API Version 1 Endpoints
│   │   │   │   ├── endpoints/      # Domain Endpoints (auth, tenders, bids, verification, audit, phase5)
│   │   │   │   ├── router.py       # API Router Aggregator
│   │   │   │   └── deps.py         # Dependencies (DB session, JWT Auth, RBAC)
│   │   ├── core/                   # Core Application Configuration
│   │   │   ├── config.py           # Pydantic Settings & Environment Configuration
│   │   │   ├── logging.py          # Structured JSON Logger Setup
│   │   │   └── security.py         # Password Hashing & JWT Token Utilities
│   │   ├── db/                     # Database Session & Seeding
│   │   │   ├── session.py          # SQLAlchemy Session & Engine Setup
│   │   │   └── seed.py             # Idempotent Demonstration Data Seeder
│   │   ├── models/                 # SQLAlchemy Domain Data Models
│   │   │   ├── domain.py           # 32 Bounded Domain Models (User, Tender, Bid, Audit, etc.)
│   │   │   └── mixins.py           # Base Model Mixins (ULID primary keys, timestamps)
│   │   ├── schemas/                # Pydantic Request/Response DTO Schemas
│   │   │   ├── domain.py           # Standard Domain Schemas
│   │   │   └── phase5.py           # Evidence, Risk, Human Review, Override Schemas
│   │   ├── services/               # Core Business Logic & Engine Services
│   │   │   ├── ai_gateway.py       # AI Provider Abstraction & PII Scrubber
│   │   │   ├── audit_service.py    # Tamper-Evident SHA-256 Audit Hash Chain Service
│   │   │   ├── compliance_engine.py# Deterministic Rule Evaluation Matrix Engine
│   │   │   ├── evidence_service.py # 9-Dimension Evidence Model Service
│   │   │   ├── officer_decision_service.py # Human Officer Decisions & Overrides
│   │   │   ├── risk_service.py     # Advisory Risk Engine & Signal Aggregation
│   │   │   └── verification_service.py # 12 Government Portal Adapters
│   │   └── main.py                 # FastAPI Application Lifecycle & Middleware Entrypoint
│   ├── tests/                      # Pytest Automated Test Suite
│   │   ├── test_audit_hash_chain.py
│   │   ├── test_auth_rbac.py
│   │   ├── test_health.py
│   │   ├── test_phase3_document_ai.py
│   │   ├── test_phase4_verification_and_compliance.py
│   │   └── test_phase5_evidence_risk_human_review.py
│   ├── Dockerfile                  # Backend Container Build Definition
│   ├── pytest.ini                  # Pytest Configuration
│   └── requirements.txt            # Python Dependencies Specification
│
├── frontend/                       # Next.js 14 Web Application
│   ├── app/                        # Next.js App Router Pages
│   │   ├── audit/                  # Tamper-Evident Audit Hash Chain Explorer
│   │   ├── bids/                   # Bid Workspace Directory
│   │   │   └── [id]/               # Bid Verification Workspace (Bidder 360, Matrix, Overrides)
│   │   ├── dashboard/              # Executive Procurement Command Center
│   │   ├── documents/              # Document Viewer & Upload Interface
│   │   ├── evidence/               # Evidence Explorer & Quality Dimensions
│   │   ├── human-review/           # Human Review Task Queue Workspace
│   │   ├── login/                  # Officer Authentication & Demo Identity Selector
│   │   ├── risk/                   # Advisory Risk Engine Management Panel
│   │   ├── tenders/                # Tender Specification Catalog
│   │   │   └── [id]/               # Tender Detail & Version History
│   │   ├── verification/           # Government Verification Center & MOCK Badges
│   │   ├── layout.tsx              # Application Root Layout & Navigation Bar
│   │   ├── page.tsx                # Homepage Redirect
│   │   └── globals.css             # Vanilla CSS Tokens & Global Utility Styling
│   ├── components/                 # Reusable UI Components
│   │   ├── Header.tsx              # Officer Navigation Header
│   │   └── StatusBadge.tsx         # Domain Status Badges
│   ├── e2e/                        # Playwright End-to-End Test Suite
│   │   ├── phase6-procurement.spec.ts          # 11 Phase 6 UI Workflow Tests
│   │   └── phase7-flagship-integration.spec.ts # Flagship 16-Step E2E Lifecycle Test
│   ├── lib/                        # Client API Helpers
│   │   └── api.ts                  # Fetch API Wrapper (Correlation & Auth Headers)
│   ├── types/                      # TypeScript Global Interface Definitions
│   │   └── index.ts                # Domain Interfaces (User, Tender, Bid, Audit, Risk, etc.)
│   ├── Dockerfile                  # Frontend Production Container Build Definition
│   ├── next.config.js              # Next.js Framework Configuration
│   ├── package.json                # Frontend Dependencies & Scripts
│   ├── playwright.config.ts        # Playwright E2E Configuration
│   └── tsconfig.json               # TypeScript Compiler Configuration
│
├── docs/                           # Complete Phase 0–8 Documentation Vault
│   ├── PHASE_7_INTEGRATION_ARCHITECTURE.md
│   ├── PHASE_7_E2E_TEST_STRATEGY.md
│   ├── PHASE_7_TEST_MATRIX.md
│   ├── PHASE_7_DEMO_WORKFLOW.md
│   ├── PHASE_7_DOCKER_VERIFICATION.md
│   ├── PHASE_7_ASYNC_WORKFLOW_VERIFICATION.md
│   ├── PHASE_7_INTEGRATION_GAP_REGISTER.md
│   ├── PHASE_7_FINAL_VERIFICATION_REPORT.md
│   ├── PHASE_8_SIH_TRACEABILITY.md
│   ├── PHASE_8_FINAL_SOLUTION_ARCHITECTURE.md
│   ├── PHASE_8_DEMO_SCRIPT.md
│   ├── PHASE_8_JUDGE_TALKING_POINTS.md
│   ├── PHASE_8_INNOVATION_AND_DIFFERENTIATORS.md
│   ├── PHASE_8_IMPACT_AND_METRICS.md
│   ├── PHASE_8_SECURITY_PRIVACY_BRIEF.md
│   ├── PHASE_8_AI_EXPLANATION.md
│   ├── PHASE_8_JUDGE_QA.md
│   ├── PHASE_8_LIMITATIONS_AND_PRODUCTION_ROADMAP.md
│   ├── PHASE_8_PPT_CONTENT.md
│   ├── PHASE_8_PROJECT_STRUCTURE.md
│   ├── PHASE_8_FINAL_SIH_CHECKLIST.md
│   └── PHASE_8_FINAL_READINESS_REPORT.md
│
├── docker-compose.yml              # Complete 5-Service Docker Stack Definition
├── PROJECT_STATUS.md               # Master Project Status Baseline
└── README.md                       # Comprehensive SIH Judge-Facing Master README
```
