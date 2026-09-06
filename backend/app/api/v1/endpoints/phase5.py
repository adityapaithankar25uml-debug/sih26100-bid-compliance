from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.v1.deps import get_current_user, require_roles
from app.models.domain import (
    User,
    EvidenceRecord,
    EvaluationSnapshot,
    RiskAssessmentProfile,
    HumanReviewTask,
    OfficerDecision,
    ManualOverride,
    BidSubmission
)
from app.services.evidence_service import evidence_service
from app.services.risk_service import risk_service
from app.services.review_service import review_service
from app.services.officer_decision_service import officer_decision_service
from app.schemas.phase5 import (
    EvidenceRecordResponse,
    EvidenceTraceGraphResponse,
    ComplianceExplanationResponse,
    EvaluationSnapshotResponse,
    RiskAssessmentResponse,
    HumanReviewTaskResponse,
    HumanReviewAssignRequest,
    HumanReviewResolveRequest,
    OfficerDecisionRequest,
    OfficerDecisionResponse,
    ManualOverrideCreateRequest,
    ManualOverrideApproveRequest,
    ManualOverrideResponse
)

router = APIRouter()


# ============================================================
# EVIDENCE LEDGER & TRACEABILITY ENDPOINTS
# ============================================================

@router.get("/evidence/{id}", response_model=EvidenceRecordResponse)
def get_evidence_record(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ev = db.query(EvidenceRecord).filter_by(id=id).first()
    if not ev:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence record not found")
    return ev


@router.get("/evidence/{id}/trace", response_model=EvidenceTraceGraphResponse)
def get_evidence_trace_by_id(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ev = db.query(EvidenceRecord).filter_by(id=id).first()
    if not ev or not ev.bid_submission_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence trace not found")
    return evidence_service.get_evidence_trace(db, submission_id=ev.bid_submission_id, requirement_id=ev.requirement_id)


@router.get("/bids/{submission_id}/evidence", response_model=List[EvidenceRecordResponse])
def list_bid_evidence(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    records = db.query(EvidenceRecord).filter_by(bid_submission_id=submission_id).all()
    return records


@router.get("/bids/{submission_id}/evidence-trace", response_model=EvidenceTraceGraphResponse)
def get_bid_evidence_trace(
    submission_id: str,
    requirement_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return evidence_service.get_evidence_trace(db, submission_id=submission_id, requirement_id=requirement_id)


# ============================================================
# COMPLIANCE EXPLANATION ("WHY?" VIEW)
# ============================================================

@router.get("/bids/{submission_id}/explanation", response_model=ComplianceExplanationResponse)
def get_bid_compliance_explanation(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return evidence_service.get_compliance_explanation(db, submission_id=submission_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================
# EVALUATION SNAPSHOTS
# ============================================================

@router.get("/bids/{submission_id}/evaluation-snapshots", response_model=List[EvaluationSnapshotResponse])
def list_bid_evaluation_snapshots(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    snapshots = db.query(EvaluationSnapshot).filter_by(bid_submission_id=submission_id).order_by(EvaluationSnapshot.created_at.desc()).all()
    return snapshots


@router.get("/evaluation-snapshots/{id}", response_model=EvaluationSnapshotResponse)
def get_evaluation_snapshot(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    snap = db.query(EvaluationSnapshot).filter_by(id=id).first()
    if not snap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evaluation snapshot not found")
    return snap


# ============================================================
# ADVISORY RISK ENGINE ENDPOINTS
# ============================================================

@router.get("/bids/{submission_id}/risk-assessment", response_model=RiskAssessmentResponse)
def get_bid_risk_assessment(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prof = db.query(RiskAssessmentProfile).filter_by(bid_submission_id=submission_id).order_by(RiskAssessmentProfile.calculated_at.desc()).first()
    if not prof:
        prof = risk_service.assess_bid_risk(db, submission_id)
    return prof


@router.post("/bids/{submission_id}/assess-risk", response_model=RiskAssessmentResponse)
def calculate_bid_risk_assessment(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin", "ServiceWorker"]))
):
    try:
        return risk_service.assess_bid_risk(db, submission_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================
# HUMAN REVIEW WORKSPACE ENDPOINTS
# ============================================================

@router.get("/human-reviews", response_model=List[HumanReviewTaskResponse])
def list_human_reviews(
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    return review_service.list_review_tasks(db, status_filter=status_filter, priority_filter=priority_filter)


@router.get("/human-reviews/{id}", response_model=HumanReviewTaskResponse)
def get_human_review_task(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    task = db.query(HumanReviewTask).filter_by(id=id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Human review task not found")
    return task


@router.post("/human-reviews/{id}/assign", response_model=HumanReviewTaskResponse)
def assign_human_review_task(
    id: str,
    req: HumanReviewAssignRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    try:
        return review_service.assign_review_task(db, task_id=id, officer_id=req.officer_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/human-reviews/{id}/resolve", response_model=HumanReviewTaskResponse)
def resolve_human_review_task(
    id: str,
    req: HumanReviewResolveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    try:
        return review_service.resolve_review_task(
            db=db,
            task_id=id,
            officer_id=current_user.id,
            decision=req.decision,
            resolution_summary=req.resolution_summary,
            comments=req.comments
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# ============================================================
# OFFICER DECISION & MANUAL OVERRIDE ENDPOINTS
# ============================================================

@router.get("/bids/{submission_id}/officer-decisions", response_model=List[OfficerDecisionResponse])
def list_bid_officer_decisions(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    decisions = db.query(OfficerDecision).filter_by(bid_submission_id=submission_id).order_by(OfficerDecision.decision_timestamp.desc()).all()
    return decisions


@router.post("/bids/{submission_id}/officer-decisions", response_model=OfficerDecisionResponse, status_code=status.HTTP_201_CREATED)
def record_officer_decision(
    submission_id: str,
    req: OfficerDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    overrides_list = [ov.dict() for ov in req.overrides] if req.overrides else None
    try:
        return officer_decision_service.record_officer_decision(
            db=db,
            bid_submission_id=submission_id,
            reviewer_id=current_user.id,
            reviewer_role=current_user.role,
            decision=req.decision,
            rationale=req.rationale,
            overrides_data=overrides_list
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/bids/{submission_id}/manual-overrides", response_model=List[ManualOverrideResponse])
def list_bid_manual_overrides(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    overrides = db.query(ManualOverride).filter_by(bid_submission_id=submission_id).order_by(ManualOverride.created_at.desc()).all()
    return overrides


@router.get("/manual-overrides/{id}", response_model=ManualOverrideResponse)
def get_manual_override(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ov = db.query(ManualOverride).filter_by(id=id).first()
    if not ov:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manual override not found")
    return ov


@router.post("/bids/{submission_id}/manual-overrides", response_model=ManualOverrideResponse, status_code=status.HTTP_201_CREATED)
def record_manual_override(
    submission_id: str,
    req: ManualOverrideCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    dec = db.query(OfficerDecision).filter_by(bid_submission_id=submission_id, reviewer_id=current_user.id).order_by(OfficerDecision.decision_timestamp.desc()).first()
    if not dec:
        dec = officer_decision_service.record_officer_decision(
            db=db,
            bid_submission_id=submission_id,
            reviewer_id=current_user.id,
            reviewer_role=current_user.role,
            decision="REQUIRES_CLARIFICATION",
            rationale="Initial officer decision recorded prior to manual requirement override."
        )

    return officer_decision_service.create_manual_override(
        db=db,
        officer_decision_id=dec.id,
        bid_submission_id=submission_id,
        requirement_id=req.requirement_id,
        rule_id=req.rule_id,
        previous_status=req.previous_status,
        new_status=req.new_status,
        override_reason=req.override_reason,
        override_reason_code=req.override_reason_code,
        supporting_evidence_refs=req.supporting_evidence_refs,
        requires_four_eyes=req.requires_four_eyes,
        officer_id=current_user.id,
        officer_role=current_user.role
    )


@router.post("/manual-overrides/{override_id}/approve", response_model=ManualOverrideResponse)
def approve_manual_override(
    override_id: str,
    req: ManualOverrideApproveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    try:
        return officer_decision_service.approve_manual_override(
            db=db,
            override_id=override_id,
            approver_id=current_user.id,
            approver_role=current_user.role,
            approved=req.approved,
            comments=req.comments
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
