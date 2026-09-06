"""002_document_intelligence

Revision ID: 002_document_intelligence
Revises: 001_initial_schema
Create Date: 2026-09-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from app.db.session import Base
import app.models  # Import models to populate Base.metadata

# revision identifiers, used by Alembic.
revision = '002_document_intelligence'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    pass
