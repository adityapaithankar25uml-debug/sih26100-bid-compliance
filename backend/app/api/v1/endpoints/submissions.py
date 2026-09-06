from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.deps import get_db, get_current_user, require_roles, get_correlation_id
from app.schemas.domain import SubmissionCreate, SubmissionResponse
from app.services.submission_service import BidSubmissionService
from app.services.audit_service import AuditService
from app.models.domain import User

router = APIRouter()


@router.post("", response_model=SubmissionResponse, summary="Submit Bid Proposal bound to TenderVersion")
def create_submission(
    sub_in: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer"])),
    correlation_id: str = Depends(get_correlation_id),
):
    submission = BidSubmissionService.create_submission(db, sub_in)

    AuditService.log_event(
        db=db,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="BID_SUBMITTED",
        resource_type="BidSubmission",
        resource_id=submission.id,
        correlation_id=correlation_id,
        payload={
            "reference": submission.submission_reference,
            "bidder_id": submission.bidder_id,
            "tender_id": submission.tender_id,
            "tender_version_id": submission.tender_version_id,
        },
    )

    return submission


@router.get("", response_model=List[SubmissionResponse], summary="List Bid Submissions")
def list_submissions(
    tender_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BidSubmissionService.list_submissions(db, tender_id=tender_id, skip=skip, limit=limit)


@router.get("/{submission_id}", response_model=SubmissionResponse, summary="Get Bid Submission Details")
def get_submission(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sub = BidSubmissionService.get_submission_by_id(db, submission_id)
    if not sub:
        raise HTTPException(status_code=404, detail="Bid submission not found.")
    return sub
