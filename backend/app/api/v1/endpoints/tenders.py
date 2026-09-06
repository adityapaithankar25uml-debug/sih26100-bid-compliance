from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.deps import get_db, get_current_user, require_roles, get_correlation_id
from app.schemas.domain import (
    TenderCreate,
    TenderResponse,
    TenderVersionResponse,
    RequirementCreate,
    RequirementResponse,
)
from app.services.tender_service import TenderService
from app.services.audit_service import AuditService
from app.models.domain import User

router = APIRouter()


@router.post("", response_model=TenderResponse, summary="Create New Procurement Tender")
def create_tender(
    tender_in: TenderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer"])),
    correlation_id: str = Depends(get_correlation_id),
):
    existing = TenderService.get_tender_by_number(db, tender_in.tender_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tender number '{tender_in.tender_number}' already exists.",
        )

    tender = TenderService.create_tender(db, tender_in)

    AuditService.log_event(
        db=db,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="TENDER_CREATED",
        resource_type="Tender",
        resource_id=tender.id,
        correlation_id=correlation_id,
        payload={"tender_number": tender.tender_number, "title": tender.title},
    )

    return tender


@router.get("", response_model=List[TenderResponse], summary="List Procurement Tenders")
def list_tenders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TenderService.list_tenders(db, skip=skip, limit=limit)


@router.get("/{tender_id}", response_model=TenderResponse, summary="Get Tender by ID")
def get_tender(
    tender_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tender = TenderService.get_tender_by_id(db, tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found.")
    return tender


@router.post("/{tender_id}/versions", response_model=TenderVersionResponse, summary="Create New Tender Version Amendment")
def create_tender_version(
    tender_id: str,
    description: str = "Tender amendment",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer"])),
    correlation_id: str = Depends(get_correlation_id),
):
    version = TenderService.create_tender_version(db, tender_id, description=description)
    if not version:
        raise HTTPException(status_code=404, detail="Tender not found.")

    AuditService.log_event(
        db=db,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="TENDER_VERSION_CREATED",
        resource_type="TenderVersion",
        resource_id=version.id,
        correlation_id=correlation_id,
        payload={"tender_id": tender_id, "version_number": version.version_number},
    )

    return version


@router.post("/versions/{version_id}/requirements", response_model=RequirementResponse, summary="Add Requirement to Tender Version")
def add_requirement(
    version_id: str,
    req_in: RequirementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer"])),
    correlation_id: str = Depends(get_correlation_id),
):
    requirement = TenderService.add_requirement(db, version_id, req_in)

    AuditService.log_event(
        db=db,
        actor_id=current_user.id,
        actor_role=current_user.role,
        action="TENDER_REQUIREMENT_CREATED",
        resource_type="TenderRequirement",
        resource_id=requirement.id,
        correlation_id=correlation_id,
        payload={"code": requirement.requirement_code, "category": requirement.category},
    )

    return requirement


@router.get("/versions/{version_id}/requirements", response_model=List[RequirementResponse], summary="List Requirements for Tender Version")
def list_requirements(
    version_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return TenderService.list_requirements_for_version(db, version_id)
