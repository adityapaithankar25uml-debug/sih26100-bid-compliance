"""001_initial_schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-06 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from app.db.session import Base
import app.models  # Import models to populate Base.metadata

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Use Base metadata to create all tables cleanly
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
