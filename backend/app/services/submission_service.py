from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.domain import BidSubmission, SubmissionCover, SourceDocument
from app.schemas.domain import SubmissionCreate, DocumentRegisterRequest


class BidSubmissionService:

    @staticmethod
    def create_submission(db: Session, sub_in: SubmissionCreate) -> BidSubmission:
        submission = BidSubmission(
            bidder_id=sub_in.bidder_id,
            tender_id=sub_in.tender_id,
            tender_version_id=sub_in.tender_version_id,
            submission_reference=sub_in.submission_reference,
            status="SUBMITTED",
        )
        db.add(submission)
        db.flush()

        # Create submission cover
        cover = SubmissionCover(
            bid_submission_id=submission.id,
            cover_type=sub_in.cover_type,
            document_count=0,
            remarks=f"Primary {sub_in.cover_type} cover",
        )
        db.add(cover)
        db.commit()
        db.refresh(submission)
        return submission

    @staticmethod
    def get_submission_by_id(db: Session, submission_id: str) -> Optional[BidSubmission]:
        return db.query(BidSubmission).filter(BidSubmission.id == submission_id).first()

    @staticmethod
    def list_submissions(
        db: Session, tender_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[BidSubmission]:
        query = db.query(BidSubmission)
        if tender_id:
            query = query.filter(BidSubmission.tender_id == tender_id)
        return query.order_by(BidSubmission.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def register_document(db: Session, doc_in: DocumentRegisterRequest) -> SourceDocument:
        document = SourceDocument(
            bid_submission_id=doc_in.bid_submission_id,
            submission_cover_id=doc_in.submission_cover_id,
            original_filename=doc_in.original_filename,
            content_type=doc_in.content_type,
            file_size_bytes=doc_in.file_size_bytes,
            sha256_hash=doc_in.sha256_hash,
            storage_ref=doc_in.storage_ref,
            upload_status="REGISTERED",
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
