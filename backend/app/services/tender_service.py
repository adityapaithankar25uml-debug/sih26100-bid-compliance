from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.domain import Tender, TenderVersion, TenderRequirement
from app.schemas.domain import TenderCreate, RequirementCreate


class TenderService:

    @staticmethod
    def create_tender(db: Session, tender_in: TenderCreate) -> Tender:
        tender = Tender(
            tender_number=tender_in.tender_number,
            title=tender_in.title,
            organization=tender_in.organization,
            status="ACTIVE",
        )
        db.add(tender)
        db.flush()

        # Create initial TenderVersion 1
        version = TenderVersion(
            tender_id=tender.id,
            version_number=1,
            description=tender_in.description or "Initial tender version",
            is_finalized=True,
        )
        db.add(version)
        db.commit()
        db.refresh(tender)
        return tender

    @staticmethod
    def get_tender_by_id(db: Session, tender_id: str) -> Optional[Tender]:
        return db.query(Tender).filter(Tender.id == tender_id).first()

    @staticmethod
    def get_tender_by_number(db: Session, tender_number: str) -> Optional[Tender]:
        return db.query(Tender).filter(Tender.tender_number == tender_number).first()

    @staticmethod
    def list_tenders(db: Session, skip: int = 0, limit: int = 100) -> List[Tender]:
        return db.query(Tender).order_by(Tender.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def create_tender_version(
        db: Session, tender_id: str, description: Optional[str] = None
    ) -> Optional[TenderVersion]:
        tender = db.query(Tender).filter(Tender.id == tender_id).first()
        if not tender:
            return None

        # Get latest version number
        latest_version = (
            db.query(TenderVersion)
            .filter(TenderVersion.tender_id == tender_id)
            .order_by(TenderVersion.version_number.desc())
            .first()
        )
        next_ver_num = (latest_version.version_number + 1) if latest_version else 1

        new_version = TenderVersion(
            tender_id=tender_id,
            version_number=next_ver_num,
            description=description or f"Tender amendment version {next_ver_num}",
            is_finalized=True,
        )
        db.add(new_version)
        db.commit()
        db.refresh(new_version)
        return new_version

    @staticmethod
    def add_requirement(
        db: Session, tender_version_id: str, req_in: RequirementCreate
    ) -> TenderRequirement:
        requirement = TenderRequirement(
            tender_version_id=tender_version_id,
            requirement_code=req_in.requirement_code,
            category=req_in.category,
            requirement_text=req_in.requirement_text,
            is_mandatory=req_in.is_mandatory,
            metadata_json=req_in.metadata_json or {},
        )
        db.add(requirement)
        db.commit()
        db.refresh(requirement)
        return requirement

    @staticmethod
    def list_requirements_for_version(
        db: Session, tender_version_id: str
    ) -> List[TenderRequirement]:
        return (
            db.query(TenderRequirement)
            .filter(TenderRequirement.tender_version_id == tender_version_id)
            .order_by(TenderRequirement.requirement_code.asc())
            .all()
        )
