from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
import datetime

from app.db.session import get_db
from app.api.v1.deps import get_current_user, require_roles
from app.models.domain import (
    User,
    GovernmentSourceRegistry,
    GovernmentVerificationRecord,
    ComplianceRule,
    PolicyVersion,
    ComplianceEvaluation,
    ComplianceRuleResult,
    HumanReviewTask,
    BidSubmission,
    Tender,
    TenderRequirement
)
from app.services.government_adapters import adapter_registry
from app.services.verification_service import verification_service
from app.services.compliance_engine import compliance_engine
from app.services.compliance_seed import seed_phase4_compliance_framework
from app.schemas.verification_compliance import (
    GovernmentSourceResponse,
    VerificationRequest,
    VerificationRecordResponse,
    ManualVerificationRequest,
    ComplianceRuleResponse,
    PolicyVersionResponse,
    ComplianceEvaluationResponse,
    ComplianceMatrixResponse,
    ComplianceMatrixItem,
    HumanReviewTaskResponse,
    HumanReviewDecisionRequest
)

router = APIRouter()


@router.get("/government-sources", response_model=List[GovernmentSourceResponse])
def list_government_sources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    seed_phase4_compliance_framework(db)
    sources = db.query(GovernmentSourceRegistry).filter_by(enabled=True).all()
    return sources


@router.post("/government-verifications", response_model=VerificationRecordResponse, status_code=status.HTTP_201_CREATED)
def trigger_government_verification(
    req: VerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin", "ServiceWorker"]))
):
    submission = db.query(BidSubmission).filter_by(id=req.bid_submission_id).first()
    context = {"legal_name": submission.bidder.legal_name} if submission and submission.bidder else None

    rec = verification_service.execute_verification(
        db=db,
        bid_submission_id=req.bid_submission_id,
        source_code=req.source_code,
        identifier_value=req.identifier_value,
        bidder_context=context,
        actor_id=current_user.id
    )
    return rec


@router.post("/government-verifications/manual", response_model=VerificationRecordResponse, status_code=status.HTTP_201_CREATED)
def record_manual_verification_fallback(
    req: ManualVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    rec = verification_service.manual_fallback(
        db=db,
        bid_submission_id=req.bid_submission_id,
        source_code=req.source_code,
        business_status=req.business_status,
        manual_notes=req.manual_notes,
        officer_id=current_user.id,
        manual_evidence_ref=req.manual_evidence_ref,
        normalized_facts=req.normalized_facts
    )
    return rec


@router.get("/government-verifications/{record_id}", response_model=VerificationRecordResponse)
def get_verification_record(
    record_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rec = db.query(GovernmentVerificationRecord).filter_by(id=record_id).first()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Verification record not found")
    return rec


@router.get("/bids/{submission_id}/verifications", response_model=List[VerificationRecordResponse])
def list_bid_verifications(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recs = db.query(GovernmentVerificationRecord).filter_by(bid_submission_id=submission_id).all()
    return recs


@router.post("/bids/{submission_id}/evaluate-compliance", response_model=ComplianceEvaluationResponse)
def evaluate_bid_compliance(
    submission_id: str,
    tender_id: Optional[str] = None,
    tender_version_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin", "ServiceWorker"]))
):
    seed_phase4_compliance_framework(db)
    sub = db.query(BidSubmission).filter_by(id=submission_id).first()
    t_id = tender_id or (sub.tender_id if sub else "TEN_01")
    tv_id = tender_version_id or "TV_01"

    eval_rec = compliance_engine.evaluate_bid_submission(
        db=db,
        bid_submission_id=submission_id,
        tender_id=t_id,
        tender_version_id=tv_id,
        evaluator_id=current_user.id
    )
    return eval_rec


@router.get("/bids/{submission_id}/compliance-matrix", response_model=ComplianceMatrixResponse)
def get_bid_compliance_matrix(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    seed_phase4_compliance_framework(db)
    sub = db.query(BidSubmission).filter_by(id=submission_id).first()
    t_id = sub.tender_id if sub else "TEN_01"

    # Fetch latest evaluation or execute on the fly
    eval_rec = db.query(ComplianceEvaluation).filter_by(bid_submission_id=submission_id).order_by(ComplianceEvaluation.created_at.desc()).first()
    if not eval_rec:
        eval_rec = compliance_engine.evaluate_bid_submission(db, submission_id, t_id, "TV_01", evaluator_id=current_user.id)

    matrix_items = []
    for rr in eval_rec.rule_results:
        rule = db.query(ComplianceRule).filter_by(id=rr.rule_id).first()
        r_name = rule.name if rule else rr.rule_code
        r_type = rule.rule_type if rule else "RULE"

        req = db.query(TenderRequirement).filter_by(id=rr.requirement_id).first() if rr.requirement_id else None
        req_title = req.title if req else f"Requirement for {rr.rule_code}"
        req_code = req.code if req else rr.rule_code

        # Extract primary fact and source
        fact_values = rr.fact_values_json or {}
        first_fact_code = list(fact_values.keys())[0] if fact_values else None
        first_fact_val = fact_values.get(first_fact_code) if first_fact_code else None

        source_code = first_fact_code.split("_")[0] if first_fact_code and "_" in first_fact_code else "SYSTEM"
        ev_ref = rr.evidence_refs_json[0] if rr.evidence_refs_json else None

        matrix_items.append(ComplianceMatrixItem(
            requirement_id=rr.requirement_id or "REQ_GENERIC",
            requirement_code=req_code,
            requirement_title=req_title,
            category=r_type,
            rule_code=rr.rule_code,
            rule_name=r_name,
            fact_code=first_fact_code,
            fact_value=first_fact_val,
            fact_status="VERIFIED" if rr.result_status == "PASS" else "UNVERIFIED",
            source_code=source_code,
            verification_status="VERIFIED" if rr.result_status == "PASS" else "NOT_VERIFIED",
            compliance_status=rr.result_status,
            evidence_ref=ev_ref,
            explanation=rr.explanation_text
        ))

    return ComplianceMatrixResponse(
        bid_submission_id=submission_id,
        tender_id=t_id,
        overall_status=eval_rec.evaluation_status,
        qualification_recommendation=eval_rec.overall_qualification_recommendation,
        matrix_items=matrix_items
    )


@router.get("/compliance/rules", response_model=List[ComplianceRuleResponse])
def list_compliance_rules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    seed_phase4_compliance_framework(db)
    rules = db.query(ComplianceRule).filter_by(enabled=True).all()
    return rules


@router.get("/compliance/policies", response_model=List[PolicyVersionResponse])
def list_policy_versions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    seed_phase4_compliance_framework(db)
    policies = db.query(PolicyVersion).all()
    return policies


@router.get("/human-review-tasks", response_model=List[HumanReviewTaskResponse])
def list_human_review_tasks(
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    q = db.query(HumanReviewTask)
    if status_filter:
        q = q.filter_by(status=status_filter)
    tasks = q.order_by(HumanReviewTask.created_at.desc()).all()
    return tasks


@router.post("/human-review-tasks/{task_id}/decision", response_model=HumanReviewTaskResponse)
def record_human_review_decision(
    task_id: str,
    req: HumanReviewDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "ComplianceOfficer", "SystemAdmin"]))
):
    task = db.query(HumanReviewTask).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Human review task not found")

    task.status = "RESOLVED" if req.decision in ("APPROVED", "OVERRIDDEN") else "REJECTED"
    task.decision = req.decision
    task.comments = req.comments
    task.assigned_officer_id = current_user.id
    task.decided_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(task)
    return task
