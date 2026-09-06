from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.v1.deps import get_db
from app.services.redis_service import RedisService
from app.services.storage_service import StorageService

router = APIRouter()


@router.get("/health", summary="Process Liveness Probe")
def get_health():
    """
    Indicates backend process liveness.
    """
    return {
        "status": "healthy",
        "service": "sih26100-backend",
        "mode": "modular-monolith",
    }


@router.get("/readiness", summary="Service Readiness Probe")
def get_readiness(db: Session = Depends(get_db)):
    """
    Verifies operational readiness of database, queue, and object storage dependencies
    without exposing credentials or sensitive connection parameters.
    """
    readiness_status = {
        "status": "ready",
        "components": {},
    }

    # 1. Database Check
    try:
        db.execute(text("SELECT 1"))
        readiness_status["components"]["database"] = {"status": "connected", "type": "PostgreSQL"}
    except Exception as e:
        readiness_status["status"] = "not_ready"
        readiness_status["components"]["database"] = {"status": "error", "detail": "Database ping failed"}

    # 2. Redis Check
    redis_ok, redis_info = RedisService.check_readiness()
    readiness_status["components"]["redis"] = redis_info
    if not redis_ok:
        readiness_status["status"] = "degraded"

    # 3. MinIO Check
    storage_ok, storage_info = StorageService.check_readiness()
    readiness_status["components"]["object_storage"] = storage_info
    if not storage_ok:
        readiness_status["status"] = "degraded"

    return readiness_status
