from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models.domain import (
    SourceDocument,
    DocumentExtraction,
    ExtractedField,
    BoundingBox,
    EvidenceRecord,
    ComplianceEvaluation
)
from app.services.ai_gateway import ai_gateway
from app.schemas.document_ai import (
    AIGatewayRequest,
    ExtractedFieldsEnvelope,
    ExtractedFactSchema,
    InconsistencyCandidateList,
    InconsistencyCandidateSchema
)
from app.services.audit_service import audit_service


class BidderIntelligenceService:
    def extract_bidder_facts(
        self,
        db: Session,
        source_document: SourceDocument,
        document_text: str,
        actor_id: str = "SYSTEM"
    ) -> ExtractedFieldsEnvelope:
        ai_req = AIGatewayRequest(
            task_type="BIDDER_FACT_EXTRACTION",
            task_id=f"TASK_BIDDER_{source_document.id}",
            data_sensitivity_level=source_document.security_classification,
            system_prompt_version="SP_BIDDER_FACT_EXTRACTION_v1.0",
            prompt_variables={"document_id": source_document.id},
            input_text_chunk=document_text[:8000]
        )

        ai_resp = ai_gateway.process_request(ai_req)
        raw_fields = ai_resp.structured_output.get("extracted_fields", [])

        # Persist DocumentExtraction & ExtractedFields
        extraction = DocumentExtraction(
            source_document_id=source_document.id,
            extraction_status="COMPLETED",
            extraction_method="AI_GATEWAY" if not ai_resp.is_mock else "TEXT_PARSER",
            confidence_score=ai_resp.confidence_score,
            extractor_version="v1.0",
            sensitivity_level=source_document.security_classification,
            metadata_json={"provider_id": ai_resp.provider_id, "is_mock": ai_resp.is_mock, "mode": ai_resp.mode}
        )
        db.add(extraction)
        db.commit()
        db.refresh(extraction)

        facts = []
        for f in raw_fields:
            field_name = f.get("field_name", "unknown")
            raw_val = str(f.get("raw_value", ""))
            norm_val = str(f.get("normalized_value", raw_val))

            ef = ExtractedField(
                document_extraction_id=extraction.id,
                field_name=field_name,
                field_value=raw_val,
                normalized_value=norm_val,
                source_text_snippet=raw_val,
                field_type="STRING",
                confidence=f.get("confidence_score", 0.95)
            )
            db.add(ef)
            db.commit()
            db.refresh(ef)

            # Add bounding box placeholder
            bbox = BoundingBox(
                extracted_field_id=ef.id,
                page_number=f.get("page_number", 1),
                x_min=50.0,
                y_min=100.0,
                x_max=350.0,
                y_max=120.0
            )
            db.add(bbox)

            facts.append(
                ExtractedFactSchema(
                    field_name=field_name,
                    raw_value=raw_val,
                    normalized_value=norm_val,
                    confidence_score=f.get("confidence_score", 0.95),
                    page_number=f.get("page_number", 1),
                    extraction_method="AI_GATEWAY" if not ai_resp.is_mock else "TEXT_PARSER",
                    provenance_ref=f"ExtractedField:{ef.id}"
                )
            )

        db.commit()

        # Audit event
        audit_service.log_event(
            db=db,
            actor_id=actor_id,
            actor_role="ServiceWorker",
            action="BIDDER_FACTS_EXTRACTED",
            resource_type="DocumentExtraction",
            resource_id=extraction.id,
            payload={
                "source_document_id": source_document.id,
                "fact_count": len(facts),
                "ai_provider": ai_resp.provider_id,
                "mode": ai_resp.mode
            }
        )

        return ExtractedFieldsEnvelope(
            extraction_id=extraction.id,
            source_document_id=source_document.id,
            extraction_method="AI_GATEWAY" if not ai_resp.is_mock else "TEXT_PARSER",
            sensitivity_level=source_document.security_classification,
            extracted_fields=facts
        )

    def detect_inconsistency_candidates(
        self,
        db: Session,
        bid_submission_id: str,
        actor_id: str = "SYSTEM"
    ) -> InconsistencyCandidateList:
        # Fetch submission documents
        docs = db.query(SourceDocument).filter_by(bid_submission_id=bid_submission_id).all()
        doc_ids = [d.id for d in docs]

        ai_req = AIGatewayRequest(
            task_type="INCONSISTENCY_DETECTION",
            task_id=f"TASK_INC_{bid_submission_id}",
            data_sensitivity_level="RESTRICTED",
            system_prompt_version="SP_INCONSISTENCY_DETECTION_v1.0",
            prompt_variables={"bid_submission_id": bid_submission_id, "document_ids": doc_ids},
            input_text_chunk=f"Document count: {len(docs)}"
        )

        ai_resp = ai_gateway.process_request(ai_req)
        raw_signals = ai_resp.structured_output.get("inconsistency_candidates", [])

        candidates = []
        for sig in raw_signals:
            cand = InconsistencyCandidateSchema(
                signal_code=sig.get("signal_code", "INC_GENERIC"),
                severity=sig.get("severity", "MEDIUM"),
                description=sig.get("description", "Candidate discrepancy detected across documents"),
                affected_document_ids=doc_ids if doc_ids else ["DOC01"],
                status="REQUIRES_HUMAN_REVIEW"
            )
            candidates.append(cand)

        # Audit event
        audit_service.log_event(
            db=db,
            actor_id=actor_id,
            actor_role="ServiceWorker",
            action="INCONSISTENCY_CANDIDATES_DETECTED",
            resource_type="BidSubmission",
            resource_id=bid_submission_id,
            payload={
                "signal_count": len(candidates),
                "bid_submission_id": bid_submission_id,
                "mode": ai_resp.mode
            }
        )

        return InconsistencyCandidateList(
            bid_submission_id=bid_submission_id,
            inconsistency_candidates=candidates
        )


bidder_intelligence_service = BidderIntelligenceService()
