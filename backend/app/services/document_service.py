import hashlib
import os
import re
from typing import Tuple, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.domain import SourceDocument
from app.services.storage_service import storage_service
from app.services.malware_service import get_malware_scanner
from app.services.audit_service import audit_service


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".png", ".jpg", ".jpeg"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "image/png",
    "image/jpeg",
}

MAGIC_BYTES = {
    b"%PDF": "application/pdf",
    b"PK\x03\x04": "application/zip",  # Office docx/xlsx zip container
    b"\x89PNG": "image/png",
    b"\xff\xd8\xff": "image/jpeg",
}


class DocumentService:
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Protects against path traversal attacks."""
        basename = os.path.basename(filename)
        sanitized = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", basename)
        return sanitized or "unnamed_document.pdf"

    @staticmethod
    def validate_file_content(filename: str, content: bytes, content_type: str) -> Tuple[bool, str]:
        # 1. Path traversal check (raw filename)
        if ".." in filename or "/" in filename or "\\" in filename:
            return False, "Path traversal attempt detected in filename"

        # 2. Size check
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024 if hasattr(settings, "MAX_UPLOAD_SIZE_MB") else 25 * 1024 * 1024
        if len(content) > max_bytes:
            return False, f"File size exceeds maximum permitted limit of {max_bytes // (1024*1024)}MB"

        # 3. Extension check
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            return False, f"File extension '{ext}' is not supported"

        # 4. Magic bytes check
        matched = False
        for magic, expected_type in MAGIC_BYTES.items():
            if content.startswith(magic):
                matched = True
                break
        if not matched and len(content) > 0:
            return False, "File magic-byte signature validation failed"

        return True, "Validation successful"

    def upload_document(
        self,
        db: Session,
        bid_submission_id: str,
        filename: str,
        content: bytes,
        content_type: str,
        actor_id: str = "SYSTEM",
        submission_cover_id: Optional[str] = None,
        parent_document_id: Optional[str] = None,
    ) -> SourceDocument:
        # Validate raw filename first (path traversal, size, extension, magic bytes)
        is_valid, reason = self.validate_file_content(filename, content, content_type)
        if not is_valid:
            raise ValueError(f"Document Validation Error: {reason}")

        safe_filename = self.sanitize_filename(filename)


        # Compute SHA-256
        sha256 = hashlib.sha256(content).hexdigest()

        # Check duplicate sha256 in submission
        existing = db.query(SourceDocument).filter_by(
            bid_submission_id=bid_submission_id,
            sha256_hash=sha256
        ).first()
        if existing:
            return existing

        # Quarantine upload to MinIO
        quarantine_ref = f"quarantine/{bid_submission_id}/{sha256}_{safe_filename}"
        storage_service.upload_file(quarantine_ref, content, content_type)

        # Malware scan
        scanner = get_malware_scanner()
        scan_status, details = scanner.scan_document(safe_filename, content)

        quarantine_status = "VALIDATED" if scan_status == "CLEAN" else "REJECTED"
        upload_status = "VALIDATED" if scan_status == "CLEAN" else "REJECTED"

        # Move to processed storage if clean
        storage_ref = quarantine_ref
        if scan_status == "CLEAN":
            storage_ref = f"processed/{bid_submission_id}/{sha256}_{safe_filename}"
            storage_service.upload_file(storage_ref, content, content_type)

        doc = SourceDocument(
            bid_submission_id=bid_submission_id,
            submission_cover_id=submission_cover_id,
            original_filename=safe_filename,
            content_type=content_type,
            file_size_bytes=len(content),
            sha256_hash=sha256,
            storage_ref=storage_ref,
            upload_status=upload_status,
            security_classification="INTERNAL",
            quarantine_status=quarantine_status,
            malware_scan_result=scan_status,
            parent_document_id=parent_document_id,
            metadata_json={"scan_details": details, "quarantine_ref": quarantine_ref}
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)

        # Audit event
        audit_service.log_event(
            db=db,
            actor_id=actor_id,
            actor_role="ServiceWorker",
            action="DOCUMENT_UPLOADED",
            resource_type="SourceDocument",
            resource_id=doc.id,
            payload={
                "original_filename": safe_filename,
                "sha256_hash": sha256,
                "malware_scan_result": scan_status,
                "quarantine_status": quarantine_status,
                "security_classification": "INTERNAL",
            }
        )

        return doc


document_service = DocumentService()
