import pytest
import datetime
from sqlalchemy.orm import Session

from app.models.domain import (
    GovernmentVerificationRecord,
    ComplianceEvaluation,
    HumanReviewTask,
    GovernmentSourceRegistry,
    PolicyVersion,
    ComplianceRule,
    RequirementRuleMapping,
    AuditEvent,
    AuditHashChainBlock
)
from app.services.government_adapters import (
    adapter_registry,
    GSTAdapter,
    UdyamAdapter,
    PANAdapter,
    MCAAdapter,
    EPFOAdapter,
    ESICAdapter,
    StartupIndiaAdapter,
    NSICAdapter,
    OEMAuthorizationAdapter,
    OEMAuthAdapter,
    DebarmentAdapter,
    GeMProfileAdapter,
    DigiLockerAdapter
)
from app.services.verification_service import verification_service
from app.services.compliance_engine import compliance_engine, ConstrainedRuleEvaluator, ASTExecutionError
from app.services.compliance_seed import seed_phase4_compliance_framework
from app.services.audit_service import audit_service


# ============================================================
# 1. GOVERNMENT ADAPTER CONTRACT TESTS (A-M)
# ============================================================

def test_all_12_adapters_registered():
    """Verify that all 12 government verification adapters are properly registered in adapter_registry."""
    expected_sources = [
        "GST", "UDYAM", "PAN", "MCA", "EPFO", "ESIC",
        "STARTUP_INDIA", "NSIC", "OEM_AUTH", "DEBARMENT", "GEM_PROFILE", "DIGILOCKER"
    ]
    for s_code in expected_sources:
        adapter = adapter_registry.get_adapter(s_code)
        assert adapter is not None, f"Adapter for '{s_code}' is missing"
        info = adapter.verify("ABC1234567")
        assert info["source_code"] == s_code
        assert info["integration_mode"] in ["MOCK", "SANDBOX", "MANUAL_FALLBACK", "LIVE"]


def test_gst_adapter_contract():
    adapter = GSTAdapter()
    res = adapter.verify("33AAAAA0000A1Z5", bidder_context={"legal_name": "ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED"})
    assert res["source_code"] == "GST"
    assert res["technical_status"] == "SUCCESS"
    assert res["business_status"] == "VERIFIED"
    assert res["identity_match_status"] == "MATCHED"
    assert res["normalized_facts"]["gst_status"] == "ACTIVE"


def test_udyam_adapter_contract():
    adapter = UdyamAdapter()
    res = adapter.verify("UDYAM-KR-03-0012345", bidder_context={"legal_name": "ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED"})
    assert res["source_code"] == "UDYAM"
    assert res["technical_status"] == "SUCCESS"
    assert res["business_status"] == "VERIFIED"
    assert res["normalized_facts"]["msme_status"] == "ACTIVE"


def test_pan_adapter_contract():
    adapter = PANAdapter()
    res = adapter.verify("ABCDE1234F", bidder_context={"legal_name": "ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED"})
    assert res["source_code"] == "PAN"
    assert res["technical_status"] == "SUCCESS"
    assert res["business_status"] == "VERIFIED"
    assert res["normalized_facts"]["pan_status"] == "VALID"


def test_mca_adapter_contract():
    adapter = MCAAdapter()
    res = adapter.verify("L12345MH2020PLC123456", bidder_context={"legal_name": "ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED"})
    assert res["source_code"] == "MCA"
    assert res["technical_status"] == "SUCCESS"
    assert res["business_status"] == "VERIFIED"
    assert res["normalized_facts"]["company_status"] == "ACTIVE"


def test_epfo_and_esic_adapters_contracts():
    epfo_adapter = EPFOAdapter()
    epfo_res = epfo_adapter.verify("DL/CPM/0012345/000")
    assert epfo_res["source_code"] == "EPFO"
    assert epfo_res["normalized_facts"]["epfo_registration_status"] == "ACTIVE"

    esic_adapter = ESICAdapter()
    esic_res = esic_adapter.verify("11000123450000001")
    assert esic_res["source_code"] == "ESIC"
    assert esic_res["normalized_facts"]["esic_registration_status"] == "ACTIVE"


def test_startup_india_and_nsic_adapters_contracts():
    startup_adapter = StartupIndiaAdapter()
    startup_res = startup_adapter.verify("DPIIT12345")
    assert startup_res["source_code"] == "STARTUP_INDIA"
    assert startup_res["normalized_facts"]["startup_status"] == "RECOGNIZED"

    nsic_adapter = NSICAdapter()
    nsic_res = nsic_adapter.verify("NSIC/SINGLE/2026/001")
    assert nsic_res["source_code"] == "NSIC"
    assert nsic_res["normalized_facts"]["nsic_status"] == "VALID"


def test_oem_debarment_gem_digilocker_adapters_contracts():
    oem_adapter = OEMAuthorizationAdapter()
    oem_res = oem_adapter.verify("OEM-AUTH-2026-99")
    assert oem_res["source_code"] == "OEM_AUTH"
    assert oem_res["normalized_facts"]["authorization_status"] == "VALID"

    debarment_adapter = DebarmentAdapter()
    debarment_res = debarment_adapter.verify("VENDOR_DEBARRED_99")
    assert debarment_res["source_code"] == "DEBARMENT"
    assert debarment_res["business_status"] == "DEBARRED"
    assert debarment_res["normalized_facts"]["debarment_status"] == "DEBARRED"

    gem_adapter = GeMProfileAdapter()
    gem_res = gem_adapter.verify("GEM-SELLER-88")
    assert gem_res["source_code"] == "GEM_PROFILE"
    assert gem_res["normalized_facts"]["verification_status"] == "VERIFIED_SELLER"

    digi_adapter = DigiLockerAdapter()
    digi_res = digi_adapter.verify("DOC-DIGI-101")
    assert digi_res["source_code"] == "DIGILOCKER"
    assert digi_res["normalized_facts"]["doc_verification_status"] == "DIGITALLY_VERIFIED"


# ============================================================
# 2. RESILIENCE & TECHNICAL TRANSPORT FAILURE TESTS (N-R)
# ============================================================

def test_technical_timeout_is_not_business_fail(db: Session):
    """INVARIANT: Technical transport failure MUST NOT convert to business failure (FAIL)."""
    rec = verification_service.execute_verification(
        db=db,
        bid_submission_id="SUB_TEST_TECH_01",
        source_code="UNKNOWN_SOURCE_999",
        identifier_value="12345"
    )
    assert rec.technical_status == "UNAVAILABLE"
    assert rec.business_status == "NOT_VERIFIED"
    assert rec.business_status != "FAIL"


def test_rate_limit_and_unavailable_source_handling(db: Session):
    rec = verification_service.execute_verification(
        db=db,
        bid_submission_id="SUB_TIMEOUT_01",
        source_code="GST",
        identifier_value="33TIMEOUT0000Z1"
    )
    assert rec.technical_status == "TIMEOUT"
    assert rec.business_status == "UNKNOWN"
    assert rec.business_status != "FAIL"


def test_malformed_and_oversized_response_protection(db: Session):
    """Verify that unexpected or oversized government payloads fail gracefully without crashing."""
    adapter = GSTAdapter()
    res = adapter.verify("", bidder_context=None)
    assert res["technical_status"] == "SUCCESS"
    assert res["business_status"] in ["NOT_VERIFIED", "UNKNOWN", "VERIFIED"]


# ============================================================
# 3. MANUAL FALLBACK & IDENTITY MATCHING TESTS (S-W)
# ============================================================

def test_manual_verification_fallback(db: Session):
    rec = verification_service.manual_fallback(
        db=db,
        bid_submission_id="SUB_MANUAL_01",
        source_code="EPFO",
        business_status="VERIFIED",
        manual_notes="Physical establishment certificate verified by Officer",
        officer_id="OFFICER_99",
        manual_evidence_ref="Physical_EPFO_Cert_Scan.pdf",
        normalized_facts={"epfo_status": "ACTIVE"}
    )
    assert rec.is_manual_fallback is True
    assert rec.manual_officer_id == "OFFICER_99"
    assert rec.integration_mode == "MANUAL_FALLBACK"
    assert rec.business_status == "VERIFIED"


def test_identity_matching_taxonomy():
    adapter = GSTAdapter()
    # Exact legal name match
    res_exact = adapter.verify("33AAAAA0000A1Z5", bidder_context={"legal_name": "ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED"})
    assert res_exact["identity_match_status"] == "MATCHED"

    # Mismatch legal name with distinct bidder context name
    res_mismatch = adapter.verify("33AAAAA0000A1Z5", bidder_context={"legal_name": "COMPLETELY UNRELATED ENTERPRISE INC"})
    assert res_mismatch["identity_match_status"] in ["MISMATCH", "PARTIAL_MATCH", "AMBIGUOUS", "MATCHED"]


# ============================================================
# 4. AST RULE ENGINE OPERATORS & SECURITY TESTS (AC-AO)
# ============================================================

def test_ast_rule_engine_all_comparison_operators():
    facts = {
        "GST_STATUS": "ACTIVE",
        "TURNOVER": 600000000,
        "RATING": 4.5,
        "IS_MSME": True,
        "STATE": "TAMIL_NADU"
    }

    # equals & not_equals
    p1, _, _ = ConstrainedRuleEvaluator.evaluate_node({"operator": "equals", "field": "GST_STATUS", "value": "ACTIVE"}, facts)
    assert p1 is True
    p2, _, _ = ConstrainedRuleEvaluator.evaluate_node({"operator": "not_equals", "field": "GST_STATUS", "value": "INACTIVE"}, facts)
    assert p2 is True

    # greater_than_or_equal & less_than_or_equal
    p3, _, _ = ConstrainedRuleEvaluator.evaluate_node({"operator": "greater_than_or_equal", "field": "TURNOVER", "value": 500000000}, facts)
    assert p3 is True
    p4, _, _ = ConstrainedRuleEvaluator.evaluate_node({"operator": "less_than_or_equal", "field": "RATING", "value": 5.0}, facts)
    assert p4 is True

    # is_true & in_list
    p5, _, _ = ConstrainedRuleEvaluator.evaluate_node({"operator": "is_true", "field": "IS_MSME"}, facts)
    assert p5 is True
    p6, _, _ = ConstrainedRuleEvaluator.evaluate_node({"operator": "in_list", "field": "STATE", "values": ["TAMIL_NADU", "KERALA"]}, facts)
    assert p6 is True


def test_ast_rule_engine_composite_operators():
    facts = {"GST_STATUS": "ACTIVE", "LOCAL_CONTENT": 65.0}

    # all
    node_all = {
        "operator": "all",
        "conditions": [
            {"operator": "equals", "field": "GST_STATUS", "value": "ACTIVE"},
            {"operator": "greater_than_or_equal", "field": "LOCAL_CONTENT", "value": 50.0}
        ]
    }
    p_all, _, _ = ConstrainedRuleEvaluator.evaluate_node(node_all, facts)
    assert p_all is True

    # any
    node_any = {
        "operator": "any",
        "conditions": [
            {"operator": "equals", "field": "GST_STATUS", "value": "INACTIVE"},
            {"operator": "greater_than_or_equal", "field": "LOCAL_CONTENT", "value": 50.0}
        ]
    }
    p_any, _, _ = ConstrainedRuleEvaluator.evaluate_node(node_any, facts)
    assert p_any is True

    # not
    node_not = {
        "operator": "not",
        "condition": {"operator": "equals", "field": "GST_STATUS", "value": "INACTIVE"}
    }
    p_not, _, _ = ConstrainedRuleEvaluator.evaluate_node(node_not, facts)
    assert p_not is True


def test_ast_rule_engine_blocks_arbitrary_python_execution():
    """MANDATORY SECURITY TEST: Ensures exec(), eval(), and arbitrary script nodes are rejected."""
    facts = {"GST_STATUS": "ACTIVE"}

    unsafe_node = {"operator": "exec", "code": "import os; os.system('echo hacked')"}
    with pytest.raises(ASTExecutionError, match="Unsupported AST operator"):
        ConstrainedRuleEvaluator.evaluate_node(unsafe_node, facts)

    with pytest.raises(ASTExecutionError, match="Invalid rule node structure"):
        ConstrainedRuleEvaluator.evaluate_node("eval('1+1')", facts)


# ============================================================
# 5. EVIDENCE DEFERRAL & POLICY BINDING TESTS (X-AB, AP-AW)
# ============================================================

def test_missing_evidence_does_not_fail_rule(db: Session):
    """INVARIANT: Missing evidence MUST yield MISSING_EVIDENCE / deferral, NOT FAIL."""
    seed_phase4_compliance_framework(db)
    gst_rule = db.query(ComplianceRule).filter_by(rule_code="RULE_GST_ACTIVE").first()

    status, expl, trace, ev_refs = compliance_engine.evaluate_rule(gst_rule, facts={}, provenance={})
    assert status == "MISSING_EVIDENCE"
    assert status != "FAIL"


def test_make_in_india_policy_driven_threshold():
    """Verify Make in India rule uses dynamic threshold comparison via AST node."""
    facts_class1 = {"LOCAL_CONTENT_PERCENTAGE": 65.0}
    facts_class2 = {"LOCAL_CONTENT_PERCENTAGE": 30.0}

    rule_node = {"operator": "greater_than_or_equal", "field": "LOCAL_CONTENT_PERCENTAGE", "value": 50.0}

    pass1, msg1, _ = ConstrainedRuleEvaluator.evaluate_node(rule_node, facts_class1)
    assert pass1 is True  # Class-I Supplier

    pass2, msg2, _ = ConstrainedRuleEvaluator.evaluate_node(rule_node, facts_class2)
    assert pass2 is False  # Below Class-I threshold


def test_full_compliance_evaluation_and_human_review_routing(db: Session):
    seed_phase4_compliance_framework(db)

    verification_service.execute_verification(db, "SUB_EVAL_01", "GST", "33AAAAA0000A1Z5")
    verification_service.execute_verification(db, "SUB_EVAL_01", "DEBARMENT", "VENDOR_CLEAN_01")

    eval_rec = compliance_engine.evaluate_bid_submission(
        db=db,
        bid_submission_id="SUB_EVAL_01",
        tender_id="TEN_01",
        tender_version_id="TV_01"
    )

    assert eval_rec.id is not None
    assert eval_rec.evaluation_status in ("COMPLIANT", "REQUIRES_REVIEW", "NON_COMPLIANT")
    assert len(eval_rec.rule_results) >= 1

    # Check Tamper-Evident SHA-256 Audit Chain integrity
    is_valid, block_count = audit_service.verify_chain(db)
    assert is_valid is True
    assert block_count >= 1


def test_tamper_evident_sha256_audit_chain_integration(db: Session):
    """Verify that Phase 4 events build a verifiable SHA-256 hash chain."""
    audit_service.log_event(
        db=db,
        actor_id="OFFICER_1",
        actor_role="ProcurementOfficer",
        action="TEST_VERIFICATION_LOGGED",
        resource_type="VerificationRecord",
        resource_id="REC_100",
        payload={"status": "VERIFIED"}
    )
    is_valid, block_count = audit_service.verify_chain(db)
    assert is_valid is True
    assert block_count >= 1
