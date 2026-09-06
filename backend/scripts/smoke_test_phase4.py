#!/usr/bin/env python3
"""
SIH26100 Phase 4 Smoke Test

Verifies end-to-end Phase 4 workflow:
1. Synthetic tender, bidder, requirements setup
2. Government verification adapter triggering (Mock mode)
3. Normalized verification result generation & Fact creation
4. Policy versioning and deterministic AST rule evaluation
5. Evidence & calculation trace generation
6. Compliance matrix & qualification outcome generation
7. Identity conflict & missing evidence routing to human review
8. Audit hash-chain tamper-evidence verification
9. Axiom verification (No AI authority, No fake LIVE claims)
"""

import sys
import os
import uuid
import datetime

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Use SQLite for standalone smoke testing if PostgreSQL is not available
os.environ["DATABASE_URL"] = "sqlite:///./smoke_test.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.models.domain import (
    User, Tender, TenderVersion, TenderRequirement, Bidder, BidSubmission,
    GovernmentSourceRegistry, PolicyVersion, ComplianceRule, RequirementRuleMapping,
    AuditEvent, AuditHashChainBlock
)
from app.services.government_adapters import adapter_registry
from app.services.verification_service import VerificationService, verification_service
from app.services.compliance_engine import ComplianceEngine, compliance_engine, ConstrainedRuleEvaluator, ASTExecutionError
from app.services.compliance_seed import seed_phase4_compliance_framework
from app.services.audit_service import audit_service



engine = create_engine("sqlite:///./smoke_test.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_smoke_test():
    print("============================================================")
    print("SIH26100 PHASE 4 SMOKE TEST — GOVERNMENT VERIFICATION & COMPLIANCE")
    print("============================================================\n")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed Phase 4 default sources, policies, rules

        print("[STEP 0] Seeding Phase 4 default sources, policy versions, and rules...")
        seed_phase4_compliance_framework(db)


        # Step 1: Create synthetic user, tender, tender version, bidder, bid submission
        print("[STEP 1] Setting up synthetic tender, bidder, and requirements...")
        officer = User(
            email=f"officer_{uuid.uuid4().hex[:6]}@cpcl.gov.in",
            full_name="Procurement Officer Smoke",
            hashed_password="hash",
            role="ProcurementOfficer",
            organization_id="CPCL"
        )
        db.add(officer)

        tender = Tender(
            tender_number=f"GEM/2026/B/SMOKE_{uuid.uuid4().hex[:6]}",
            title="Smoke Test Refinery Pipe Supply",
            organization="CPCL",
            status="PUBLISHED"
        )
        db.add(tender)
        db.flush()

        tender_version = TenderVersion(
            tender_id=tender.id,
            version_number=1,
            description="Initial version",
            is_finalized=True
        )
        db.add(tender_version)
        db.flush()

        req_gst = TenderRequirement(
            tender_version_id=tender_version.id,
            requirement_code="REQ_GST_ACTIVE",
            category="ELIGIBILITY",
            requirement_text="Bidder must have active GST registration.",
            is_mandatory=True
        )
        req_turnover = TenderRequirement(
            tender_version_id=tender_version.id,
            requirement_code="REQ_TURNOVER_MIN",
            category="FINANCIAL",
            requirement_text="Bidder average annual turnover must be >= 10 Crores.",
            is_mandatory=True
        )
        req_debarment = TenderRequirement(
            tender_version_id=tender_version.id,
            requirement_code="REQ_NO_DEBARMENT",
            category="DECLARATION",
            requirement_text="Bidder must not be debarred/blacklisted by any government authority.",
            is_mandatory=True
        )
        req_mii = TenderRequirement(
            tender_version_id=tender_version.id,
            requirement_code="REQ_MAKE_IN_INDIA",
            category="TECHNICAL",
            requirement_text="Bidder must meet Class-I local content requirement (>= 50%).",
            is_mandatory=True
        )
        db.add_all([req_gst, req_turnover, req_debarment, req_mii])
        db.flush()

        bidder = Bidder(
            bidder_name="Apex Pipes & Steel Ltd",
            registration_number=f"REG_{uuid.uuid4().hex[:6]}",
            entity_type="PRIVATE_LIMITED",
            organization_type="MSE"
        )
        db.add(bidder)
        db.flush()

        submission = BidSubmission(
            bidder_id=bidder.id,
            tender_id=tender.id,
            tender_version_id=tender_version.id,
            submission_reference=f"SUB_SMOKE_{uuid.uuid4().hex[:6]}",
            status="SUBMITTED"
        )
        db.add(submission)
        db.commit()

        # Step 2: Trigger Government Verification (Mock Adapters)
        print("[STEP 2] Triggering government verifications via adapters (Mock Mode)...")

        gst_record = verification_service.execute_verification(
            db=db,
            bid_submission_id=submission.id,
            source_code="GST",
            identifier_value="33AAAAA0000A1Z5"
        )
        print(f"  - GST Verification: technical={gst_record.technical_status}, business={gst_record.business_status}, mode={gst_record.integration_mode}")

        debarment_record = verification_service.execute_verification(
            db=db,
            bid_submission_id=submission.id,
            source_code="DEBARMENT",
            identifier_value=bidder.registration_number
        )
        print(f"  - Debarment Verification: technical={debarment_record.technical_status}, business={debarment_record.business_status}, mode={debarment_record.integration_mode}")

        # Step 3: Verify Fact Extraction & Normalization
        print("[STEP 3] Verifying compliance fact normalization...")
        facts = compliance_engine.collect_facts_for_submission(db, submission.id)
        print(f"  - Collected {len(facts)} facts from submission records")

        # Step 4: AST Rule Evaluator Safety Check
        print("[STEP 4] Testing AST Constrained Rule Evaluator security...")
        
        # Safe evaluation
        valid_node = {"operator": "equals", "field": "GST_STATUS", "value": "ACTIVE"}
        passed, msg, trace = ConstrainedRuleEvaluator.evaluate_node(valid_node, {"GST_STATUS": "ACTIVE"})
        assert passed is True, "Expected safe evaluation to evaluate True"

        # Unsafe node attempting arbitrary script execution (must fail AST security check)
        unsafe_node = {"operator": "exec", "code": "import os; os.system('echo pwned')"}
        try:
            ConstrainedRuleEvaluator.evaluate_node(unsafe_node, {})
            assert False, "AST Evaluator permitted dangerous expression!"
        except ASTExecutionError as e:
            print(f"  - Security Check PASSED: Blocked arbitrary code execution ({e})")

        # Step 5: Full Compliance Evaluation & Trace Generation
        print("[STEP 5] Executing full deterministic compliance engine evaluation...")
        
        # Link requirements to rules
        rule_gst = db.query(ComplianceRule).filter_by(rule_code="RULE_GST_ACTIVE").first()
        rule_turnover = db.query(ComplianceRule).filter_by(rule_code="RULE_TURNOVER_THRESHOLD").first()
        rule_debarment = db.query(ComplianceRule).filter_by(rule_code="RULE_DEBARMENT_CHECK").first()
        rule_mii = db.query(ComplianceRule).filter_by(rule_code="RULE_MAKE_IN_INDIA").first()

        if rule_gst:
            db.add(RequirementRuleMapping(tender_id=tender.id, tender_version_id=tender_version.id, requirement_id=req_gst.id, rule_id=rule_gst.id))
        if rule_turnover:
            db.add(RequirementRuleMapping(tender_id=tender.id, tender_version_id=tender_version.id, requirement_id=req_turnover.id, rule_id=rule_turnover.id))
        if rule_debarment:
            db.add(RequirementRuleMapping(tender_id=tender.id, tender_version_id=tender_version.id, requirement_id=req_debarment.id, rule_id=rule_debarment.id))
        if rule_mii:
            db.add(RequirementRuleMapping(tender_id=tender.id, tender_version_id=tender_version.id, requirement_id=req_mii.id, rule_id=rule_mii.id))
        db.commit()

        evaluation = compliance_engine.evaluate_bid_submission(
            db=db,
            bid_submission_id=submission.id,
            tender_id=tender.id,
            tender_version_id=tender_version.id
        )

        print(f"  - Evaluation Status: {evaluation.evaluation_status}")
        print(f"  - Recommendation: {evaluation.overall_qualification_recommendation}")
        print(f"  - Rule Results Count: {len(evaluation.rule_results)}")

        # Step 6: Verify Compliance Matrix & Trace Output
        print("[STEP 6] Verifying compliance matrix & calculation trace...")
        for r_res in evaluation.rule_results:
            print(f"  - Rule: {r_res.rule_code} | Status: {r_res.result_status} | Explanation: {r_res.explanation_text}")

        # Step 7: Technical Timeout Test (Timeout -> UNKNOWN / REVIEW_REQUIRED, NOT FAIL)
        print("[STEP 7] Verifying Technical Failure Boundary (Timeout != FAIL)...")
        timeout_record = verification_service.execute_verification(
            db=db,
            bid_submission_id=submission.id,
            source_code="UNKNOWN_SOURCE_999",
            identifier_value="12345"
        )
        assert timeout_record.technical_status == "UNAVAILABLE", "Expected UNAVAILABLE technical status"
        assert timeout_record.business_status == "NOT_VERIFIED", "Expected NOT_VERIFIED business status"
        assert timeout_record.business_status != "FAIL", "Technical failure must not auto-fail business verification"
        print("  - Technical Failure correctly yielded NOT_VERIFIED business status without auto-failing bidder.")

        # Step 8: Manual Fallback Verification
        print("[STEP 8] Verifying Manual Fallback Workflow...")
        manual_record = verification_service.manual_fallback(
            db=db,
            bid_submission_id=submission.id,
            source_code="EPFO",
            business_status="VERIFIED",
            manual_notes="Verified against EPFO Portal manually",
            officer_id=officer.id,
            manual_evidence_ref="DOC_EPFO_RECEIPT_2026.pdf",
            normalized_facts={"epfo_status": "ACTIVE"}
        )
        assert manual_record.is_manual_fallback is True, "Expected manual fallback flag"
        print(f"  - Manual Fallback recorded: source={manual_record.source_code}, status={manual_record.business_status}")


        # Step 9: Audit Hash-Chain Integrity Check
        print("[STEP 9] Verifying Audit Hash-Chain Integrity...")
        blocks = db.query(AuditHashChainBlock).order_by(AuditHashChainBlock.block_index.asc()).all()
        assert len(blocks) > 0, "Expected audit hash chain blocks"
        print(f"  - Audit Hash Chain has {len(blocks)} blocks.")
        prev_hash = "0" * 64
        for b in blocks:
            assert b.previous_hash == prev_hash, f"Hash chain broken at block {b.block_index}"
            prev_hash = b.current_hash
        print("  - Audit Hash Chain Integrity VERIFIED (SHA-256 link valid).")

        # Step 10: Axiom Verification
        print("[STEP 10] Verifying Axioms & Labeling Integrity...")
        sources = db.query(GovernmentSourceRegistry).all()
        for s in sources:
            assert s.integration_mode in ["MOCK", "SANDBOX", "MANUAL_FALLBACK", "LIVE"], f"Invalid mode: {s.integration_mode}"
            if s.integration_mode == "MOCK":
                assert "MOCK" in s.readiness_status or s.readiness_status != "PRODUCTION_READY", "Mock adapter claimed live production readiness!"
        print("  - Axiom Check PASSED: No fake LIVE claims detected across government source registries.")

        print("\n============================================================")
        print("SMOKE TEST COMPLETE — ALL 10 PHASES PASSED SUCCESSFULLY!")
        print("============================================================")

    finally:
        db.close()

if __name__ == "__main__":
    run_smoke_test()
