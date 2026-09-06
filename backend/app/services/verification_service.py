import uuid
import datetime
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from app.models.domain import GovernmentVerificationRecord, ComplianceFact, SourceDocument
from app.services.government_adapters import adapter_registry
from app.services.audit_service import audit_service


class VerificationService:
    def execute_verification(
        self,
        db: Session,
        bid_submission_id: str,
        source_code: str,
        identifier_value: str,
        bidder_context: Optional[Dict[str, Any]] = None,
        integration_mode: str = "MOCK",
        actor_id: str = "SYSTEM",
        correlation_id: Optional[str] = None
    ) -> GovernmentVerificationRecord:
        corr_id = correlation_id or f"CORR_{uuid.uuid4().hex[:12].upper()}"
        adapter = adapter_registry.get_adapter(source_code)

        if not adapter:
            # Handle unknown or unconfigured adapter gracefully
            rec = GovernmentVerificationRecord(
                bid_submission_id=bid_submission_id,
                source_code=source_code,
                adapter_name="UnknownAdapter",
                integration_mode=integration_mode,
                technical_status="UNAVAILABLE",
                business_status="NOT_VERIFIED",
                source_authority_type="UNKNOWN",
                freshness_status="NOT_APPLICABLE",
                identity_match_status="NOT_VERIFIED",
                normalized_facts_json={},
                error_category="UNSUPPORTED_ADAPTER",
                correlation_id=corr_id
            )
            db.add(rec)
            db.commit()
            db.refresh(rec)
            return rec

        # Execute adapter
        try:
            res = adapter.verify(identifier_value, bidder_context, integration_mode=integration_mode)
            tech_status = res.get("technical_status", "SUCCESS")
            bus_status = res.get("business_status", "VERIFIED")
            id_match = res.get("identity_match_status", "MATCHED")
            facts = res.get("normalized_facts", {})
            raw_hash = res.get("raw_response_hash")
            err_cat = res.get("error_category")
        except Exception as exc:
            # Technical failure handling (Timeout/Network) MUST NEVER become business FAIL
            tech_status = "TIMEOUT"
            bus_status = "UNKNOWN"
            id_match = "NOT_VERIFIED"
            facts = {}
            raw_hash = None
            err_cat = f"ADAPTER_EXCEPTION: {str(exc)}"

        rec = GovernmentVerificationRecord(
            bid_submission_id=bid_submission_id,
            source_code=source_code,
            adapter_name=adapter.__class__.__name__,
            integration_mode=integration_mode,
            requested_at=datetime.datetime.utcnow(),
            responded_at=datetime.datetime.utcnow(),
            technical_status=tech_status,
            business_status=bus_status,
            source_authority_type=adapter.authority_type,
            freshness_status="FRESH",
            identity_match_status=id_match,
            normalized_facts_json=facts,
            raw_response_hash=raw_hash,
            error_category=err_cat,
            correlation_id=corr_id
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)

        # Convert normalized facts to ComplianceFact entries
        for key, val in facts.items():
            cf = ComplianceFact(
                bid_submission_id=bid_submission_id,
                fact_code=f"{source_code}_{key.upper()}",
                fact_value={"value": val},
                fact_status="VERIFIED" if bus_status == "VERIFIED" else "UNVERIFIED",
                provenance_ref=f"GovernmentVerificationRecord:{rec.id}#{key}",
                verification_record_id=rec.id
            )
            db.add(cf)

        db.commit()

        # Audit verification execution
        audit_service.log_event(
            db=db,
            actor_id=actor_id,
            actor_role="ProcurementOfficer",
            action="GOVERNMENT_VERIFICATION_EXECUTED",
            resource_type="GovernmentVerificationRecord",
            resource_id=rec.id,
            payload={
                "source_code": source_code,
                "technical_status": tech_status,
                "business_status": bus_status,
                "identity_match_status": id_match,
                "integration_mode": integration_mode,
                "correlation_id": corr_id
            }
        )

        return rec

    def manual_fallback(
        self,
        db: Session,
        bid_submission_id: str,
        source_code: str,
        business_status: str,
        manual_notes: str,
        officer_id: str,
        manual_evidence_ref: Optional[str] = None,
        normalized_facts: Optional[Dict[str, Any]] = None
    ) -> GovernmentVerificationRecord:
        facts = normalized_facts or {}
        rec = GovernmentVerificationRecord(
            bid_submission_id=bid_submission_id,
            source_code=source_code,
            adapter_name="ManualFallbackAdapter",
            integration_mode="MANUAL_FALLBACK",
            requested_at=datetime.datetime.utcnow(),
            responded_at=datetime.datetime.utcnow(),
            technical_status="SUCCESS",
            business_status=business_status,
            source_authority_type="MANUAL_OFFICER_VERIFICATION",
            freshness_status="FRESH",
            identity_match_status="MATCHED",
            normalized_facts_json=facts,
            is_manual_fallback=True,
            manual_officer_id=officer_id,
            manual_notes=manual_notes,
            manual_evidence_ref=manual_evidence_ref,
            correlation_id=f"MANUAL_{uuid.uuid4().hex[:12].upper()}"
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)

        # Convert manual facts to ComplianceFact entries
        for key, val in facts.items():
            cf = ComplianceFact(
                bid_submission_id=bid_submission_id,
                fact_code=f"{source_code}_{key.upper()}",
                fact_value={"value": val},
                fact_status="VERIFIED" if business_status == "VERIFIED" else "UNVERIFIED",
                provenance_ref=f"GovernmentVerificationRecord:{rec.id}#manual#{key}",
                verification_record_id=rec.id
            )
            db.add(cf)

        db.commit()

        # Audit manual fallback
        audit_service.log_event(
            db=db,
            actor_id=officer_id,
            actor_role="ProcurementOfficer",
            action="MANUAL_VERIFICATION_FALLBACK_RECORDED",
            resource_type="GovernmentVerificationRecord",
            resource_id=rec.id,
            payload={
                "source_code": source_code,
                "business_status": business_status,
                "manual_notes": manual_notes,
                "manual_evidence_ref": manual_evidence_ref
            }
        )

        return rec


verification_service = VerificationService()
