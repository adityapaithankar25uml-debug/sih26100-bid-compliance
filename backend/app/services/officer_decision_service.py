import datetime
import json
import hashlib
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.domain import (
    OfficerDecision,
    ManualOverride,
    EvaluationSnapshot,
    BidSubmission,
    ComplianceEvaluation,
    GovernmentVerificationRecord,
    ComplianceFact,
    RiskAssessmentProfile,
    TenderRequirement,
    ComplianceRule,
    User
)
from app.services.audit_service import audit_service


class OfficerDecisionService:
    """Service managing Human Officer Decisions, Non-Destructive Manual Overrides,
    Evaluation Snapshots, and Audit Chain Registration."""

    def create_evaluation_snapshot(
        self,
        db: Session,
        bid_submission_id: str,
        evaluator_id: str = "SYSTEM"
    ) -> EvaluationSnapshot:
        """Construct and persist a point-in-time evaluation snapshot with SHA-256 state hash."""
        sub = db.query(BidSubmission).filter_by(id=bid_submission_id).first()
        if not sub:
            raise ValueError(f"Submission {bid_submission_id} not found")

        eval_rec = db.query(ComplianceEvaluation).filter_by(bid_submission_id=bid_submission_id).order_by(ComplianceEvaluation.created_at.desc()).first()
        gov_recs = db.query(GovernmentVerificationRecord).filter_by(bid_submission_id=bid_submission_id).all()
        facts = db.query(ComplianceFact).filter_by(bid_submission_id=bid_submission_id).all()
        risk_prof = db.query(RiskAssessmentProfile).filter_by(bid_submission_id=bid_submission_id).order_by(RiskAssessmentProfile.calculated_at.desc()).first()

        snapshot_payload = {
            "submission_id": sub.id,
            "submission_reference": sub.submission_reference,
            "bidder_id": sub.bidder_id,
            "tender_id": sub.tender_id,
            "tender_version_id": sub.tender_version_id,
            "evaluation_status": eval_rec.evaluation_status if eval_rec else "NOT_EVALUATED",
            "qualification_recommendation": eval_rec.overall_qualification_recommendation if eval_rec else "NONE",
            "evaluated_at": eval_rec.evaluated_at.isoformat() if eval_rec else datetime.datetime.utcnow().isoformat(),
            "rule_results": [
                {
                    "rule_code": rr.rule_code,
                    "requirement_id": rr.requirement_id,
                    "result_status": rr.result_status,
                    "explanation": rr.explanation_text,
                    "fact_values": rr.fact_values_json
                }
                for rr in (eval_rec.rule_results if eval_rec else [])
            ],
            "government_verifications": [
                {
                    "source_code": g.source_code,
                    "adapter_name": g.adapter_name,
                    "integration_mode": g.integration_mode,
                    "technical_status": g.technical_status,
                    "business_status": g.business_status,
                    "identity_match_status": g.identity_match_status
                }
                for g in gov_recs
            ],
            "facts": [
                {
                    "fact_code": f.fact_code,
                    "fact_value": f.fact_value,
                    "fact_status": f.fact_status,
                    "provenance": f.provenance_ref
                }
                for f in facts
            ],
            "risk_profile": {
                "overall_risk_level": risk_prof.overall_risk_level if risk_prof else "LOW",
                "risk_score": risk_prof.risk_score if risk_prof else 0.0,
                "signal_count": len(risk_prof.signals) if risk_prof else 0
            }
        }

        canonical_json = json.dumps(snapshot_payload, sort_keys=True, separators=(",", ":"))
        snapshot_hash = hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

        snapshot = EvaluationSnapshot(
            bid_submission_id=bid_submission_id,
            tender_version_id=sub.tender_version_id,
            evaluation_id=eval_rec.id if eval_rec else None,
            snapshot_data_json=snapshot_payload,
            snapshot_hash=snapshot_hash,
            created_at=datetime.datetime.utcnow()
        )
        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

        # Append to Audit Chain
        audit_service.log_event(
            db=db,
            actor_id=evaluator_id,
            actor_role="System",
            action="EVALUATION_SNAPSHOT_CREATED",
            resource_type="EvaluationSnapshot",
            resource_id=snapshot.id,
            payload={"submission_id": bid_submission_id, "snapshot_hash": snapshot_hash}
        )

        return snapshot

    def record_officer_decision(
        self,
        db: Session,
        bid_submission_id: str,
        reviewer_id: str,
        reviewer_role: str,
        decision: str,
        rationale: str,
        overrides_data: Optional[List[Dict[str, Any]]] = None
    ) -> OfficerDecision:
        """Record formal human officer decision (QUALIFIED, DISQUALIFIED, etc.) and non-destructive overrides."""
        sub = db.query(BidSubmission).filter_by(id=bid_submission_id).first()
        if not sub:
            raise ValueError(f"Submission {bid_submission_id} not found")

        # 1. Take evaluation snapshot
        snapshot = self.create_evaluation_snapshot(db, bid_submission_id, evaluator_id=reviewer_id)

        # 2. Fetch risk profile
        risk_prof = db.query(RiskAssessmentProfile).filter_by(bid_submission_id=bid_submission_id).order_by(RiskAssessmentProfile.calculated_at.desc()).first()

        # 3. Create Officer Decision record
        off_decision = OfficerDecision(
            bid_submission_id=bid_submission_id,
            reviewer_id=reviewer_id,
            tender_id=sub.tender_id,
            tender_version_id=sub.tender_version_id,
            bidder_id=sub.bidder_id,
            decision=decision,
            rationale=rationale,
            evaluation_snapshot_id=snapshot.id,
            risk_profile_id=risk_prof.id if risk_prof else None,
            decision_timestamp=datetime.datetime.utcnow()
        )
        db.add(off_decision)
        db.commit()
        db.refresh(off_decision)

        # Update submission status accordingly
        sub.status = decision
        db.commit()

        # 4. Handle Manual Overrides if requested
        if overrides_data:
            for ov_item in overrides_data:
                self.create_manual_override(
                    db=db,
                    officer_decision_id=off_decision.id,
                    bid_submission_id=bid_submission_id,
                    requirement_id=ov_item["requirement_id"],
                    rule_id=ov_item.get("rule_id"),
                    previous_status=ov_item["previous_status"],
                    new_status=ov_item["new_status"],
                    override_reason=ov_item["override_reason"],
                    override_reason_code=ov_item.get("override_reason_code", "OFFICER_REVIEW"),
                    supporting_evidence_refs=ov_item.get("supporting_evidence_refs"),
                    requires_four_eyes=ov_item.get("requires_four_eyes", False),
                    officer_id=reviewer_id,
                    officer_role=reviewer_role
                )

        # 5. Append Audit Event for Officer Decision
        audit_event = audit_service.log_event(
            db=db,
            actor_id=reviewer_id,
            actor_role=reviewer_role,
            action="OFFICER_DECISION_CREATED",
            resource_type="OfficerDecision",
            resource_id=off_decision.id,
            payload={
                "submission_id": bid_submission_id,
                "decision": decision,
                "rationale": rationale,
                "snapshot_id": snapshot.id
            }
        )
        off_decision.audit_event_id = audit_event.id
        db.commit()
        db.refresh(off_decision)

        return off_decision

    def create_manual_override(
        self,
        db: Session,
        officer_decision_id: str,
        bid_submission_id: str,
        requirement_id: str,
        previous_status: str,
        new_status: str,
        override_reason: str,
        rule_id: Optional[str] = None,
        override_reason_code: str = "OFFICER_REVIEW",
        supporting_evidence_refs: Optional[List[str]] = None,
        requires_four_eyes: bool = False,
        officer_id: str = "SYSTEM",
        officer_role: str = "ProcurementOfficer"
    ) -> ManualOverride:
        """Record non-destructive manual override preserving original deterministic evaluation."""
        four_eyes_status = "PENDING_APPROVAL" if requires_four_eyes else "APPROVED"

        override = ManualOverride(
            officer_decision_id=officer_decision_id,
            bid_submission_id=bid_submission_id,
            requirement_id=requirement_id,
            rule_id=rule_id,
            previous_status=previous_status,
            new_status=new_status,
            override_reason_code=override_reason_code,
            override_reason=override_reason,
            supporting_evidence_refs_json=supporting_evidence_refs or [],
            requires_four_eyes=requires_four_eyes,
            approved_by_officer_id=officer_id if not requires_four_eyes else None,
            four_eyes_status=four_eyes_status
        )
        db.add(override)
        db.commit()
        db.refresh(override)

        # Audit Event for Manual Override
        audit_service.log_event(
            db=db,
            actor_id=officer_id,
            actor_role=officer_role,
            action="MANUAL_OVERRIDE_CREATED",
            resource_type="ManualOverride",
            resource_id=override.id,
            payload={
                "submission_id": bid_submission_id,
                "requirement_id": requirement_id,
                "previous_status": previous_status,
                "new_status": new_status,
                "reason_code": override_reason_code,
                "four_eyes_status": four_eyes_status
            }
        )
        return override

    def approve_manual_override(
        self,
        db: Session,
        override_id: str,
        approver_id: str,
        approver_role: str,
        approved: bool,
        comments: Optional[str] = None
    ) -> ManualOverride:
        """Process four-eyes approval by Officer B."""
        override = db.query(ManualOverride).filter_by(id=override_id).first()
        if not override:
            raise ValueError(f"Manual override {override_id} not found")

        if override.four_eyes_status != "PENDING_APPROVAL":
            raise ValueError(f"Override {override_id} is not pending four-eyes approval")

        if override.officer_decision and override.officer_decision.reviewer_id == approver_id:
            raise ValueError("Four-eyes policy violation: Overriding officer cannot self-approve their own override request.")

        override.approved_by_officer_id = approver_id
        override.four_eyes_status = "APPROVED" if approved else "REJECTED"
        db.commit()
        db.refresh(override)

        # Audit Event
        audit_service.log_event(
            db=db,
            actor_id=approver_id,
            actor_role=approver_role,
            action="MANUAL_OVERRIDE_APPROVED" if approved else "MANUAL_OVERRIDE_REJECTED",
            resource_type="ManualOverride",
            resource_id=override.id,
            payload={
                "override_id": override_id,
                "approved": approved,
                "comments": comments
            }
        )
        return override


officer_decision_service = OfficerDecisionService()
