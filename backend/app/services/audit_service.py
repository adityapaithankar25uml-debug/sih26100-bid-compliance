import hashlib
import json
import datetime
from typing import Dict, Any, Tuple, Optional, List
from sqlalchemy.orm import Session
from app.models.domain import AuditEvent, AuditHashChainBlock


class AuditService:

    @staticmethod
    def canonicalize_payload(payload: Dict[str, Any]) -> str:
        """
        Produces a deterministic, canonical JSON string representation of an audit event payload.
        """
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def compute_sha256(data_str: str) -> str:
        """
        Computes SHA-256 hash string of an input text.
        """
        return hashlib.sha256(data_str.encode("utf-8")).hexdigest()

    @classmethod
    def log_event(
        cls,
        db: Session,
        actor_id: str,
        actor_role: str,
        action: str,
        resource_type: str,
        resource_id: str,
        correlation_id: str,
        payload: Dict[str, Any],
    ) -> AuditEvent:
        """
        Logs an auditable domain action, canonicalizes the payload, calculates SHA-256,
        and appends a new block to the Tamper-Evident Audit Hash Chain.
        """
        canonical_str = cls.canonicalize_payload(payload)
        payload_hash = cls.compute_sha256(canonical_str)

        audit_event = AuditEvent(
            actor_id=actor_id,
            actor_role=actor_role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            correlation_id=correlation_id,
            payload_hash=payload_hash,
            event_payload=payload,
        )
        db.add(audit_event)
        db.flush()

        # Fetch last hash block in chain
        last_block = (
            db.query(AuditHashChainBlock)
            .order_by(AuditHashChainBlock.block_index.desc())
            .first()
        )

        if last_block:
            previous_hash = last_block.current_hash
            block_index = last_block.block_index + 1
        else:
            previous_hash = "0" * 64  # Genesis block previous hash
            block_index = 0

        now_utc = datetime.datetime.utcnow()
        block_content = f"{previous_hash}:{payload_hash}:{block_index}:{now_utc.isoformat()}"
        current_hash = cls.compute_sha256(block_content)

        hash_block = AuditHashChainBlock(
            block_index=block_index,
            audit_event_id=audit_event.id,
            previous_hash=previous_hash,
            current_hash=current_hash,
            timestamp=now_utc,
        )
        db.add(hash_block)
        db.commit()
        db.refresh(audit_event)

        return audit_event

    @classmethod
    def verify_chain_integrity(cls, db: Session) -> Tuple[bool, int, int, Optional[int], str]:
        """
        Verifies the tamper-evident hash chain from block 0 to top.
        Returns: (is_valid, total_blocks, verified_blocks, first_corrupted_block, message)
        """
        blocks: List[AuditHashChainBlock] = (
            db.query(AuditHashChainBlock)
            .order_by(AuditHashChainBlock.block_index.asc())
            .all()
        )

        if not blocks:
            return True, 0, 0, None, "Audit chain is empty."

        expected_previous_hash = "0" * 64

        for index, block in enumerate(blocks):
            # 1. Verify previous hash link matches
            if block.previous_hash != expected_previous_hash:
                return (
                    False,
                    len(blocks),
                    index,
                    block.block_index,
                    f"Hash chain broken at block index {block.block_index}: previous_hash mismatch.",
                )

            # 2. Verify audit event payload hash match
            event = db.query(AuditEvent).filter(AuditEvent.id == block.audit_event_id).first()
            if not event:
                return (
                    False,
                    len(blocks),
                    index,
                    block.block_index,
                    f"Audit event missing for block index {block.block_index}.",
                )

            canonical_str = cls.canonicalize_payload(event.event_payload)
            expected_payload_hash = cls.compute_sha256(canonical_str)

            if event.payload_hash != expected_payload_hash:
                return (
                    False,
                    len(blocks),
                    index,
                    block.block_index,
                    f"Audit event payload altered at block index {block.block_index}: payload hash mismatch.",
                )

            # 3. Verify current block hash computation
            block_content = f"{block.previous_hash}:{event.payload_hash}:{block.block_index}:{block.timestamp.isoformat()}"
            recomputed_current_hash = cls.compute_sha256(block_content)

            if block.current_hash != recomputed_current_hash:
                return (
                    False,
                    len(blocks),
                    index,
                    block.block_index,
                    f"Block hash tampered at block index {block.block_index}: current_hash mismatch.",
                )

            expected_previous_hash = block.current_hash

        return True, len(blocks), len(blocks), None, "Audit hash chain integrity verified successfully."
