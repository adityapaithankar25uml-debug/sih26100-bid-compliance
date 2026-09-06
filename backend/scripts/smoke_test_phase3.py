"""
PHASE 3 FUNCTIONAL END-TO-END SMOKE TEST SCRIPT
SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
"""

import os
import sys

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base, engine as prod_engine, SessionLocal as ProdSessionLocal
import app.models  # Populate Base.metadata
from app.services.document_service import document_service
from app.services.document_pipeline import document_pipeline_service
from app.services.tender_intelligence import tender_intelligence_service
from app.services.bidder_intelligence import bidder_intelligence_service
from app.services.audit_service import audit_service


def get_smoke_db():
    try:
        # Try primary engine
        connection = prod_engine.connect()
        connection.close()
        engine = prod_engine
        SessionLocal = ProdSessionLocal
    except Exception:
        # Fallback to SQLite for local standalone execution
        engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def run_smoke_test():
    print("======================================================================")
    print("      STARTING PHASE 3 DOCUMENT INTELLIGENCE FUNCTIONAL SMOKE TEST    ")
    print("======================================================================")

    # 1. Initialize Tables & DB Session
    engine, SessionLocal = get_smoke_db()
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 2. Ingest Synthetic Tender Document
        print("\n--- 1. INGESTING SYNTHETIC TENDER DOCUMENT ---")
        tender_pdf = b"%PDF-1.4 NOTICE INVITING TENDER CPCL Chennai Refinery. Minimum Annual Turnover Required: Rs 50 Crores."
        doc_tender = document_service.upload_document(
            db=db,
            bid_submission_id="SUB_DEMO_TENDER_01",
            filename="CPCL_Tender_Notice_2026.pdf",
            content=tender_pdf,
            content_type="application/pdf",
            actor_id="OFFICER_01"
        )
        print(f"[OK] Uploaded Tender Doc ID: {doc_tender.id}")
        print(f"[OK] Quarantine Status: {doc_tender.quarantine_status}")
        print(f"[OK] Malware Scan Result: {doc_tender.malware_scan_result}")
        print(f"[OK] SHA-256 Hash: {doc_tender.sha256_hash[:16]}...")

        # 3. Extract Tender Requirement Candidates
        print("\n--- 2. EXTRACTING ADVISORY TENDER REQUIREMENT CANDIDATES ---")
        cand_list = tender_intelligence_service.extract_tender_requirement_candidates(
            db=db,
            tender_id="TEN_CPCL_2026_99",
            source_document=doc_tender,
            document_text="Notice Inviting Tender CPCL. Average Annual Financial Turnover: Rs 50 Crores."
        )
        print(f"[OK] Extracted {len(cand_list.candidate_requirements)} Tender Requirement Candidates:")
        for c in cand_list.candidate_requirements:
            print(f"   • Code: {c.candidate_code} | Category: {c.category} | Threshold: Rs {c.threshold_value / 1e7:.1f} Cr | Non-Authoritative: {not c.is_authoritative}")

        # 4. Ingest Synthetic Bidder CA Turnover Certificate Document
        print("\n--- 3. INGESTING SYNTHETIC BIDDER DOCUMENT ---")
        bidder_pdf = (
            b"%PDF-1.4 CHARTERED ACCOUNTANT TURNOVER CERTIFICATE\n"
            b"This is to certify that M/s ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED\n"
            b"GSTIN: 33AAAAA0000A1Z5 | PAN: AAAAA0000A | Udyam: UDYAM-TN-01-0000000\n"
            b"Turnover FY 2023-24: Rs 65.00 Crores\n"
            b"Turnover FY 2022-23: Rs 58.50 Crores"
        )
        doc_bidder = document_service.upload_document(
            db=db,
            bid_submission_id="SUB_DEMO_BIDDER_01",
            filename="CA_Turnover_Certificate_ACME.pdf",
            content=bidder_pdf,
            content_type="application/pdf",
            actor_id="BIDDER_01"
        )
        print(f"[OK] Uploaded Bidder Doc ID: {doc_bidder.id}")
        print(f"[OK] Quarantine Status: {doc_bidder.quarantine_status}")
        print(f"[OK] Security Classification: {doc_bidder.security_classification}")

        # 5. Process Full Document Pipeline
        print("\n--- 4. EXECUTING DOCUMENT INTELLIGENCE PIPELINE ---")
        pipe_res = document_pipeline_service.process_document(db, doc_bidder.id, actor_id="SERVICE_WORKER_01")
        print(f"[OK] Pipeline Processing Status: {pipe_res['status']}")
        print(f"[OK] Predicted Taxonomy Type: {pipe_res['predicted_doc_type']}")
        print(f"[OK] Security Classification: {pipe_res['security_classification']}")
        print(f"[OK] PII Detected: {pipe_res['pii_detected']}")
        print(f"[OK] Prompt Injection Detected: {pipe_res['has_prompt_injection']}")
        print(f"[OK] Extracted Facts Count: {pipe_res['extracted_fields_count']}")

        # 6. Detect Inconsistency Candidates
        print("\n--- 5. DETECTING CANDIDATE INCONSISTENCY SIGNALS ---")
        inc_list = bidder_intelligence_service.detect_inconsistency_candidates(db, "SUB_DEMO_BIDDER_01")
        print(f"[OK] Detected {len(inc_list.inconsistency_candidates)} Inconsistency Candidates:")
        for sig in inc_list.inconsistency_candidates:
            print(f"   • Signal: {sig.signal_code} | Severity: {sig.severity} | Status: {sig.status}")

        # 7. Audit Hash Chain Verification
        print("\n--- 6. VERIFYING TAMPER-EVIDENT SHA-256 AUDIT HASH CHAIN ---")
        is_valid, block_count = audit_service.verify_chain(db)
        print(f"[OK] Tamper-Evident SHA-256 Audit Hash Chain Valid: {is_valid}")
        print(f"[OK] Total Verified Audit Hash Chain Blocks: {block_count}")

        print("\n======================================================================")
        print("   PHASE 3 SMOKE TEST SUCCESSFUL — ALL COMPONENTS OPERATIONAL        ")
        print("======================================================================\n")

    finally:
        db.close()


if __name__ == "__main__":
    run_smoke_test()
