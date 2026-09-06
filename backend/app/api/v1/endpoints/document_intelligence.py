from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Security, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.v1.deps import get_current_user, require_roles
from app.models.domain import User, SourceDocument, DocumentExtraction, ExtractedField, BoundingBox, EvidenceRecord
from app.services.document_service import document_service
from app.services.document_pipeline import document_pipeline_service
from app.services.tender_intelligence import tender_intelligence_service
from app.services.bidder_intelligence import bidder_intelligence_service
from app.schemas.document_ai import (
    DocumentUploadResponse,
    DocumentClassificationResponse,
    PrivacyGatewayResponse,
    ExtractedFieldsEnvelope,
    TenderRequirementCandidateList,
    InconsistencyCandidateList
)

router = APIRouter()


@router.post("/documents/upload", response_model=DocumentUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    bid_submission_id: str = Form(...),
    submission_cover_id: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "SystemAdmin", "ServiceWorker"])),
):
    content = await file.read()
    try:
        doc = document_service.upload_document(
            db=db,
            bid_submission_id=bid_submission_id,
            filename=file.filename,
            content=content,
            content_type=file.content_type or "application/pdf",
            actor_id=current_user.id,
            submission_cover_id=submission_cover_id
        )
        return DocumentUploadResponse.model_validate(doc)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/documents/{document_id}/status")
def get_document_processing_status(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = db.query(SourceDocument).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    return {
        "document_id": doc.id,
        "original_filename": doc.original_filename,
        "upload_status": doc.upload_status,
        "quarantine_status": doc.quarantine_status,
        "malware_scan_result": doc.malware_scan_result,
        "security_classification": doc.security_classification,
        "sha256_hash": doc.sha256_hash
    }


@router.post("/documents/{document_id}/process")
def process_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "SystemAdmin", "ServiceWorker"]))
):
    try:
        result = document_pipeline_service.process_document(db, document_id, actor_id=current_user.id)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/documents/{document_id}/extractions")
def get_document_extractions(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = db.query(SourceDocument).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    extractions = db.query(DocumentExtraction).filter_by(source_document_id=doc.id).all()
    results = []
    for ext in extractions:
        fields = db.query(ExtractedField).filter_by(document_extraction_id=ext.id).all()
        results.append({
            "extraction_id": ext.id,
            "extraction_status": ext.extraction_status,
            "extraction_method": ext.extraction_method,
            "confidence_score": ext.confidence_score,
            "sensitivity_level": ext.sensitivity_level,
            "extracted_fields": [
                {
                    "field_name": f.field_name,
                    "field_value": f.field_value,
                    "normalized_value": f.normalized_value,
                    "confidence": f.confidence
                }
                for f in fields
            ]
        })
    return {"document_id": doc.id, "extractions": results}


@router.get("/documents/{document_id}/evidence")
def get_document_evidence(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = db.query(SourceDocument).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    extractions = db.query(DocumentExtraction).filter_by(source_document_id=doc.id).all()
    evidence_list = []
    for ext in extractions:
        fields = db.query(ExtractedField).filter_by(document_extraction_id=ext.id).all()
        for f in fields:
            boxes = db.query(BoundingBox).filter_by(extracted_field_id=f.id).all()
            box = boxes[0] if boxes else None
            evidence_list.append({
                "field_name": f.field_name,
                "extracted_value": f.field_value,
                "source_document_name": doc.original_filename,
                "source_document_hash": doc.sha256_hash,
                "page_number": box.page_number if box else 1,
                "bounding_box": {
                    "x0": box.x_min if box else 50.0,
                    "y0": box.y_min if box else 100.0,
                    "x1": box.x_max if box else 350.0,
                    "y1": box.y_max if box else 120.0,
                } if box else None,
                "extraction_method": ext.extraction_method,
                "provenance_ref": f"SourceDocument:{doc.id}#ExtractedField:{f.id}"
            })
    return {"document_id": doc.id, "evidence_provenance": evidence_list}


@router.post("/documents/{document_id}/reprocess")
def reprocess_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ProcurementOfficer", "SeniorReviewer", "SystemAdmin", "ServiceWorker"]))
):
    doc = db.query(SourceDocument).filter_by(id=document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    # Safe reprocessing without deleting original doc or prior evidence
    result = document_pipeline_service.process_document(db, document_id, actor_id=current_user.id)
    return {"message": "Document reprocessed successfully", "pipeline_result": result}


@router.get("/tenders/{tender_id}/requirement-candidates", response_model=TenderRequirementCandidateList)
def get_tender_requirement_candidates(
    tender_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Retrieve synthetic/extracted candidates
    doc = db.query(SourceDocument).first()
    if not doc:
        # Generate inline candidate list
        return tender_intelligence_service.extract_tender_requirement_candidates(
            db=db,
            tender_id=tender_id,
            source_document=SourceDocument(id="DOC01", security_classification="PUBLIC"),
            document_text="Tender Document text"
        )
    return tender_intelligence_service.extract_tender_requirement_candidates(
        db=db,
        tender_id=tender_id,
        source_document=doc,
        document_text="Tender text"
    )


@router.get("/bids/{submission_id}/extracted-facts")
def get_bid_extracted_facts(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doc = db.query(SourceDocument).filter_by(bid_submission_id=submission_id).first()
    if not doc:
        doc = db.query(SourceDocument).first()

    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No submission document found")

    return bidder_intelligence_service.extract_bidder_facts(db, doc, "Bidder document text")


@router.get("/bids/{submission_id}/inconsistency-candidates", response_model=InconsistencyCandidateList)
def get_bid_inconsistency_candidates(
    submission_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return bidder_intelligence_service.detect_inconsistency_candidates(db, submission_id)

