from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.deps import get_db, get_current_user, require_roles, get_correlation_id
from app.schemas.domain import DocumentRegisterRequest, DocumentResponse
from app.services.submission_service import BidSubmissionService
from app.services.audit_service import AuditService
from app.models.domain import User

router = APIRouter()


@router.post("", response_model=DocumentResponse, summary="Register Source Document Metadata")
def register_document(
    doc_in: DocumentRegisterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer"])),
    correlation_id: str = Depends(get_correlation_id),
):
    document = BidSubmissionService.register_document(db, doc_in)

    AuditService.log_event(
        db=db,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="SOURCE_DOCUMENT_REGISTERED",
        resource_type="SourceDocument",
        resource_id=document.id,
        correlation_id=correlation_id,
        payload={
            "filename": document.original_filename,
            "sha256_hash": document.sha256_hash,
            "size_bytes": document.file_size_bytes,
        },
    )

    return document
