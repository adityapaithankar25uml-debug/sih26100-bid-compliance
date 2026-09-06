"""003_government_verification_compliance

Revision ID: 003_government_verification_compliance
Revises: 002_document_intelligence
Create Date: 2026-09-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '003_government_verification_compliance'
down_revision = '002_document_intelligence'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'government_source_registries',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('source_code', sa.String(length=50), nullable=False),
        sa.Column('display_name', sa.String(length=255), nullable=False),
        sa.Column('authority_type', sa.String(length=100), nullable=False),
        sa.Column('verification_scope', sa.String(length=255), nullable=False),
        sa.Column('integration_mode', sa.String(length=50), nullable=False),
        sa.Column('readiness_status', sa.String(length=100), nullable=False),
        sa.Column('freshness_policy_days', sa.Integer(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('requires_consent', sa.Boolean(), nullable=False),
        sa.Column('manual_fallback_allowed', sa.Boolean(), nullable=False),
        sa.Column('documentation_reference', sa.String(length=500), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('source_code')
    )

    op.create_table(
        'government_verification_records',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('bid_submission_id', sa.String(length=26), sa.ForeignKey('bid_submissions.id'), nullable=True),
        sa.Column('bidder_id', sa.String(length=26), sa.ForeignKey('bidders.id'), nullable=True),
        sa.Column('source_code', sa.String(length=50), nullable=False),
        sa.Column('adapter_name', sa.String(length=100), nullable=False),
        sa.Column('integration_mode', sa.String(length=50), nullable=False),
        sa.Column('requested_at', sa.DateTime(), nullable=False),
        sa.Column('responded_at', sa.DateTime(), nullable=False),
        sa.Column('technical_status', sa.String(length=50), nullable=False),
        sa.Column('business_status', sa.String(length=50), nullable=False),
        sa.Column('source_authority_type', sa.String(length=100), nullable=False),
        sa.Column('freshness_status', sa.String(length=50), nullable=False),
        sa.Column('identity_match_status', sa.String(length=50), nullable=False),
        sa.Column('normalized_facts_json', sa.JSON(), nullable=False),
        sa.Column('raw_response_hash', sa.String(length=64), nullable=True),
        sa.Column('error_category', sa.String(length=100), nullable=True),
        sa.Column('is_manual_fallback', sa.Boolean(), nullable=False),
        sa.Column('manual_officer_id', sa.String(length=26), nullable=True),
        sa.Column('manual_notes', sa.Text(), nullable=True),
        sa.Column('manual_evidence_ref', sa.String(length=255), nullable=True),
        sa.Column('correlation_id', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'policy_versions',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('policy_code', sa.String(length=100), nullable=False),
        sa.Column('version', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('jurisdiction', sa.String(length=100), nullable=False),
        sa.Column('effective_from', sa.DateTime(), nullable=False),
        sa.Column('effective_to', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('source_reference', sa.String(length=500), nullable=True),
        sa.Column('policy_hash', sa.String(length=64), nullable=False),
        sa.Column('rules_config_json', sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('policy_code', 'version', name='uq_policy_code_version')
    )

    op.create_table(
        'compliance_rules',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('rule_code', sa.String(length=100), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('rule_type', sa.String(length=50), nullable=False),
        sa.Column('version', sa.String(length=50), nullable=False),
        sa.Column('policy_code', sa.String(length=100), nullable=False),
        sa.Column('policy_version', sa.String(length=50), nullable=False),
        sa.Column('effective_from', sa.DateTime(), nullable=False),
        sa.Column('effective_to', sa.DateTime(), nullable=True),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False),
        sa.Column('evaluation_expression_json', sa.JSON(), nullable=False),
        sa.Column('required_facts_json', sa.JSON(), nullable=False),
        sa.Column('explanation_template', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('rule_code')
    )

    op.create_table(
        'requirement_rule_mappings',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('tender_id', sa.String(length=26), sa.ForeignKey('tenders.id'), nullable=False),
        sa.Column('tender_version_id', sa.String(length=26), sa.ForeignKey('tender_versions.id'), nullable=False),
        sa.Column('requirement_id', sa.String(length=26), sa.ForeignKey('tender_requirements.id'), nullable=False),
        sa.Column('rule_id', sa.String(length=26), sa.ForeignKey('compliance_rules.id'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'compliance_facts',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('bid_submission_id', sa.String(length=26), sa.ForeignKey('bid_submissions.id'), nullable=False),
        sa.Column('fact_code', sa.String(length=100), nullable=False),
        sa.Column('fact_value', sa.JSON(), nullable=False),
        sa.Column('fact_status', sa.String(length=50), nullable=False),
        sa.Column('provenance_ref', sa.String(length=500), nullable=False),
        sa.Column('verification_record_id', sa.String(length=26), sa.ForeignKey('government_verification_records.id'), nullable=True),
        sa.Column('extracted_field_id', sa.String(length=26), sa.ForeignKey('extracted_fields.id'), nullable=True),
        sa.Column('retrieved_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'compliance_evaluations',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('bid_submission_id', sa.String(length=26), sa.ForeignKey('bid_submissions.id'), nullable=False),
        sa.Column('tender_id', sa.String(length=26), sa.ForeignKey('tenders.id'), nullable=False),
        sa.Column('tender_version_id', sa.String(length=26), sa.ForeignKey('tender_versions.id'), nullable=False),
        sa.Column('policy_version_id', sa.String(length=26), sa.ForeignKey('policy_versions.id'), nullable=True),
        sa.Column('evaluation_status', sa.String(length=50), nullable=False),
        sa.Column('overall_qualification_recommendation', sa.String(length=50), nullable=False),
        sa.Column('evaluation_trace_json', sa.JSON(), nullable=False),
        sa.Column('evaluated_at', sa.DateTime(), nullable=False),
        sa.Column('evaluator_id', sa.String(length=26), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'compliance_rule_results',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('evaluation_id', sa.String(length=26), sa.ForeignKey('compliance_evaluations.id'), nullable=False),
        sa.Column('rule_id', sa.String(length=26), sa.ForeignKey('compliance_rules.id'), nullable=False),
        sa.Column('rule_code', sa.String(length=100), nullable=False),
        sa.Column('requirement_id', sa.String(length=26), sa.ForeignKey('tender_requirements.id'), nullable=True),
        sa.Column('result_status', sa.String(length=50), nullable=False),
        sa.Column('evaluation_trace_json', sa.JSON(), nullable=False),
        sa.Column('explanation_text', sa.Text(), nullable=False),
        sa.Column('fact_values_json', sa.JSON(), nullable=False),
        sa.Column('evidence_refs_json', sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'human_review_tasks',
        sa.Column('id', sa.String(length=26), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('bid_submission_id', sa.String(length=26), sa.ForeignKey('bid_submissions.id'), nullable=False),
        sa.Column('document_id', sa.String(length=26), sa.ForeignKey('source_documents.id'), nullable=True),
        sa.Column('verification_record_id', sa.String(length=26), sa.ForeignKey('government_verification_records.id'), nullable=True),
        sa.Column('evaluation_id', sa.String(length=26), sa.ForeignKey('compliance_evaluations.id'), nullable=True),
        sa.Column('review_reason', sa.String(length=255), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('assigned_officer_id', sa.String(length=26), nullable=True),
        sa.Column('decision', sa.String(length=50), nullable=True),
        sa.Column('comments', sa.Text(), nullable=True),
        sa.Column('decided_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('human_review_tasks')
    op.drop_table('compliance_rule_results')
    op.drop_table('compliance_evaluations')
    op.drop_table('compliance_facts')
    op.drop_table('requirement_rule_mappings')
    op.drop_table('compliance_rules')
    op.drop_table('policy_versions')
    op.drop_table('government_verification_records')
    op.drop_table('government_source_registries')
