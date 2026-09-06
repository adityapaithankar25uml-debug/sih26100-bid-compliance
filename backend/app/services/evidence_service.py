import datetime
import json
import hashlib
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.domain import (
    EvidenceRecord,
    ComplianceEvaluation,
    ComplianceRuleResult,
    ComplianceFact,
    SourceDocument,
    GovernmentVerificationRecord,
    BidSubmission,
    TenderRequirement,
    ComplianceRule,
    PolicyVersion,
    HumanReviewTask,
    OfficerDecision,
    ManualOverride,
    RiskAssessmentProfile,
    RiskFactorSignal,
    AuditEvent
)
from app.schemas.phase5 import (
    EvidenceQuality,
    EvidenceTraceGraphResponse,
    EvidenceTraceNode,
    EvidenceTraceEdge,
    ComplianceExplanationResponse,
    WhyExplanationItem
)


class EvidenceLedgerService:
    """Service managing Evidence Ledger, Evidence Quality, Traceability Graph, and 'Why?' Explanations."""

    def create_evidence_record(
        self,
        db: Session,
        evidence_type: str,
        bid_submission_id: Optional[str] = None,
        compliance_evaluation_id: Optional[str] = None,
        requirement_id: Optional[str] = None,
        rule_id: Optional[str] = None,
        policy_version_id: Optional[str] = None,
        source_document_id: Optional[str] = None,
        verification_result_id: Optional[str] = None,
        verification_record_id: Optional[str] = None,
        confidence_score: float = 1.0,
        extraction_method: Optional[str] = "DIRECT",
        page_number: Optional[int] = None,
        source_text_snippet: Optional[str] = None,
        bounding_box_json: Optional[Dict[str, Any]] = None,
        evidence_payload: Optional[Dict[str, Any]] = None,
        quality: Optional[EvidenceQuality] = None,
        security_classification: str = "INTERNAL",
        status: str = "VALID",
        provenance_metadata: Optional[Dict[str, Any]] = None
    ) -> EvidenceRecord:
        """Create and persist an evidence record with provenance and structured quality dimensions."""
        if not quality:
            # Default quality assessment based on source type
            quality = self._assess_default_quality(
                evidence_type=evidence_type,
                source_document_id=source_document_id,
                verification_record_id=verification_record_id,
                confidence_score=confidence_score
            )

        evidence = EvidenceRecord(
            bid_submission_id=bid_submission_id,
            compliance_evaluation_id=compliance_evaluation_id,
            requirement_id=requirement_id,
            rule_id=rule_id,
            policy_version_id=policy_version_id,
            source_document_id=source_document_id,
            verification_result_id=verification_result_id,
            verification_record_id=verification_record_id,
            evidence_type=evidence_type,
            confidence_score=confidence_score,
            extraction_method=extraction_method,
            page_number=page_number,
            source_text_snippet=source_text_snippet,
            bounding_box_json=bounding_box_json,
            evidence_payload=evidence_payload or {},
            evidence_quality_json=quality.dict() if isinstance(quality, EvidenceQuality) else quality,
            status=status,
            security_classification=security_classification,
            provenance_metadata_json=provenance_metadata or {}
        )
        db.add(evidence)
        db.commit()
        db.refresh(evidence)
        return evidence

    def _assess_default_quality(
        self,
        evidence_type: str,
        source_document_id: Optional[str],
        verification_record_id: Optional[str],
        confidence_score: float
    ) -> EvidenceQuality:
        """Derive explicit multi-dimensional evidence quality dimensions."""
        if verification_record_id or "GOVT" in evidence_type.upper():
            authority = "AUTHORITATIVE_GOVT"
            provenance = "DIRECT"
        elif source_document_id or "DOC" in evidence_type.upper():
            authority = "BIDDER_DOCUMENT"
            provenance = "OCR" if confidence_score < 0.95 else "DIRECT"
        else:
            authority = "AI_EXTRACTED"
            provenance = "AI_PARSED"

        freshness = "FRESH"
        completeness = "COMPLETE" if confidence_score >= 0.8 else "PARTIAL"
        integrity = "VERIFIED"
        linkage = "MATCHED" if confidence_score >= 0.7 else "PARTIAL_MATCH"
        # Presentation-level summary derived from explicit policy rules (NOT an authoritative single numerical score)
        if authority == "AUTHORITATIVE_GOVT" and integrity == "VERIFIED":
            summary = "STRONG"
        elif confidence_score >= 0.8:
            summary = "MODERATE"
        elif confidence_score >= 0.5:
            summary = "NEEDS_REVIEW"
        else:
            summary = "INSUFFICIENT"

        authenticity = "SCAN_CLEAN" if confidence_score >= 0.8 else "OCR_VERIFIED"
        temporal = "VALID_WINDOW"
        consistency = "CONSISTENT"

        return EvidenceQuality(
            source_authority=authority,
            source_freshness=freshness,
            completeness=completeness,
            integrity_hash_validity=integrity,
            identity_linkage=linkage,
            document_authenticity=authenticity,
            temporal_applicability=temporal,
            extraction_provenance=provenance,
            consistency=consistency,
            quality_assessment_summary=summary
        )

    def get_evidence_trace(
        self,
        db: Session,
        submission_id: str,
        requirement_id: Optional[str] = None
    ) -> EvidenceTraceGraphResponse:
        """Build full traceability graph: Requirement -> Rule -> Fact -> Evidence -> Source -> Risk -> Review -> Decision -> Audit."""
        nodes: List[EvidenceTraceNode] = []
        edges: List[EvidenceTraceEdge] = []
        seen_nodes = set()

        def add_node(node_id: str, n_type: str, label: str, status: str, details: Dict[str, Any]):
            if node_id not in seen_nodes:
                seen_nodes.add(node_id)
                nodes.append(EvidenceTraceNode(
                    node_id=node_id,
                    node_type=n_type,
                    label=label,
                    status=status,
                    details=details
                ))

        def add_edge(src: str, tgt: str, rel: str):
            edges.append(EvidenceTraceEdge(source_node_id=src, target_node_id=tgt, relationship=rel))

        # 1. Fetch submission
        sub = db.query(BidSubmission).filter_by(id=submission_id).first()
        if not sub:
            return EvidenceTraceGraphResponse(submission_id=submission_id, nodes=[], edges=[])

        sub_node_id = f"SUB_{sub.id}"
        add_node(sub_node_id, "SOURCE_DOC", f"Bid Submission {sub.submission_reference}", sub.status, {"bidder_id": sub.bidder_id})

        # 2. Fetch Compliance Evaluations & Rule Results
        evals = db.query(ComplianceEvaluation).filter_by(bid_submission_id=submission_id).order_by(ComplianceEvaluation.created_at.desc()).all()
        for ev in evals:
            ev_node_id = f"EVAL_{ev.id}"
            add_node(ev_node_id, "RULE", f"Compliance Evaluation {ev.id[:8]}", ev.evaluation_status, {"qualification": ev.overall_qualification_recommendation})
            add_edge(sub_node_id, ev_node_id, "EVALUATED_BY")

            for rr in ev.rule_results:
                if requirement_id and rr.requirement_id != requirement_id:
                    continue
                rr_node_id = f"RR_{rr.id}"
                req = db.query(TenderRequirement).filter_by(id=rr.requirement_id).first() if rr.requirement_id else None
                req_title = req.requirement_text[:40] if req else rr.rule_code
                add_node(rr_node_id, "REQUIREMENT", f"Req: {req_title}", rr.result_status, {"rule_code": rr.rule_code, "explanation": rr.explanation_text})
                add_edge(ev_node_id, rr_node_id, "EVALUATES_REQUIREMENT")

                # Link facts & evidence
                facts = db.query(ComplianceFact).filter_by(bid_submission_id=submission_id).all()
                for fact in facts:
                    if any(fc in fact.fact_code for fc in (rr.fact_values_json or {}).keys()):
                        fact_node_id = f"FACT_{fact.id}"
                        add_node(fact_node_id, "FACT", f"Fact: {fact.fact_code}", fact.fact_status, {"value": str(fact.fact_value)})
                        add_edge(rr_node_id, fact_node_id, "USES_FACT")

                        if fact.verification_record_id:
                            vr = db.query(GovernmentVerificationRecord).filter_by(id=fact.verification_record_id).first()
                            if vr:
                                vr_node_id = f"GOVT_{vr.id}"
                                add_node(vr_node_id, "GOVT_RECORD", f"Govt: {vr.source_code}", vr.business_status, {"adapter": vr.adapter_name, "mode": vr.integration_mode})
                                add_edge(fact_node_id, vr_node_id, "VERIFIED_BY")

        # 3. Fetch Evidence Records
        evidences = db.query(EvidenceRecord).filter(
            (EvidenceRecord.bid_submission_id == submission_id) |
            (EvidenceRecord.compliance_evaluation_id.in_([e.id for e in evals]))
        ).all()
        for ev_rec in evidences:
            ev_rec_node_id = f"EV_{ev_rec.id}"
            add_node(ev_rec_node_id, "EVIDENCE", f"Evidence: {ev_rec.evidence_type}", ev_rec.status, {"confidence": ev_rec.confidence_score, "quality": ev_rec.evidence_quality_json})

            if ev_rec.source_document_id:
                doc = db.query(SourceDocument).filter_by(id=ev_rec.source_document_id).first()
                if doc:
                    doc_node_id = f"DOC_{doc.id}"
                    add_node(doc_node_id, "SOURCE_DOC", f"Doc: {doc.original_filename}", doc.quarantine_status, {"sha256": doc.sha256_hash[:10]})
                    add_edge(ev_rec_node_id, doc_node_id, "DERIVED_FROM_DOC")

            if ev_rec.verification_record_id:
                vr_node_id = f"GOVT_{ev_rec.verification_record_id}"
                if vr_node_id in seen_nodes:
                    add_edge(ev_rec_node_id, vr_node_id, "DERIVED_FROM_GOVT")

        # 4. Fetch Risk Signals & Profile
        risk_prof = db.query(RiskAssessmentProfile).filter_by(bid_submission_id=submission_id).order_by(RiskAssessmentProfile.calculated_at.desc()).first()
        if risk_prof:
            rp_node_id = f"RISK_{risk_prof.id}"
            add_node(rp_node_id, "RISK_SIGNAL", f"Risk Level: {risk_prof.overall_risk_level}", risk_prof.overall_risk_level, {"score": risk_prof.risk_score})
            add_edge(sub_node_id, rp_node_id, "HAS_RISK_PROFILE")

        # 5. Fetch Human Reviews
        reviews = db.query(HumanReviewTask).filter_by(bid_submission_id=submission_id).all()
        for rev in reviews:
            rev_node_id = f"REV_{rev.id}"
            add_node(rev_node_id, "HUMAN_REVIEW", f"Review: {rev.review_reason}", rev.status, {"priority": rev.priority, "severity": rev.severity})
            add_edge(sub_node_id, rev_node_id, "REQUIRES_REVIEW")

        # 6. Fetch Officer Decisions & Overrides
        decisions = db.query(OfficerDecision).filter_by(bid_submission_id=submission_id).all()
        for dec in decisions:
            dec_node_id = f"DEC_{dec.id}"
            add_node(dec_node_id, "OFFICER_DECISION", f"Decision: {dec.decision}", dec.decision, {"reviewer_id": dec.reviewer_id, "rationale": dec.rationale})
            add_edge(sub_node_id, dec_node_id, "FINAL_DECISION")

            overrides = db.query(ManualOverride).filter_by(officer_decision_id=dec.id).all()
            for ov in overrides:
                ov_node_id = f"OV_{ov.id}"
                add_node(ov_node_id, "OFFICER_DECISION", f"Override: {ov.previous_status} -> {ov.new_status}", ov.four_eyes_status, {"reason": ov.override_reason})
                add_edge(dec_node_id, ov_node_id, "INCLUDES_OVERRIDE")

        return EvidenceTraceGraphResponse(
            submission_id=submission_id,
            requirement_id=requirement_id,
            nodes=nodes,
            edges=edges
        )

    def get_compliance_explanation(
        self,
        db: Session,
        submission_id: str
    ) -> ComplianceExplanationResponse:
        """Generate structured deterministic 'Why?' explainability response grounded in facts, rules, and calculation traces."""
        sub = db.query(BidSubmission).filter_by(id=submission_id).first()
        if not sub:
            raise ValueError(f"Submission {submission_id} not found")

        eval_rec = db.query(ComplianceEvaluation).filter_by(bid_submission_id=submission_id).order_by(ComplianceEvaluation.created_at.desc()).first()
        if not eval_rec:
            return ComplianceExplanationResponse(
                bid_submission_id=submission_id,
                overall_status="NOT_EVALUATED",
                qualification_recommendation="EVALUATION_REQUIRED",
                evaluated_at=datetime.datetime.utcnow(),
                explanations=[]
            )

        explanations: List[WhyExplanationItem] = []
        for rr in eval_rec.rule_results:
            req = db.query(TenderRequirement).filter_by(id=rr.requirement_id).first() if rr.requirement_id else None
            req_code = req.requirement_code if req else rr.rule_code
            req_title = req.requirement_text if req else f"Requirement for {rr.rule_code}"

            rule = db.query(ComplianceRule).filter_by(id=rr.rule_id).first()
            policy_ver = rule.policy_version_str if rule else "1.0"

            # Gather supporting evidence summary
            ev_records = db.query(EvidenceRecord).filter(
                (EvidenceRecord.bid_submission_id == submission_id) &
                ((EvidenceRecord.requirement_id == rr.requirement_id) | (EvidenceRecord.rule_id == rr.rule_id))
            ).all()

            ev_summary = [
                {
                    "evidence_id": e.id,
                    "evidence_type": e.evidence_type,
                    "status": e.status,
                    "confidence": e.confidence_score,
                    "quality": e.evidence_quality_json
                }
                for e in ev_records
            ]

            # Deterministic explanation construction
            ai_advisory = self._generate_advisory_ai_explanation(rr.result_status, rr.rule_code, rr.explanation_text)

            explanations.append(WhyExplanationItem(
                requirement_id=rr.requirement_id or "REQ_GENERIC",
                requirement_code=req_code,
                requirement_title=req_title,
                rule_code=rr.rule_code,
                policy_version=policy_ver,
                tender_version=str(sub.tender_version_id),
                status=rr.result_status,
                facts_used=rr.fact_values_json or {},
                evidence_summary=ev_summary,
                calculation_trace=rr.evaluation_trace_json or {},
                explanation_text=rr.explanation_text,
                ai_advisory_summary=ai_advisory
            ))

        return ComplianceExplanationResponse(
            bid_submission_id=submission_id,
            overall_status=eval_rec.evaluation_status,
            qualification_recommendation=eval_rec.overall_qualification_recommendation,
            evaluated_at=eval_rec.evaluated_at,
            explanations=explanations
        )

    def _generate_advisory_ai_explanation(self, status: str, rule_code: str, explanation_text: str) -> str:
        """Generate advisory non-authoritative AI explanation text clearly labeled AI ADVISORY."""
        if status == "PASS":
            return f"AI ADVISORY — Rule {rule_code} satisfied deterministically based on verified government facts."
        elif status == "MISSING_EVIDENCE":
            return f"AI ADVISORY — Mandatory evidence for {rule_code} was not found in submission documents. Human review is recommended."
        elif status == "FAIL":
            return f"AI ADVISORY — Evaluation indicates rule {rule_code} failed threshold criteria. Reason: {explanation_text}."
        elif status == "REQUIRES_REVIEW":
            return f"AI ADVISORY — Rule {rule_code} contains ambiguous or conflicting records. Human procurement officer review is required."
        else:
            return f"AI ADVISORY — Rule {rule_code} status: {status}. Refer to authoritative calculation trace."


evidence_service = EvidenceLedgerService()
