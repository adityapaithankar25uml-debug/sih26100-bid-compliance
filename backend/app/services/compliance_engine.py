import datetime
import hashlib
import uuid
from typing import Dict, Any, List, Tuple, Optional
from sqlalchemy.orm import Session

from app.models.domain import (
    ComplianceRule,
    PolicyVersion,
    ComplianceFact,
    ComplianceEvaluation,
    ComplianceRuleResult,
    TenderRequirement,
    RequirementRuleMapping,
    SourceDocument,
    ExtractedField,
    GovernmentVerificationRecord,
    HumanReviewTask
)
from app.services.audit_service import audit_service


class ASTExecutionError(ValueError):
    """Exception raised when an invalid or unsafe AST expression is encountered."""
    pass


class ConstrainedRuleEvaluator:
    """
    Deterministic AST Rule Evaluator.
    STRICTLY PROHIBITS eval(), exec(), IMPORTS, AND ARBITRARY PYTHON CODE EXECUTION.
    Evaluates JSON-structured logic trees.
    """

    @classmethod
    def evaluate_node(cls, node: Dict[str, Any], facts: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
        if not isinstance(node, dict):
            raise ASTExecutionError(f"Invalid rule node structure: expected dict, got {type(node)}")

        operator = node.get("operator", "").lower()

        if operator == "equals":
            field = node.get("field")
            expected = node.get("value")
            actual = facts.get(field)
            passed = (actual == expected)
            trace = {"field": field, "actual": actual, "expected": expected, "operator": "=="}
            msg = f"Fact '{field}' ({actual}) == expected '{expected}'" if passed else f"Fact '{field}' ({actual}) != expected '{expected}'"
            return passed, msg, trace

        elif operator == "not_equals":
            field = node.get("field")
            expected = node.get("value")
            actual = facts.get(field)
            passed = (actual != expected)
            trace = {"field": field, "actual": actual, "expected": expected, "operator": "!="}
            msg = f"Fact '{field}' ({actual}) != '{expected}'" if passed else f"Fact '{field}' ({actual}) == '{expected}'"
            return passed, msg, trace

        elif operator == "greater_than_or_equal":
            field = node.get("field")
            expected = float(node.get("value", 0))
            raw_val = facts.get(field)
            if raw_val is None:
                return False, f"Fact '{field}' is missing", {"field": field, "actual": None, "expected": expected}
            try:
                actual = float(raw_val)
            except (ValueError, TypeError):
                return False, f"Fact '{field}' value '{raw_val}' is not numeric", {"field": field, "actual": raw_val, "expected": expected}
            passed = (actual >= expected)
            trace = {"field": field, "actual": actual, "expected": expected, "operator": ">="}
            msg = f"Fact '{field}' ({actual}) >= required threshold ({expected})" if passed else f"Fact '{field}' ({actual}) < required threshold ({expected})"
            return passed, msg, trace

        elif operator == "less_than_or_equal":
            field = node.get("field")
            expected = float(node.get("value", 0))
            raw_val = facts.get(field)
            if raw_val is None:
                return False, f"Fact '{field}' is missing", {"field": field, "actual": None, "expected": expected}
            try:
                actual = float(raw_val)
            except (ValueError, TypeError):
                return False, f"Fact '{field}' value '{raw_val}' is not numeric", {"field": field, "actual": raw_val, "expected": expected}
            passed = (actual <= expected)
            trace = {"field": field, "actual": actual, "expected": expected, "operator": "<="}
            msg = f"Fact '{field}' ({actual}) <= threshold ({expected})" if passed else f"Fact '{field}' ({actual}) > threshold ({expected})"
            return passed, msg, trace

        elif operator == "is_true":
            field = node.get("field")
            val = facts.get(field)
            passed = bool(val is True or str(val).lower() in ("true", "active", "1", "yes", "verified"))
            trace = {"field": field, "actual": val, "operator": "is_true"}
            msg = f"Fact '{field}' is True" if passed else f"Fact '{field}' is False/Missing"
            return passed, msg, trace

        elif operator == "is_not_empty":
            field = node.get("field")
            val = facts.get(field)
            passed = bool(val is not None and str(val).strip() != "")
            trace = {"field": field, "actual": val, "operator": "is_not_empty"}
            msg = f"Fact '{field}' is present" if passed else f"Fact '{field}' is empty or missing"
            return passed, msg, trace

        elif operator == "in_list":
            field = node.get("field")
            allowed = node.get("values", [])
            val = facts.get(field)
            passed = (val in allowed)
            trace = {"field": field, "actual": val, "allowed": allowed, "operator": "in"}
            msg = f"Fact '{field}' ({val}) is in permitted list {allowed}" if passed else f"Fact '{field}' ({val}) is not in permitted list {allowed}"
            return passed, msg, trace

        elif operator == "all":
            conditions = node.get("conditions", [])
            sub_results = []
            sub_traces = []
            all_pass = True
            for cond in conditions:
                p, m, t = cls.evaluate_node(cond, facts)
                sub_results.append(m)
                sub_traces.append(t)
                if not p:
                    all_pass = False
            msg = "ALL conditions satisfied" if all_pass else f"Condition failed: {'; '.join(sub_results)}"
            return all_pass, msg, {"operator": "all", "sub_traces": sub_traces}

        elif operator == "any":
            conditions = node.get("conditions", [])
            sub_results = []
            sub_traces = []
            any_pass = False
            for cond in conditions:
                p, m, t = cls.evaluate_node(cond, facts)
                sub_results.append(m)
                sub_traces.append(t)
                if p:
                    any_pass = True
            msg = "ANY condition satisfied" if any_pass else "NO conditions satisfied"
            return any_pass, msg, {"operator": "any", "sub_traces": sub_traces}

        elif operator == "not":
            cond = node.get("condition", {})
            p, m, t = cls.evaluate_node(cond, facts)
            passed = not p
            return passed, f"NOT ({m})", {"operator": "not", "sub_trace": t}

        else:
            raise ASTExecutionError(f"Unsupported AST operator: '{operator}'. Unsafe execution blocked.")


class ComplianceEngine:
    def collect_facts_for_submission(self, db: Session, bid_submission_id: str) -> Tuple[Dict[str, Any], Dict[str, str]]:
        """
        Collects normalized facts from ComplianceFact entries and extracted fields.
        Returns: (fact_dictionary, provenance_dictionary)
        """
        facts: Dict[str, Any] = {}
        provenance: Dict[str, str] = {}

        # 1. Fact entries from government verification
        c_facts = db.query(ComplianceFact).filter_by(bid_submission_id=bid_submission_id).all()
        for cf in c_facts:
            code = cf.fact_code.upper()
            val = cf.fact_value.get("value") if isinstance(cf.fact_value, dict) else cf.fact_value
            facts[code] = val
            provenance[code] = cf.provenance_ref

        # 2. Extracted fields from Phase 3 document intelligence
        docs = db.query(SourceDocument).filter_by(bid_submission_id=bid_submission_id).all()
        for d in docs:
            for ext in d.extractions:
                for field in ext.fields:
                    fname = field.field_name.upper()
                    if fname not in facts:
                        facts[fname] = field.normalized_value or field.field_value
                        provenance[fname] = f"SourceDocument:{d.id}#ExtractedField:{field.id}"

        return facts, provenance

    def evaluate_rule(
        self,
        rule: ComplianceRule,
        facts: Dict[str, Any],
        provenance: Dict[str, str]
    ) -> Tuple[str, str, Dict[str, Any], List[str]]:
        """
        Evaluates a single compliance rule against collected facts.
        Returns: (result_status, explanation_text, evaluation_trace, evidence_refs)
        """
        req_facts = rule.required_facts_json or []
        evidence_refs = []
        missing_facts = []

        for rf in req_facts:
            rf_upper = rf.upper()
            if rf_upper in provenance:
                evidence_refs.append(provenance[rf_upper])
            if rf_upper not in facts or facts[rf_upper] is None:
                missing_facts.append(rf)

        # Rule Invariant: MISSING EVIDENCE IS NOT A FAIL
        if missing_facts:
            expl = f"Rule '{rule.name}' evaluation deferred: Required evidence for facts {missing_facts} is missing."
            trace = {"status": "MISSING_EVIDENCE", "missing_facts": missing_facts, "facts_provided": list(facts.keys())}
            return "MISSING_EVIDENCE", expl, trace, evidence_refs

        try:
            passed, msg, trace = ConstrainedRuleEvaluator.evaluate_node(rule.evaluation_expression_json, facts)
            status = "PASS" if passed else "FAIL"
            expl = f"Rule '{rule.name}' {status}: {msg}"
            return status, expl, trace, evidence_refs
        except ASTExecutionError as exc:
            return "UNKNOWN", f"AST Evaluation Error: {str(exc)}", {"error": str(exc)}, evidence_refs

    def evaluate_bid_submission(
        self,
        db: Session,
        bid_submission_id: str,
        tender_id: str,
        tender_version_id: str,
        policy_code: str = "POL_GEM_COMPLIANCE_2026",
        evaluator_id: str = "SYSTEM"
    ) -> ComplianceEvaluation:
        # Bind policy version
        policy_ver = db.query(PolicyVersion).filter_by(policy_code=policy_code, status="ACTIVE").first()
        policy_ver_id = policy_ver.id if policy_ver else None

        # Collect facts
        facts, provenance = self.collect_facts_for_submission(db, bid_submission_id)

        # Fetch active rules for tender requirements
        mappings = db.query(RequirementRuleMapping).filter_by(
            tender_id=tender_id,
            tender_version_id=tender_version_id,
            is_active=True
        ).all()

        rule_results_data = []
        overall_status = "COMPLIANT"
        review_reasons = []

        if not mappings:
            # Fallback to default active rules
            rules = db.query(ComplianceRule).filter_by(enabled=True).all()
            for r in rules:
                res_status, expl, trace, ev_refs = self.evaluate_rule(r, facts, provenance)
                rule_results_data.append({
                    "rule": r,
                    "requirement_id": None,
                    "result_status": res_status,
                    "explanation": expl,
                    "trace": trace,
                    "evidence_refs": ev_refs
                })
        else:
            for m in mappings:
                r = db.query(ComplianceRule).filter_by(id=m.rule_id).first()
                if r and r.enabled:
                    res_status, expl, trace, ev_refs = self.evaluate_rule(r, facts, provenance)
                    rule_results_data.append({
                        "rule": r,
                        "requirement_id": m.requirement_id,
                        "result_status": res_status,
                        "explanation": expl,
                        "trace": trace,
                        "evidence_refs": ev_refs
                    })

        # Aggregate overall status
        has_fail = any(rd["result_status"] == "FAIL" for rd in rule_results_data)
        has_missing = any(rd["result_status"] in ("MISSING_EVIDENCE", "UNKNOWN", "REVIEW_REQUIRED") for rd in rule_results_data)

        if has_fail:
            overall_status = "NON_COMPLIANT"
            recommendation = "DISQUALIFIED_RECOMMENDED"
        elif has_missing:
            overall_status = "REQUIRES_REVIEW"
            recommendation = "HUMAN_OFFICER_REVIEW_REQUIRED"
        else:
            overall_status = "COMPLIANT"
            recommendation = "QUALIFIED_RECOMMENDED"

        # Create ComplianceEvaluation record
        eval_record = ComplianceEvaluation(
            bid_submission_id=bid_submission_id,
            tender_id=tender_id,
            tender_version_id=tender_version_id,
            policy_version_id=policy_ver_id,
            evaluation_status=overall_status,
            overall_qualification_recommendation=recommendation,
            evaluation_trace_json={
                "tender_id": tender_id,
                "tender_version_id": tender_version_id,
                "policy_code": policy_code,
                "facts_count": len(facts),
                "rules_evaluated_count": len(rule_results_data),
                "overall_status": overall_status,
                "qualification_recommendation": recommendation,
                "evaluated_at": datetime.datetime.utcnow().isoformat()
            },
            evaluator_id=evaluator_id
        )
        db.add(eval_record)
        db.commit()
        db.refresh(eval_record)

        # Create RuleResults
        for rd in rule_results_data:
            r = rd["rule"]
            crr = ComplianceRuleResult(
                evaluation_id=eval_record.id,
                rule_id=r.id,
                rule_code=r.rule_code,
                requirement_id=rd["requirement_id"],
                result_status=rd["result_status"],
                evaluation_trace_json=rd["trace"],
                explanation_text=rd["explanation"],
                fact_values_json={rf: facts.get(rf.upper()) for rf in (r.required_facts_json or [])},
                evidence_refs_json=rd["evidence_refs"]
            )
            db.add(crr)

        db.commit()

        # If review required or conflict detected, spawn HumanReviewTask
        if overall_status == "REQUIRES_REVIEW":
            hrt = HumanReviewTask(
                bid_submission_id=bid_submission_id,
                evaluation_id=eval_record.id,
                review_reason="Compliance Evaluation Requires Officer Verification due to Missing Evidence or Conflicting Attributes",
                severity="MEDIUM",
                status="PENDING"
            )
            db.add(hrt)
            db.commit()

        # Audit evaluation execution
        audit_service.log_event(
            db=db,
            actor_id=evaluator_id,
            actor_role="ServiceWorker",
            action="COMPLIANCE_EVALUATION_COMPLETED",
            resource_type="ComplianceEvaluation",
            resource_id=eval_record.id,
            payload={
                "bid_submission_id": bid_submission_id,
                "tender_id": tender_id,
                "overall_status": overall_status,
                "recommendation": recommendation,
                "rules_evaluated": len(rule_results_data)
            }
        )

        return eval_record


compliance_engine = ComplianceEngine()
