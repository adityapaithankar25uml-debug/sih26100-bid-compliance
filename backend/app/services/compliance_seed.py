import hashlib
import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session

from app.models.domain import (
    GovernmentSourceRegistry,
    PolicyVersion,
    ComplianceRule,
    TenderRequirement,
    RequirementRuleMapping
)
from app.services.government_adapters import adapter_registry


def seed_phase4_compliance_framework(db: Session):
    """
    Seeds initial government sources, policy versioning, and default deterministic compliance rules.
    """
    # 1. Seed Government Source Registries
    sources_data = [
        ("GST", "GSTIN Tax Portal", "GSTN_TAX_AUTHORITY", "GST Registration & Tax Return Status", "MOCK", "MOCK_ONLY", 30),
        ("UDYAM", "Udyam MSME Portal", "MSME_MINISTRY", "Udyam Registration & Enterprise Category", "MOCK", "MOCK_ONLY", 60),
        ("PAN", "Income Tax Department", "INCOME_TAX_DEPARTMENT", "PAN Card & Taxpayer Identity", "MOCK", "MOCK_ONLY", 90),
        ("MCA", "Ministry of Corporate Affairs", "MINISTRY_OF_CORPORATE_AFFAIRS", "CIN & Company Incorporation Status", "MOCK", "MOCK_ONLY", 90),
        ("EPFO", "Employees Provident Fund Org", "EPFO_LABOUR_MINISTRY", "PF Establishment & Subscriber Count", "MOCK", "MOCK_ONLY", 30),
        ("ESIC", "Employees State Insurance Corp", "ESIC_LABOUR_MINISTRY", "ESI Establishment Registration", "MOCK", "MOCK_ONLY", 30),
        ("STARTUP_INDIA", "DPIIT Startup India Portal", "DPIIT_COMMERCE_MINISTRY", "Startup Recognition & Exemption", "MOCK", "MOCK_ONLY", 90),
        ("NSIC", "National Small Industries Corp", "NATIONAL_SMALL_INDUSTRIES_CORP", "Single Point Registration & Exemption", "MOCK", "MOCK_ONLY", 60),
        ("OEM_AUTH", "OEM Vendor Registry", "OEM_VENDOR_REGISTRY", "Manufacturer Authorization Certificate", "MOCK", "MOCK_ONLY", 30),
        ("DEBARMENT", "GeM Administrative Portal", "GEM_CPPP_ADMINISTRATIVE_AUTHORITY", "Blacklisting & Debarment History", "MOCK", "MOCK_ONLY", 7),
        ("GEM_PROFILE", "GeM Portal Profile", "GEM_PROCUREMENT_PORTAL", "Verified Seller Status & Rating", "MOCK", "MOCK_ONLY", 15),
        ("DIGILOCKER", "MeitY DigiLocker", "MEITY_DIGILOCKER_ISSUER", "Consent-based Document Issuer", "MOCK", "MOCK_ONLY", 30),
    ]

    for s_code, d_name, auth, scope, mode, status, days in sources_data:
        existing = db.query(GovernmentSourceRegistry).filter_by(source_code=s_code).first()
        if not existing:
            sr = GovernmentSourceRegistry(
                source_code=s_code,
                display_name=d_name,
                authority_type=auth,
                verification_scope=scope,
                integration_mode=mode,
                readiness_status=status,
                freshness_policy_days=days,
                enabled=True
            )
            db.add(sr)

    # 2. Seed Policy Version
    p_code = "POL_GEM_COMPLIANCE_2026"
    p_ver = "1.0"
    p_existing = db.query(PolicyVersion).filter_by(policy_code=p_code, version=p_ver).first()
    if not p_existing:
        pv = PolicyVersion(
            policy_code=p_code,
            version=p_ver,
            title="GeM General Financial & Statutory Procurement Policy 2026",
            jurisdiction="INDIA_GEM",
            effective_from=datetime.datetime(2026, 1, 1),
            status="ACTIVE",
            source_reference="Ministry of Finance / GeM GTC 2026",
            policy_hash=hashlib.sha256(b"POL_GEM_COMPLIANCE_2026_v1.0").hexdigest(),
            rules_config_json={"make_in_india_class1_min_percentage": 50.0}
        )
        db.add(pv)

    db.commit()

    # 3. Seed Deterministic Compliance Rules
    rules_defs = [
        {
            "rule_code": "RULE_GST_ACTIVE",
            "name": "Active GST Registration Requirement",
            "description": "Verifies that the bidder possesses an active GST registration from GSTN tax authority.",
            "rule_type": "BOOLEAN_FACT",
            "policy_code": p_code,
            "policy_version": p_ver,
            "severity": "MANDATORY",
            "evaluation_expression_json": {
                "operator": "equals",
                "field": "GST_GST_STATUS",
                "value": "ACTIVE"
            },
            "required_facts_json": ["GST_GST_STATUS"],
            "explanation_template": "Bidder GST registration status must be ACTIVE."
        },
        {
            "rule_code": "RULE_DEBARMENT_CHECK",
            "name": "Non-Debarment & Non-Blacklisting Requirement",
            "description": "Verifies that the bidder is NOT debarred or blacklisted by GeM, CPPP, or MoPNG/CPCL.",
            "rule_type": "ENUM_MATCH",
            "policy_code": p_code,
            "policy_version": p_ver,
            "severity": "CRITICAL",
            "evaluation_expression_json": {
                "operator": "equals",
                "field": "DEBARMENT_DEBARMENT_STATUS",
                "value": "NOT_DEBARRED"
            },
            "required_facts_json": ["DEBARMENT_DEBARMENT_STATUS"],
            "explanation_template": "Bidder must not be debarred by any government procurement authority."
        },
        {
            "rule_code": "RULE_UDYAM_MSME",
            "name": "MSME / Udyam Active Status Verification",
            "description": "Verifies active Udyam registration status for MSME benefit eligibility.",
            "rule_type": "BOOLEAN_FACT",
            "policy_code": p_code,
            "policy_version": p_ver,
            "severity": "CONDITIONAL",
            "evaluation_expression_json": {
                "operator": "equals",
                "field": "UDYAM_MSME_STATUS",
                "value": "ACTIVE"
            },
            "required_facts_json": ["UDYAM_MSME_STATUS"],
            "explanation_template": "Bidder MSME status must be ACTIVE for procurement concessions."
        },
        {
            "rule_code": "RULE_TURNOVER_THRESHOLD",
            "name": "Minimum Annual Financial Turnover Threshold",
            "description": "Verifies bidder turnover meets minimum required tender threshold.",
            "rule_type": "NUMERIC_THRESHOLD",
            "policy_code": p_code,
            "policy_version": p_ver,
            "severity": "MANDATORY",
            "evaluation_expression_json": {
                "operator": "greater_than_or_equal",
                "field": "ANNUAL_TURNOVER_FY24",
                "value": 500000000  # Rs 50 Cr
            },
            "required_facts_json": ["ANNUAL_TURNOVER_FY24"],
            "explanation_template": "Bidder turnover must equal or exceed Rs 50 Crores."
        },
        {
            "rule_code": "RULE_MAKE_IN_INDIA",
            "name": "Make In India Local Content Class-I Requirement",
            "description": "Verifies local content percentage meets Class-I supplier threshold (>= 50%).",
            "rule_type": "PERCENTAGE_THRESHOLD",
            "policy_code": p_code,
            "policy_version": p_ver,
            "severity": "MANDATORY",
            "evaluation_expression_json": {
                "operator": "greater_than_or_equal",
                "field": "LOCAL_CONTENT_PERCENTAGE",
                "value": 50.0
            },
            "required_facts_json": ["LOCAL_CONTENT_PERCENTAGE"],
            "explanation_template": "Local content percentage must be >= 50% for Class-I Local Supplier preference."
        },
        {
            "rule_code": "RULE_OEM_AUTHORIZATION",
            "name": "OEM Authorization Certificate Validity",
            "description": "Verifies valid OEM authorization code and manufacturer certificate status.",
            "rule_type": "ENUM_MATCH",
            "policy_code": p_code,
            "policy_version": p_ver,
            "severity": "MANDATORY",
            "evaluation_expression_json": {
                "operator": "equals",
                "field": "OEM_AUTH_AUTHORIZATION_STATUS",
                "value": "VALID"
            },
            "required_facts_json": ["OEM_AUTH_AUTHORIZATION_STATUS"],
            "explanation_template": "OEM Authorization Certificate status must be VALID."
        }
    ]

    for r_def in rules_defs:
        r_code = r_def["rule_code"]
        existing_r = db.query(ComplianceRule).filter_by(rule_code=r_code).first()
        if not existing_r:
            cr = ComplianceRule(**r_def)
            db.add(cr)

    db.commit()


# Alias for backward compatibility / smoke test compatibility
seed_phase4_defaults = seed_phase4_compliance_framework

