from app.services.audit_service import AuditService
from app.models.domain import AuditEvent


def test_audit_hash_chain_verification_and_tamper_detection(db):
    # 1. Create Event A
    event_a = AuditService.log_event(
        db=db,
        actor_id="USER-001",
        actor_role="ProcurementOfficer",
        action="TENDER_CREATED",
        resource_type="Tender",
        resource_id="TENDER-001",
        correlation_id="CORR-A",
        payload={"tender_number": "TENDER-001", "amount": 100000},
    )

    # 2. Create Event B
    event_b = AuditService.log_event(
        db=db,
        actor_id="USER-002",
        actor_role="ProcurementOfficer",
        action="BIDDER_REGISTERED",
        resource_type="Bidder",
        resource_id="BIDDER-001",
        correlation_id="CORR-B",
        payload={"bidder_name": "ABC Engineering Pvt Ltd"},
    )

    # 3. Create Event C
    event_c = AuditService.log_event(
        db=db,
        actor_id="USER-001",
        actor_role="ProcurementOfficer",
        action="BID_SUBMITTED",
        resource_type="BidSubmission",
        resource_id="SUB-001",
        correlation_id="CORR-C",
        payload={"submission_ref": "SUB-001"},
    )

    # 4. Verify original hash chain integrity (Must be VALID)
    is_valid, total, verified, corrupted_index, msg = AuditService.verify_chain_integrity(db)
    assert is_valid is True
    assert total == 3
    assert verified == 3
    assert corrupted_index is None

    # 5. TAMPER TEST: Alter Event B payload in database directly
    event_b.event_payload = {"bidder_name": "TAMPERED Malicious Competitor Pvt Ltd"}
    db.commit()

    # 6. Verify tampered hash chain integrity (Must FAIL & report corruption at block 1)
    is_valid, total, verified, corrupted_index, msg = AuditService.verify_chain_integrity(db)
    assert is_valid is False
    assert corrupted_index == 1
    assert "Audit event payload altered" in msg
