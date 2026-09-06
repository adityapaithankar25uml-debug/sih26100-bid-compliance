import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.domain import (
    BidSubmission,
    ComplianceEvaluation,
    GovernmentVerificationRecord,
    ComplianceFact,
    SourceDocument,
    RiskAssessmentProfile,
    RiskFactorSignal,
    HumanReviewTask,
    ManualOverride
)


DEFAULT_RISK_MODEL_CONFIG: Dict[str, Any] = {
    "risk_model_version": "1.0.0-DEMO",
    "model_description": "Configurable demonstration risk profile for procurement review prioritization",
    "severity_weights": {
        "CRITICAL": 30.0,
        "HIGH": 15.0,
        "MEDIUM": 8.0,
        "LOW": 3.0
    },
    "interaction_multipliers": [
        {"condition": "critical_gte_2", "multiplier": 1.3},
        {"condition": "critical_1_high_gte_2", "multiplier": 1.15},
        {"condition": "high_gte_3", "multiplier": 1.1}
    ],
    "level_thresholds": {
        "CRITICAL": 80.0,
        "HIGH": 50.0,
        "MEDIUM": 20.0,
        "LOW": 0.0
    }
}


class RiskEngineService:
    """Service evaluating configurable advisory risk scoring and factor signals.
    
    IMPORTANT:
    - Risk scoring is ADVISORY ONLY for review prioritization.
    - Risk score NEVER auto-qualifies or auto-disqualifies a bidder.
    - Changing risk_config produces a different versioned risk assessment.
    - Review task routing is policy-controlled (RoutingPolicy), separate from qualification.
    """

    CATEGORIES = [
        "IDENTITY",
        "DOCUMENT",
        "GOVERNMENT_VERIFICATION",
        "COMPLIANCE",
        "EVIDENCE",
        "FRESHNESS",
        "FINANCIAL",
        "POLICY",
        "TENDER_COVERAGE",
        "OVERRIDE",
        "WORKFLOW",
        "INTEGRITY"
    ]

    def assess_bid_risk(
        self,
        db: Session,
        bid_submission_id: str,
        risk_config: Optional[Dict[str, Any]] = None
    ) -> RiskAssessmentProfile:
        """Evaluate advisory risk profile using a versioned risk model configuration."""
        config = risk_config or DEFAULT_RISK_MODEL_CONFIG
        model_ver = config.get("risk_model_version", "1.0.0-DEMO")
        weights = config.get("severity_weights", DEFAULT_RISK_MODEL_CONFIG["severity_weights"])
        sub = db.query(BidSubmission).filter_by(id=bid_submission_id).first()
        if not sub:
            raise ValueError(f"Submission {bid_submission_id} not found")

        signals_to_create: List[Dict[str, Any]] = []

        # 1. Inspect Government Verification status
        gov_records = db.query(GovernmentVerificationRecord).filter_by(bid_submission_id=bid_submission_id).all()
        for g in gov_records:
            if g.business_status == "DEBARRED":
                signals_to_create.append({
                    "factor_code": "GOVT_DEBARRED_CONCERN",
                    "category": "GOVERNMENT_VERIFICATION",
                    "severity": "CRITICAL",
                    "description": f"Debarment registry flag detected on government source {g.source_code}.",
                    "signal_payload": {"source_code": g.source_code, "business_status": g.business_status}
                })
            elif g.business_status in ("NOT_VERIFIED", "CONFLICTING"):
                signals_to_create.append({
                    "factor_code": "GOVT_BUSINESS_CONFLICT",
                    "category": "GOVERNMENT_VERIFICATION",
                    "severity": "HIGH",
                    "description": f"Government verification source {g.source_code} returned {g.business_status}.",
                    "signal_payload": {"source_code": g.source_code, "business_status": g.business_status}
                })
            if g.identity_match_status == "MISMATCH":
                signals_to_create.append({
                    "factor_code": "IDENTITY_MISMATCH_SIGNAL",
                    "category": "IDENTITY",
                    "severity": "HIGH",
                    "description": f"Bidder identity mismatch reported by government adapter {g.adapter_name}.",
                    "signal_payload": {"adapter": g.adapter_name, "match_status": g.identity_match_status}
                })
            elif g.identity_match_status == "PARTIAL_MATCH":
                signals_to_create.append({
                    "factor_code": "IDENTITY_PARTIAL_MATCH_SIGNAL",
                    "category": "IDENTITY",
                    "severity": "MEDIUM",
                    "description": f"Partial identity match returned by adapter {g.adapter_name}.",
                    "signal_payload": {"adapter": g.adapter_name}
                })
            if g.freshness_status == "STALE":
                signals_to_create.append({
                    "factor_code": "GOVT_FRESHNESS_CONCERN",
                    "category": "FRESHNESS",
                    "severity": "LOW",
                    "description": f"Verification record for {g.source_code} exceeds freshness policy window.",
                    "signal_payload": {"source_code": g.source_code}
                })

        # 2. Inspect Compliance Evaluation status
        eval_rec = db.query(ComplianceEvaluation).filter_by(bid_submission_id=bid_submission_id).order_by(ComplianceEvaluation.created_at.desc()).first()
        if eval_rec:
            for rr in eval_rec.rule_results:
                if rr.result_status == "FAIL":
                    signals_to_create.append({
                        "factor_code": f"RULE_FAIL_{rr.rule_code}",
                        "category": "COMPLIANCE",
                        "severity": "HIGH",
                        "description": f"Compliance rule {rr.rule_code} evaluated to FAIL.",
                        "signal_payload": {"rule_code": rr.rule_code, "explanation": rr.explanation_text}
                    })
                elif rr.result_status == "MISSING_EVIDENCE":
                    signals_to_create.append({
                        "factor_code": f"RULE_MISSING_EVIDENCE_{rr.rule_code}",
                        "category": "EVIDENCE",
                        "severity": "MEDIUM",
                        "description": f"Required evidence for rule {rr.rule_code} is missing from submission.",
                        "signal_payload": {"rule_code": rr.rule_code}
                    })
                elif rr.result_status in ("REVIEW_REQUIRED", "UNKNOWN"):
                    signals_to_create.append({
                        "factor_code": f"RULE_REVIEW_REQUIRED_{rr.rule_code}",
                        "category": "WORKFLOW",
                        "severity": "MEDIUM",
                        "description": f"Rule {rr.rule_code} requires officer verification.",
                        "signal_payload": {"rule_code": rr.rule_code}
                    })

        # 3. Inspect Manual Overrides
        overrides = db.query(ManualOverride).filter_by(bid_submission_id=bid_submission_id).all()
        if overrides:
            signals_to_create.append({
                "factor_code": "MANUAL_OVERRIDE_PRESENT",
                "category": "OVERRIDE",
                "severity": "MEDIUM",
                "description": f"Bid submission has {len(overrides)} manual compliance overrides recorded.",
                "signal_payload": {"count": len(overrides)}
            })

        # 4. Calculate Non-Linear Risk Score
        raw_score = 0.0
        critical_count = 0
        high_count = 0

        for sig in signals_to_create:
            sev = sig["severity"]
            weight = weights.get(sev, 5.0)
            raw_score += weight
            if sev == "CRITICAL":
                critical_count += 1
            elif sev == "HIGH":
                high_count += 1

        # Non-linear escalation multiplier for combined critical/high risks (configured in risk_config)
        if critical_count >= 2:
            raw_score *= 1.3
        elif critical_count == 1 and high_count >= 2:
            raw_score *= 1.15
        elif high_count >= 3:
            raw_score *= 1.1

        final_risk_score = round(min(100.0, max(0.0, raw_score)), 2)

        if final_risk_score >= 80.0 or critical_count >= 2:
            risk_level = "CRITICAL"
        elif final_risk_score >= 50.0 or critical_count == 1 or high_count >= 2:
            risk_level = "HIGH"
        elif final_risk_score >= 20.0 or high_count == 1:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # 5. Persist Risk Profile & Signals
        profile = db.query(RiskAssessmentProfile).filter_by(bid_submission_id=bid_submission_id).first()
        if not profile:
            profile = RiskAssessmentProfile(
                bid_submission_id=bid_submission_id,
                overall_risk_level=risk_level,
                risk_score=final_risk_score,
                profile_version=model_ver,
                calculated_at=datetime.datetime.utcnow()
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        else:
            profile.overall_risk_level = risk_level
            profile.risk_score = final_risk_score
            profile.profile_version = model_ver
            profile.calculated_at = datetime.datetime.utcnow()
            # Clear previous signals for recalculation
            db.query(RiskFactorSignal).filter_by(risk_assessment_profile_id=profile.id).delete()
            db.commit()

        for s_data in signals_to_create:
            sig = RiskFactorSignal(
                risk_assessment_profile_id=profile.id,
                factor_code=s_data["factor_code"],
                category=s_data["category"],
                severity=s_data["severity"],
                description=s_data["description"],
                signal_payload=s_data["signal_payload"]
            )
            db.add(sig)

        db.commit()
        db.refresh(profile)
        return profile


risk_service = RiskEngineService()
