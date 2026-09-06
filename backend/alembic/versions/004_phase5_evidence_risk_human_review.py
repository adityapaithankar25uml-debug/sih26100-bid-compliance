"""004_phase5_evidence_risk_human_review

Revision ID: 004_phase5_evidence_risk_human_review
Revises: 003_government_verification_compliance
Create Date: 2026-09-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '004_phase5_evidence_risk_human_review'
down_revision = '003_government_verification_compliance'
branch_labels = None
depends_on = None


def upgrade():
    # Create evaluation_snapshots table
    op.create_table(
        'evaluation_snapshots',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('bid_submission_id', sa.String(length=26), sa.ForeignKey('bid_submissions.id'), nullable=False),
        sa.Column('tender_version_id', sa.String(length=26), sa.ForeignKey('tender_versions.id'), nullable=True),
        sa.Column('policy_version_id', sa.String(length=26), sa.ForeignKey('policy_versions.id'), nullable=True),
        sa.Column('evaluation_id', sa.String(length=26), sa.ForeignKey('compliance_evaluations.id'), nullable=True),
        sa.Column('snapshot_data_json', sa.JSON(), nullable=False),
        sa.Column('snapshot_hash', sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_evaluation_snapshots_bid_submission_id', 'evaluation_snapshots', ['bid_submission_id'])
    op.create_index('ix_evaluation_snapshots_snapshot_hash', 'evaluation_snapshots', ['snapshot_hash'])

    # Add columns to evidence_records
    with op.batch_alter_table('evidence_records') as batch_op:
        batch_op.add_column(sa.Column('bid_submission_id', sa.String(length=26), sa.ForeignKey('bid_submissions.id'), nullable=True))
        batch_op.add_column(sa.Column('requirement_id', sa.String(length=26), sa.ForeignKey('tender_requirements.id'), nullable=True))
        batch_op.add_column(sa.Column('rule_id', sa.String(length=26), sa.ForeignKey('compliance_rules.id'), nullable=True))
        batch_op.add_column(sa.Column('policy_version_id', sa.String(length=26), sa.ForeignKey('policy_versions.id'), nullable=True))
        batch_op.add_column(sa.Column('verification_record_id', sa.String(length=26), sa.ForeignKey('government_verification_records.id'), nullable=True))
        batch_op.add_column(sa.Column('evidence_quality_json', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('status', sa.String(length=50), server_default='VALID', nullable=False))
        batch_op.add_column(sa.Column('security_classification', sa.String(length=50), server_default='INTERNAL', nullable=False))
        batch_op.add_column(sa.Column('provenance_metadata_json', sa.JSON(), nullable=True))

    # Add columns to risk_assessment_profiles
    with op.batch_alter_table('risk_assessment_profiles') as batch_op:
        batch_op.add_column(sa.Column('profile_version', sa.String(length=50), server_default='1.0.0', nullable=False))

    # Add columns to officer_decisions
    with op.batch_alter_table('officer_decisions') as batch_op:
        batch_op.add_column(sa.Column('tender_id', sa.String(length=26), sa.ForeignKey('tenders.id'), nullable=True))
        batch_op.add_column(sa.Column('tender_version_id', sa.String(length=26), sa.ForeignKey('tender_versions.id'), nullable=True))
        batch_op.add_column(sa.Column('bidder_id', sa.String(length=26), sa.ForeignKey('bidders.id'), nullable=True))
        batch_op.add_column(sa.Column('evaluation_snapshot_id', sa.String(length=26), nullable=True))
        batch_op.add_column(sa.Column('risk_profile_id', sa.String(length=26), sa.ForeignKey('risk_assessment_profiles.id'), nullable=True))
        batch_op.add_column(sa.Column('audit_event_id', sa.String(length=26), sa.ForeignKey('audit_events.id'), nullable=True))

    # Add columns to manual_overrides
    with op.batch_alter_table('manual_overrides') as batch_op:
        batch_op.add_column(sa.Column('bid_submission_id', sa.String(length=26), sa.ForeignKey('bid_submissions.id'), nullable=True))
        batch_op.add_column(sa.Column('rule_id', sa.String(length=26), sa.ForeignKey('compliance_rules.id'), nullable=True))
        batch_op.add_column(sa.Column('override_reason_code', sa.String(length=100), server_default='OFFICER_REVIEW', nullable=True))
        batch_op.add_column(sa.Column('supporting_evidence_refs_json', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('requires_four_eyes', sa.Boolean(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('approved_by_officer_id', sa.String(length=26), sa.ForeignKey('users.id'), nullable=True))
        batch_op.add_column(sa.Column('four_eyes_status', sa.String(length=50), server_default='APPROVED', nullable=False))

    # Add columns to human_review_tasks
    with op.batch_alter_table('human_review_tasks') as batch_op:
        batch_op.add_column(sa.Column('tender_id', sa.String(length=26), sa.ForeignKey('tenders.id'), nullable=True))
        batch_op.add_column(sa.Column('tender_requirement_id', sa.String(length=26), sa.ForeignKey('tender_requirements.id'), nullable=True))
        batch_op.add_column(sa.Column('bidder_id', sa.String(length=26), sa.ForeignKey('bidders.id'), nullable=True))
        batch_op.add_column(sa.Column('policy_version_id', sa.String(length=26), sa.ForeignKey('policy_versions.id'), nullable=True))
        batch_op.add_column(sa.Column('review_code', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('priority', sa.String(length=50), server_default='MEDIUM', nullable=False))
        batch_op.add_column(sa.Column('suggested_action', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('resolution_summary', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('evidence_refs_json', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('review_history_json', sa.JSON(), nullable=True))


def downgrade():
    with op.batch_alter_table('human_review_tasks') as batch_op:
        batch_op.drop_column('review_history_json')
        batch_op.drop_column('evidence_refs_json')
        batch_op.drop_column('resolution_summary')
        batch_op.drop_column('suggested_action')
        batch_op.drop_column('priority')
        batch_op.drop_column('review_code')
        batch_op.drop_column('policy_version_id')
        batch_op.drop_column('bidder_id')
        batch_op.drop_column('tender_requirement_id')
        batch_op.drop_column('tender_id')

    with op.batch_alter_table('manual_overrides') as batch_op:
        batch_op.drop_column('four_eyes_status')
        batch_op.drop_column('approved_by_officer_id')
        batch_op.drop_column('requires_four_eyes')
        batch_op.drop_column('supporting_evidence_refs_json')
        batch_op.drop_column('override_reason_code')
        batch_op.drop_column('rule_id')
        batch_op.drop_column('bid_submission_id')

    with op.batch_alter_table('officer_decisions') as batch_op:
        batch_op.drop_column('audit_event_id')
        batch_op.drop_column('risk_profile_id')
        batch_op.drop_column('evaluation_snapshot_id')
        batch_op.drop_column('bidder_id')
        batch_op.drop_column('tender_version_id')
        batch_op.drop_column('tender_id')

    with op.batch_alter_table('risk_assessment_profiles') as batch_op:
        batch_op.drop_column('profile_version')

    with op.batch_alter_table('evidence_records') as batch_op:
        batch_op.drop_column('provenance_metadata_json')
        batch_op.drop_column('security_classification')
        batch_op.drop_column('status')
        batch_op.drop_column('evidence_quality_json')
        batch_op.drop_column('verification_record_id')
        batch_op.drop_column('policy_version_id')
        batch_op.drop_column('rule_id')
        batch_op.drop_column('requirement_id')
        batch_op.drop_column('bid_submission_id')

    op.drop_index('ix_evaluation_snapshots_snapshot_hash', table_name='evaluation_snapshots')
    op.drop_index('ix_evaluation_snapshots_bid_submission_id', table_name='evaluation_snapshots')
    op.drop_table('evaluation_snapshots')
