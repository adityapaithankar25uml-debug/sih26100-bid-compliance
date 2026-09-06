import pytest
import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.domain import (
    User,
    Bidder,
    Tender,
    TenderVersion,
    TenderRequirement,
    ComplianceRule,
    ComplianceRuleResult,
    BidSubmission,
    ComplianceEvaluation,
    EvidenceRecord,
    RiskAssessmentProfile,
    HumanReviewTask,
    OfficerDecision,
    ManualOverride,
    EvaluationSnapshot,
    AuditEvent,
    AuditHashChainBlock
)
from app.services.evidence_service import evidence_service
from app.services.risk_service import risk_service
from app.services.review_service import review_service
from app.services.officer_decision_service import officer_decision_service
from app.services.compliance_seed import seed_phase4_compliance_framework
from app.services.audit_service import audit_service
from app.core.security import create_access_token, get_password_hash


@pytest.fixture
def setup_phase5_data(db: Session):
    seed_phase4_compliance_framework(db)

    # 1. Create Bidder
    bidder = Bidder(
        bidder_name="Apex Energy Technologies Pvt Ltd",
        registration_number="REG_APEX_9988",
        entity_type="PRIVATE_LIMITED",
        organization_type="MSE"
    )
    db.add(bidder)
    db.commit()

    # 2. Create Tender & Version
    tender = Tender(
        tender_number="TEN_PHASE5_001",
        title="Procurement of High-Pressure Valves for Refinery Operation",
        organization="CPCL",
        status="PUBLISHED"
    )
    db.add(tender)
    db.commit()

    t_version = TenderVersion(
        tender_id=tender.id,
        version_number=1,
        description="Phase 5 Test Tender Version",
        is_finalized=True
    )
    db.add(t_version)
    db.commit()

    # 3. Create Tender Requirement
    req = TenderRequirement(
        tender_version_id=t_version.id,
        requirement_code="REQ_GST_01",
        category="TECHNICAL",
        requirement_text="Bidder must possess active GST registration certificate.",
        is_mandatory=True
    )
    db.add(req)
    db.commit()

    # 4. Create Bid Submission
    sub = BidSubmission(
        bidder_id=bidder.id,
        tender_id=tender.id,
        tender_version_id=t_version.id,
        submission_reference="SUB_PHASE5_9901",
        status="SUBMITTED"
    )
    db.add(sub)
    db.commit()

    # 5. Create Compliance Evaluation & Rule Results
    eval_rec = ComplianceEvaluation(
        bid_submission_id=sub.id,
        tender_id=tender.id,
        tender_version_id=t_version.id,
        status="REQUIRES_HUMAN_REVIEW",
        evaluation_status="REQUIRES_REVIEW",
        overall_qualification_recommendation="HUMAN_OFFICER_REVIEW_REQUIRED",
        evaluation_result_json={"passed_rules": 2, "failed_rules": 0, "missing_evidence_rules": 1},
        evaluation_trace_json={"trace": "Phase 5 Test Evaluation Trace"},
        evaluator_id="SYSTEM"
    )
    db.add(eval_rec)
    db.commit()

    rule = db.query(ComplianceRule).filter_by(rule_code="RULE_GST_ACTIVE").first()
    if not rule:
        rule = ComplianceRule(
            rule_code="RULE_GST_ACTIVE",
            name="GST Active Registration Rule",
            rule_type="BOOLEAN_FACT",
            version="1.0",
            policy_code="POL_GEM_COMPLIANCE_2026",
            policy_version="1.0",
            severity="MANDATORY",
            evaluation_expression_json={"operator": "==", "left": {"type": "fact", "name": "GST_GST_STATUS"}, "right": "ACTIVE"},
            required_facts_json=["GST_GST_STATUS"],
            explanation_template="GST registration status must be ACTIVE"
        )
        db.add(rule)
        db.commit()

    rr = ComplianceRuleResult(
        evaluation_id=eval_rec.id,
        rule_id=rule.id,
        rule_code=rule.rule_code,
        requirement_id=req.id,
        result_status="PASS",
        evaluation_trace_json={"trace": "Rule passed"},
        explanation_text="GST registration is active.",
        fact_values_json={"GST_GST_STATUS": "ACTIVE"},
        evidence_refs_json=["EV_GST_01"]
    )
    db.add(rr)
    db.commit()

    return {
        "bidder": bidder,
        "tender": tender,
        "tender_version": t_version,
        "requirement": req,
        "submission": sub,
        "evaluation": eval_rec
    }



def test_evidence_creation_and_quality_assessment(db: Session, setup_phase5_data):
    sub = setup_phase5_data["submission"]
    eval_rec = setup_phase5_data["evaluation"]

    ev = evidence_service.create_evidence_record(
        db=db,
        evidence_type="GST_CERTIFICATE_EXTRACT",
        bid_submission_id=sub.id,
        compliance_evaluation_id=eval_rec.id,
        confidence_score=0.92,
        extraction_method="OCR_PADDLE",
        source_text_snippet="GSTIN: 33AAAAA0000A1Z5 Status: Active",
        status="VALID"
    )

    assert ev.id is not None
    assert ev.evidence_type == "GST_CERTIFICATE_EXTRACT"
    assert ev.confidence_score == 0.92
    assert ev.evidence_quality_json is not None
    assert ev.evidence_quality_json["source_authority"] == "AI_EXTRACTED"
    assert ev.evidence_quality_json["quality_assessment_summary"] == "MODERATE"


def test_evidence_traceability_graph(db: Session, setup_phase5_data):
    sub = setup_phase5_data["submission"]
    req = setup_phase5_data["requirement"]

    # Add evidence
    evidence_service.create_evidence_record(
        db=db,
        evidence_type="GOVT_GST_RECORD",
        bid_submission_id=sub.id,
        requirement_id=req.id,
        confidence_score=1.0,
        status="VALID"
    )

    trace = evidence_service.get_evidence_trace(db, submission_id=sub.id, requirement_id=req.id)
    assert trace.submission_id == sub.id
    assert len(trace.nodes) >= 2
    assert any(n.node_type == "REQUIREMENT" for n in trace.nodes)
    assert any(n.node_type == "EVIDENCE" for n in trace.nodes)


def test_compliance_explanation_why_view(db: Session, setup_phase5_data):
    sub = setup_phase5_data["submission"]

    exp_response = evidence_service.get_compliance_explanation(db, submission_id=sub.id)
    assert exp_response.bid_submission_id == sub.id
    assert exp_response.overall_status == "REQUIRES_REVIEW"
    assert exp_response.qualification_recommendation == "HUMAN_OFFICER_REVIEW_REQUIRED"


def test_advisory_risk_scoring_and_signals(db: Session, setup_phase5_data):
    sub = setup_phase5_data["submission"]

    prof = risk_service.assess_bid_risk(db, bid_submission_id=sub.id)
    assert prof.id is not None
    assert prof.bid_submission_id == sub.id
    assert prof.overall_risk_level in ("LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert 0.0 <= prof.risk_score <= 100.0

    # Verify Risk is ADVISORY ONLY (Submission status is NOT automatically altered by risk calculation)
    updated_sub = db.query(BidSubmission).filter_by(id=sub.id).first()
    assert updated_sub.status == "SUBMITTED"


def test_human_review_workspace_workflow(db: Session, setup_phase5_data):
    sub = setup_phase5_data["submission"]

    # 1. Create task
    task = review_service.create_review_task(
        db=db,
        bid_submission_id=sub.id,
        review_reason="Mismatch in turnover figures between CA Certificate and GST portal.",
        severity="HIGH",
        priority="HIGH"
    )
    assert task.id is not None
    assert task.status == "PENDING"

    # 2. List tasks
    pending_tasks = review_service.list_review_tasks(db, status_filter="PENDING")
    assert len(pending_tasks) >= 1

    # 3. Assign task
    review_service.assign_review_task(db, task_id=task.id, officer_id="OFFICER_001")
    assert task.status == "IN_REVIEW"
    assert task.assigned_officer_id == "OFFICER_001"

    # 4. Resolve task
    review_service.resolve_review_task(
        db=db,
        task_id=task.id,
        officer_id="OFFICER_001",
        decision="APPROVED",
        resolution_summary="CA audited financial statement verified. Figure discrepancy reconciled."
    )
    assert task.status == "RESOLVED"
    assert task.decision == "APPROVED"


def test_officer_decision_and_non_destructive_manual_override(db: Session, setup_phase5_data):
    sub = setup_phase5_data["submission"]
    req = setup_phase5_data["requirement"]

    # 1. Record Officer Decision with manual override
    off_decision = officer_decision_service.record_officer_decision(
        db=db,
        bid_submission_id=sub.id,
        reviewer_id="OFFICER_007",
        reviewer_role="ProcurementOfficer",
        decision="QUALIFIED",
        rationale="Bidder satisfied all technical requirements upon officer verification.",
        overrides_data=[{
            "requirement_id": req.id,
            "previous_status": "MISSING_EVIDENCE",
            "new_status": "PASS",
            "override_reason_code": "NEW_EVIDENCE",
            "override_reason": "Hardcopy CA certificate presented during pre-bid review meeting.",
            "requires_four_eyes": False
        }]
    )

    assert off_decision.id is not None
    assert off_decision.decision == "QUALIFIED"
    assert len(off_decision.overrides) == 1
    assert off_decision.evaluation_snapshot_id is not None

    # Verify Non-Destructive Override (Original evaluation history is preserved)
    eval_rec = db.query(ComplianceEvaluation).filter_by(bid_submission_id=sub.id).first()
    assert eval_rec.evaluation_status == "REQUIRES_REVIEW" # Original evaluation status intact!

    # Verify Evaluation Snapshot was created
    snap = db.query(EvaluationSnapshot).filter_by(id=off_decision.evaluation_snapshot_id).first()
    assert snap is not None
    assert len(snap.snapshot_hash) == 64


def test_four_eyes_override_approval_governance(db: Session, setup_phase5_data):
    sub = setup_phase5_data["submission"]
    req = setup_phase5_data["requirement"]

    # 1. Create decision with 4-eyes requirement
    off_dec = officer_decision_service.record_officer_decision(
        db=db,
        bid_submission_id=sub.id,
        reviewer_id="OFFICER_A",
        reviewer_role="ProcurementOfficer",
        decision="QUALIFIED",
        rationale="Special policy exception requested.",
        overrides_data=[{
            "requirement_id": req.id,
            "previous_status": "FAIL",
            "new_status": "PASS",
            "override_reason_code": "POLICY_EXCEPTION",
            "override_reason": "Executive exemption granted by procurement board.",
            "requires_four_eyes": True
        }]
    )

    override = off_dec.overrides[0]
    assert override.requires_four_eyes is True
    assert override.four_eyes_status == "PENDING_APPROVAL"

    # 2. Officer B approves override
    approved_ov = officer_decision_service.approve_manual_override(
        db=db,
        override_id=override.id,
        approver_id="OFFICER_B",
        approver_role="SeniorReviewer",
        approved=True,
        comments="Executive exemption verified against board resolution minutes."
    )

    assert approved_ov.four_eyes_status == "APPROVED"
    assert approved_ov.approved_by_officer_id == "OFFICER_B"


def test_tamper_evident_audit_hash_chain_integration(db: Session, setup_phase5_data):
    sub = setup_phase5_data["submission"]

    # Perform actions
    officer_decision_service.create_evaluation_snapshot(db, bid_submission_id=sub.id, evaluator_id="TEST_AUDIT")

    # Verify audit hash chain
    is_valid, total_blocks = audit_service.verify_chain(db)
    assert is_valid is True
    assert total_blocks >= 1


def test_phase5_api_rbac_security(client: TestClient, db: Session, setup_phase5_data):
    sub = setup_phase5_data["submission"]

    # Create standard bidder user
    bidder_user = User(
        email="bidder_user@vendor.com",
        full_name="Bidder Vendor User",
        hashed_password=get_password_hash("BidderPass123!"),
        role="Bidder",
        organization_id="VENDOR_01"
    )
    db.add(bidder_user)
    db.commit()

    bidder_token = create_access_token(subject=bidder_user.id, role=bidder_user.role)
    bidder_headers = {"Authorization": f"Bearer {bidder_token}"}

    # 1. Bidder attempts officer decision (Should be 403 Forbidden)
    res = client.post(
        f"/api/v1/bids/{sub.id}/officer-decisions",
        headers=bidder_headers,
        json={
            "decision": "QUALIFIED",
            "rationale": "Unauthorized bidder attempting self-qualification"
        }
    )
    assert res.status_code == 403

    # 2. Bidder attempts to resolve human review (Should be 403 Forbidden)
    res = client.post(
        "/api/v1/human-reviews/TASK_99/resolve",
        headers=bidder_headers,
        json={
            "decision": "RESOLVED",
            "resolution_summary": "Unauthorized resolution attempt"
        }
    )
    assert res.status_code == 403

    # 3. Unauthenticated request to create manual override (Should be 401 Unauthorized)
    res_unauth = client.post(
        f"/api/v1/bids/{sub.id}/manual-overrides",
        json={
            "requirement_id": setup_phase5_data["requirement"].id,
            "previous_status": "FAIL",
            "new_status": "PASS",
            "override_reason": "Unauthenticated override attempt"
        }
    )
    assert res_unauth.status_code == 401

    # 4. Bidder attempts manual override creation (Should be 403 Forbidden)
    res_bidder_ov = client.post(
        f"/api/v1/bids/{sub.id}/manual-overrides",
        headers=bidder_headers,
        json={
            "requirement_id": setup_phase5_data["requirement"].id,
            "previous_status": "FAIL",
            "new_status": "PASS",
            "override_reason": "Bidder override attempt"
        }
    )
    assert res_bidder_ov.status_code == 403

    # 5. Bidder attempts manual override approval (Should be 403 Forbidden)
    res_bidder_app = client.post(
        "/api/v1/manual-overrides/OV_DUMMY_99/approve",
        headers=bidder_headers,
        json={"approved": True}
    )
    assert res_bidder_app.status_code == 403


def test_phase5_api_officer_workflow(client: TestClient, db: Session, setup_phase5_data, officer_headers):
    sub = setup_phase5_data["submission"]

    # 1. Fetch risk assessment
    res = client.get(f"/api/v1/bids/{sub.id}/risk-assessment", headers=officer_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["bid_submission_id"] == sub.id
    assert data["is_advisory_only"] is True

    # 2. Fetch compliance explanation ("Why?" view)
    res = client.get(f"/api/v1/bids/{sub.id}/explanation", headers=officer_headers)
    assert res.status_code == 200
    exp_data = res.json()
    assert exp_data["bid_submission_id"] == sub.id
    assert len(exp_data["explanations"]) >= 1

    # 3. Post officer decision
    res = client.post(
        f"/api/v1/bids/{sub.id}/officer-decisions",
        headers=officer_headers,
        json={
            "decision": "QUALIFIED",
            "rationale": "Comprehensive verification complete. All criteria satisfied."
        }
    )
    assert res.status_code == 201
    dec_data = res.json()
    assert dec_data["decision"] == "QUALIFIED"
    assert dec_data["evaluation_snapshot_id"] is not None


def test_manual_override_api_four_eyes_and_get_endpoints(client: TestClient, db: Session, setup_phase5_data, officer_headers):
    sub = setup_phase5_data["submission"]
    req = setup_phase5_data["requirement"]

    # 1. Procurement Officer A proposes override with four-eyes required
    res_ov = client.post(
        f"/api/v1/bids/{sub.id}/manual-overrides",
        headers=officer_headers,
        json={
            "requirement_id": req.id,
            "previous_status": "MISSING_EVIDENCE",
            "new_status": "PASS",
            "override_reason_code": "POLICY_EXCEPTION",
            "override_reason": "Board pre-bid exemption approved.",
            "requires_four_eyes": True
        }
    )
    assert res_ov.status_code == 201
    ov_data = res_ov.json()
    override_id = ov_data["id"]
    assert ov_data["requires_four_eyes"] is True
    assert ov_data["four_eyes_status"] == "PENDING_APPROVAL"

    # 2. Procurement Officer A attempts approval -> 403 Forbidden (ProcurementOfficer lacks approval role)
    res_proc_app = client.post(
        f"/api/v1/manual-overrides/{override_id}/approve",
        headers=officer_headers,
        json={"approved": True, "comments": "Procurement officer attempting approval"}
    )
    assert res_proc_app.status_code == 403

    # 3. Create Senior Reviewer A (Proposer) and Senior Reviewer B (Approver)
    snr_a = User(
        email="senior_reviewer_a@cpcl.gov.in",
        full_name="Senior Reviewer A",
        hashed_password=get_password_hash("SeniorPass123!"),
        role="SeniorReviewer",
        organization_id="CPCL"
    )
    snr_b = User(
        email="senior_reviewer_b@cpcl.gov.in",
        full_name="Senior Reviewer B",
        hashed_password=get_password_hash("SeniorPass123!"),
        role="SeniorReviewer",
        organization_id="CPCL"
    )
    db.add(snr_a)
    db.add(snr_b)
    db.commit()

    token_a = create_access_token(subject=snr_a.id, role=snr_a.role)
    headers_a = {"Authorization": f"Bearer {token_a}"}

    token_b = create_access_token(subject=snr_b.id, role=snr_b.role)
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 4. Senior Reviewer A proposes four-eyes override
    res_snr_ov = client.post(
        f"/api/v1/bids/{sub.id}/manual-overrides",
        headers=headers_a,
        json={
            "requirement_id": req.id,
            "previous_status": "FAIL",
            "new_status": "PASS",
            "override_reason_code": "DATA_CORRECTION",
            "override_reason": "CA audited turnover data verified.",
            "requires_four_eyes": True
        }
    )
    assert res_snr_ov.status_code == 201
    snr_override_id = res_snr_ov.json()["id"]

    # 5. Senior Reviewer A attempts self-approval -> 400 Bad Request (Four-eyes policy violation)
    res_self_app = client.post(
        f"/api/v1/manual-overrides/{snr_override_id}/approve",
        headers=headers_a,
        json={"approved": True, "comments": "Attempting self-approval"}
    )
    assert res_self_app.status_code == 400
    assert "Four-eyes policy violation" in res_self_app.json()["detail"]

    # 6. Senior Reviewer B approves Senior Reviewer A's request -> 200 OK
    res_app = client.post(
        f"/api/v1/manual-overrides/{snr_override_id}/approve",
        headers=headers_b,
        json={"approved": True, "comments": "Senior Reviewer B verified CA statement."}
    )
    assert res_app.status_code == 200
    assert res_app.json()["four_eyes_status"] == "APPROVED"

    # 5. Test GET manual overrides for submission
    res_list = client.get(f"/api/v1/bids/{sub.id}/manual-overrides", headers=officer_headers)
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

    # 6. Test GET manual override by ID
    res_get = client.get(f"/api/v1/manual-overrides/{override_id}", headers=officer_headers)
    assert res_get.status_code == 200
    assert res_get.json()["id"] == override_id
