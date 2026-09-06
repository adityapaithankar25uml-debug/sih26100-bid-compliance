import datetime
from sqlalchemy.orm import Session

from app.models.domain import (
    BidSubmission,
    ComplianceEvaluation,
    EvidenceRecord,
    HumanReviewTask,
    RiskAssessmentProfile,
    RiskFactorSignal,
    TenderRequirement,
    ComplianceRule
)
from app.services.evidence_service import evidence_service
from app.services.risk_service import risk_service
from app.services.review_service import review_service


def seed_phase5_workspace(db: Session, submission_id: str = "SUB_01") -> None:
    """Seed Phase 5 evidence, risk profile, and human review tasks for a demo submission if not already present."""
    sub = db.query(BidSubmission).filter_by(id=submission_id).first()
    if not sub:
        return

    # Seed Evidence Records if missing
    existing_ev = db.query(EvidenceRecord).filter_by(bid_submission_id=submission_id).first()
    if not existing_ev:
        eval_rec = db.query(ComplianceEvaluation).filter_by(bid_submission_id=submission_id).first()
        reqs = db.query(TenderRequirement).all()

        for req in reqs:
            evidence_service.create_evidence_record(
                db=db,
                evidence_type=f"CERTIFICATE_{req.requirement_code}",
                bid_submission_id=submission_id,
                compliance_evaluation_id=eval_rec.id if eval_rec else None,
                requirement_id=req.id,
                confidence_score=0.98,
                extraction_method="DIRECT",
                page_number=1,
                source_text_snippet=f"Verified compliance documentation for {req.requirement_code}",
                security_classification="INTERNAL",
                status="VALID"
            )

    # Seed Risk Profile if missing
    existing_risk = db.query(RiskAssessmentProfile).filter_by(bid_submission_id=submission_id).first()
    if not existing_risk:
        risk_service.assess_bid_risk(db, submission_id)

    # Seed Human Review Task if missing
    existing_rev = db.query(HumanReviewTask).filter_by(bid_submission_id=submission_id).first()
    if not existing_rev:
        review_service.create_review_task(
            db=db,
            bid_submission_id=submission_id,
            review_reason="Conflicting identity details detected between GST portal and bid proposal document.",
            severity="HIGH",
            priority="HIGH",
            suggested_action="Review legal entity name alignment across GST certificate and uploaded PAN card.",
            evidence_refs=["EV_GST_01", "EV_DOC_PAN_01"]
        )
