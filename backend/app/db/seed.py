from sqlalchemy.orm import Session
from app.db.session import SessionLocal, Base, engine
from app.models.domain import User, Tender, TenderVersion, TenderRequirement, Bidder, BidderIdentity, BidSubmission, SubmissionCover
from app.core.security import get_password_hash
from app.services.audit_service import AuditService
from app.core.logging import logger


def seed_database(db: Session) -> None:
    logger.info("Initializing synthetic demonstration seed data...")

    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # 1. Create Demo Users if not exists
    users_data = [
        ("officer@cpcl.gov.in", "Rajesh Kumar (Procurement Officer)", "ProcurementOfficer"),
        ("senior@cpcl.gov.in", "Anita Sharma (Senior Reviewer)", "SeniorReviewer"),
        ("auditor@cpcl.gov.in", "Vikram Patel (Auditor)", "Auditor"),
        ("admin@cpcl.gov.in", "System Administrator", "SystemAdmin"),
    ]

    users = {}
    for email, full_name, role in users_data:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                email=email,
                full_name=full_name,
                hashed_password=get_password_hash("DemoPass123!"),
                role=role,
                organization_id="CPCL",
                is_active=True,
            )
            db.add(user)
            db.flush()
            logger.info(f"Seeded demo user: {email} ({role})")
        users[role] = user

    # 2. Create Demonstration Tender
    tender = db.query(Tender).filter(Tender.tender_number == "TENDER-CPCL-2026-001").first()
    if not tender:
        tender = Tender(
            tender_number="TENDER-CPCL-2026-001",
            title="Industrial Pumps & Valves Supply Procurement — Demonstration Tender",
            organization="CPCL",
            status="ACTIVE",
        )
        db.add(tender)
        db.flush()

        tender_version = TenderVersion(
            tender_id=tender.id,
            version_number=1,
            description="Initial baseline specification version for demonstration",
            is_finalized=True,
        )
        db.add(tender_version)
        db.flush()

        # Add requirements
        reqs = [
            TenderRequirement(
                tender_version_id=tender_version.id,
                requirement_code="REQ-TECH-001",
                category="TECHNICAL",
                requirement_text="Bidder must demonstrate prior execution of at least 3 similar industrial pump supply contracts in oil & gas sector.",
                is_mandatory=True,
            ),
            TenderRequirement(
                tender_version_id=tender_version.id,
                requirement_code="REQ-FIN-001",
                category="FINANCIAL",
                requirement_text="Minimum average annual financial turnover of INR 50 Lakhs over past 3 financial years certified by Chartered Accountant.",
                is_mandatory=True,
            ),
            TenderRequirement(
                tender_version_id=tender_version.id,
                requirement_code="REQ-MSE-001",
                category="PREFERENCE",
                requirement_text="Valid Micro & Small Enterprises (MSE) Udyam Registration Certificate for purchase preference exemption.",
                is_mandatory=False,
            ),
        ]
        db.add_all(reqs)
        db.flush()
        logger.info(f"Seeded demo tender: {tender.tender_number}")
    else:
        tender_version = db.query(TenderVersion).filter(TenderVersion.tender_id == tender.id).first()

    # 3. Create Demonstration Bidder
    bidder = db.query(Bidder).filter(Bidder.registration_number == "REG-2026-ABC-01").first()
    if not bidder:
        bidder = Bidder(
            bidder_name="ABC Engineering Services Pvt Ltd (DEMONSTRATION)",
            registration_number="REG-2026-ABC-01",
            entity_type="PRIVATE_LIMITED",
            organization_type="MSE",
        )
        db.add(bidder)
        db.flush()

        identity = BidderIdentity(
            bidder_id=bidder.id,
            pan_hash="DEMO_HASH_PAN_AAACA1234F",
            gstin_hash="DEMO_HASH_GSTIN_33AAACA1234F1Z5",
            udyam_hash="DEMO_HASH_UDYAM_TN-01-0012345",
            verification_status="UNVERIFIED",
        )
        db.add(identity)
        db.flush()
        logger.info(f"Seeded demo bidder: {bidder.bidder_name}")

    # 4. Create Demonstration Submission
    sub = db.query(BidSubmission).filter(BidSubmission.submission_reference == "SUB-2026-CPCL-001").first()
    if not sub and bidder and tender and tender_version:
        sub = BidSubmission(
            bidder_id=bidder.id,
            tender_id=tender.id,
            tender_version_id=tender_version.id,
            submission_reference="SUB-2026-CPCL-001",
            status="SUBMITTED",
        )
        db.add(sub)
        db.flush()

        cover = SubmissionCover(
            bid_submission_id=sub.id,
            cover_type="TECHNICAL",
            document_count=2,
            remarks="Technical proposal and experience certificates",
        )
        db.add(cover)
        db.flush()
        logger.info(f"Seeded demo submission: {sub.submission_reference}")

    # 5. Log Initial Audit Chain Event if empty
    AuditService.log_event(
        db=db,
        actor_id=users["ProcurementOfficer"].id,
        actor_role="ProcurementOfficer",
        action="SYSTEM_INITIALIZED",
        resource_type="System",
        resource_id="SIH26100-PLATFORM",
        correlation_id="INIT-SEED-001",
        payload={"message": "Phase 2 Core Platform initialized with safe synthetic demonstration data."},
    )

    db.commit()
    logger.info("Seed data initialization complete.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
