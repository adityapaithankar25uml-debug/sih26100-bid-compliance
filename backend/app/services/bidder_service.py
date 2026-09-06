import hashlib
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.domain import Bidder, BidderIdentity
from app.schemas.domain import BidderCreate


class BidderService:

    @staticmethod
    def create_bidder(db: Session, bidder_in: BidderCreate) -> Bidder:
        bidder = Bidder(
            bidder_name=bidder_in.bidder_name,
            registration_number=bidder_in.registration_number,
            entity_type=bidder_in.entity_type,
            organization_type=bidder_in.organization_type,
        )
        db.add(bidder)
        db.flush()

        # Compute synthetic identity hashes for PAN/GSTIN/UDYAM if provided
        pan_hash = (
            hashlib.sha256(bidder_in.pan.encode()).hexdigest()
            if bidder_in.pan
            else None
        )
        gstin_hash = (
            hashlib.sha256(bidder_in.gstin.encode()).hexdigest()
            if bidder_in.gstin
            else None
        )
        udyam_hash = (
            hashlib.sha256(bidder_in.udyam.encode()).hexdigest()
            if bidder_in.udyam
            else None
        )

        identity = BidderIdentity(
            bidder_id=bidder.id,
            pan_hash=pan_hash,
            gstin_hash=gstin_hash,
            udyam_hash=udyam_hash,
            verification_status="UNVERIFIED",
        )
        db.add(identity)
        db.commit()
        db.refresh(bidder)
        return bidder

    @staticmethod
    def get_bidder_by_id(db: Session, bidder_id: str) -> Optional[Bidder]:
        return db.query(Bidder).filter(Bidder.id == bidder_id).first()

    @staticmethod
    def list_bidders(db: Session, skip: int = 0, limit: int = 100) -> List[Bidder]:
        return db.query(Bidder).order_by(Bidder.created_at.desc()).offset(skip).limit(limit).all()
