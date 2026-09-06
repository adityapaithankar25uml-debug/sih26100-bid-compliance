# Phase 7 — Docker Compose & Full-Stack Deployment Verification

## 1. Multi-Container Services Architecture

The SIH26100 platform is orchestrated using Docker Compose (`docker-compose.yml`), encapsulating all database, caching, object storage, API backend, and Next.js frontend services:

```
                          ┌──────────────────────────┐
                          │    Next.js Frontend      │ (Port 3000)
                          └────────────┬─────────────┘
                                       │ HTTP / REST
                                       ▼
                          ┌──────────────────────────┐
                          │     FastAPI Backend      │ (Port 8000)
                          └──────┬─────┬──────┬──────┘
                                 │     │      │
            ┌────────────────────┘     │      └────────────────────┐
            ▼                          ▼                           ▼
┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐
│ PostgreSQL 16 Alpine  │  │    Redis 7 Alpine     │  │ MinIO Object Storage  │
│      (Port 5432)      │  │      (Port 6379)      │  │     (Port 9000)       │
└───────────────────────┘  └───────────────────────┘  └───────────────────────┘
```

---

## 2. Service Definitions & Health Check Controls

### 1. `postgres` (PostgreSQL 16 Alpine)
- **Container Name**: `sih26100-postgres`
- **Port**: `5432:5432`
- **Healthcheck**: `pg_isready -U sih_user -d sih26100_db` (Interval 5s, timeout 5s, retries 5)

### 2. `redis` (Redis 7 Alpine)
- **Container Name**: `sih26100-redis`
- **Port**: `6379:6379`
- **Healthcheck**: `redis-cli ping` (Interval 5s, timeout 3s, retries 5)

### 3. `minio` (MinIO Object Storage)
- **Container Name**: `sih26100-minio`
- **Ports**: `9000:9000`, `9001:9001` (Console)
- **Healthcheck**: `curl -f http://localhost:9000/minio/health/live` (Interval 5s, timeout 3s, retries 5)

### 4. `backend` (FastAPI Modular Monolith)
- **Container Name**: `sih26100-backend`
- **Port**: `8000:8000`
- **Healthcheck**: `curl -f http://localhost:8000/api/v1/health || exit 1` (Interval 10s, timeout 5s, retries 5)
- **Dependencies**: Depends on `postgres`, `redis`, and `minio` being healthy.

### 5. `frontend` (Next.js 14 App Router)
- **Container Name**: `sih26100-frontend`
- **Port**: `3000:3000`
- **Build Args**: `NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1`
- **Dependencies**: Depends on `backend` being healthy.

---

## 3. Deployment & Readiness Verification Procedure

### Single-Command Full-Stack Start
```bash
docker-compose up --build -d
```

### Healthcheck Status Inspection
```bash
docker-compose ps
```

### Verification Criteria
- All containers status: `Up (healthy)`.
- Backend readiness probe returns 200 OK: `http://localhost:8000/api/v1/readiness`.
- Frontend loads Command Center without connection errors: `http://localhost:3000/dashboard`.
