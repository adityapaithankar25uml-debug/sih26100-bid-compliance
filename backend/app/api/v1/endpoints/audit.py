from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.deps import get_db, get_current_user, require_roles
from app.schemas.domain import AuditEventResponse, AuditChainVerifyResponse
from app.services.audit_service import AuditService
from app.models.domain import AuditEvent, User

router = APIRouter()


@router.get("/events", response_model=List[AuditEventResponse], summary="List Audit Events")
def list_audit_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Auditor", "SeniorReviewer", "SystemAdmin"])),
):
    return db.query(AuditEvent).order_by(AuditEvent.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/verify-chain", response_model=AuditChainVerifyResponse, summary="Verify Tamper-Evident Audit Hash Chain Integrity")
def verify_audit_chain(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["Auditor", "SeniorReviewer", "SystemAdmin"])),
):
    is_valid, total, verified, corrupted_index, msg = AuditService.verify_chain_integrity(db)
    return AuditChainVerifyResponse(
        is_valid=is_valid,
        total_blocks=total,
        verified_blocks=verified,
        first_corrupted_block=corrupted_index,
        message=msg,
    )
