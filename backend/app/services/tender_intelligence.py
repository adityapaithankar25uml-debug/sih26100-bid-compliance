from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.models.domain import SourceDocument, ExtractedField, DocumentExtraction
from app.services.ai_gateway import ai_gateway
from app.schemas.document_ai import AIGatewayRequest, TenderRequirementCandidateList, TenderRequirementCandidateSchema
from app.services.audit_service import audit_service


class TenderIntelligenceService:
    def extract_tender_requirement_candidates(
        self,
        db: Session,
        tender_id: str,
        source_document: SourceDocument,
        document_text: str,
        actor_id: str = "SYSTEM"
    ) -> TenderRequirementCandidateList:
        # Prepare AI Gateway Request
        ai_req = AIGatewayRequest(
            task_type="TENDER_REQUIREMENT_EXTRACTION",
            task_id=f"TASK_TENDER_{source_document.id}",
            data_sensitivity_level=source_document.security_classification,
            system_prompt_version="SP_TENDER_REQUIREMENT_EXTRACTION_v1.0",
            prompt_variables={"document_id": source_document.id, "tender_id": tender_id},
            input_text_chunk=document_text[:8000]
        )

        ai_resp = ai_gateway.process_request(ai_req)
        raw_candidates = ai_resp.structured_output.get("candidate_requirements", [])

        candidates = []
        for c in raw_candidates:
            cand = TenderRequirementCandidateSchema(
                candidate_code=c.get("candidate_code", "REQ-01"),
                category=c.get("category", "STATUTORY_COMPLIANCE"),
                description=c.get("description", ""),
                threshold_value=c.get("threshold_value"),
                unit=c.get("unit"),
                is_mandatory=c.get("is_mandatory", True),
                suggested_rule_code=c.get("suggested_rule_code"),
                source_document_id=source_document.id,
                page_number=c.get("page_number", 1),
                source_text_snippet=c.get("source_text_snippet"),
                extraction_confidence=c.get("extraction_confidence", 0.95),
                is_authoritative=False  # Strictly non-authoritative proposal
            )
            candidates.append(cand)

        # Audit event
        audit_service.log_event(
            db=db,
            actor_id=actor_id,
            actor_role="ServiceWorker",
            action="TENDER_REQUIREMENTS_EXTRACTED",
            resource_type="SourceDocument",
            resource_id=source_document.id,
            payload={
                "tender_id": tender_id,
                "candidate_count": len(candidates),
                "ai_provider": ai_resp.provider_id,
                "is_mock": ai_resp.is_mock,
                "mode": ai_resp.mode
            }
        )

        return TenderRequirementCandidateList(
            tender_id=tender_id,
            candidate_requirements=candidates
        )


tender_intelligence_service = TenderIntelligenceService()
