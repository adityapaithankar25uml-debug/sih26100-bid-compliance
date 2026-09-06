import datetime
from sqlalchemy import Column, String, DateTime
from app.db.session import Base
from app.core.security import generate_ulid


class BaseModelMixin:
    """
    Base mixin providing Crockford Base32 ULID primary key, timestamps, and classification tag.
    """
    id = Column(String(26), primary_key=True, default=generate_ulid, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False,
    )
    classification = Column(String(50), default="INTERNAL", nullable=False)
