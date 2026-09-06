from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.deps import get_db, get_current_user, require_roles, get_correlation_id
from app.schemas.domain import BidderCreate, BidderResponse
from app.services.bidder_service import BidderService
from app.services.audit_service import AuditService
from app.models.domain import User

router = APIRouter()


@router.post("", response_model=BidderResponse, summary="Register New Bidder Entity")
def create_bidder(
    bidder_in: BidderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer"])),
    correlation_id: str = Depends(get_correlation_id),
):
    bidder = BidderService.create_bidder(db, bidder_in)

    AuditService.log_event(
        db=db,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="BIDDER_REGISTERED",
        resource_type="Bidder",
        resource_id=bidder.id,
        correlation_id=correlation_id,
        payload={"bidder_name": bidder.bidder_name, "registration": bidder.registration_number},
    )

    return bidder


@router.get("", response_model=List[BidderResponse], summary="List Registered Bidders")
def list_bidders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return BidderService.list_bidders(db, skip=skip, limit=limit)


@router.get("/{bidder_id}", response_model=BidderResponse, summary="Get Bidder Profile")
def get_bidder(
    bidder_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bidder = BidderService.get_bidder_by_id(db, bidder_id)
    if not bidder:
        raise HTTPException(status_code=404, detail="Bidder not found.")
    return bidder
