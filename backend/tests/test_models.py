from app.models.domain import User, Tender, TenderVersion, TenderRequirement, Bidder, BidSubmission


def test_domain_model_relationships(db):
    # 1. User
    user = User(
        email="test_user@cpcl.gov.in",
        full_name="Test User",
        hashed_password="hashed_pass_123",
        role="ProcurementOfficer",
    )
    db.add(user)
    db.flush()
    assert len(user.id) == 26

    # 2. Tender & Version
    tender = Tender(
        tender_number="TENDER-TEST-001",
        title="Test Procurement Tender",
        organization="CPCL",
    )
    db.add(tender)
    db.flush()

    version = TenderVersion(
        tender_id=tender.id,
        version_number=1,
        description="Version 1",
    )
    db.add(version)
    db.flush()

    req = TenderRequirement(
        tender_version_id=version.id,
        requirement_code="REQ-001",
        category="TECHNICAL",
        requirement_text="Must supply pumps",
    )
    db.add(req)

    # 3. Bidder & Submission
    bidder = Bidder(
        bidder_name="Test Bidder Ltd",
        registration_number="REG-001",
    )
    db.add(bidder)
    db.flush()

    submission = BidSubmission(
        bidder_id=bidder.id,
        tender_id=tender.id,
        tender_version_id=version.id,
        submission_reference="SUB-001",
    )
    db.add(submission)
    db.commit()

    assert submission.id is not None
    assert submission.tender_version_id == version.id
    assert len(tender.versions) == 1
    assert len(version.requirements) == 1
