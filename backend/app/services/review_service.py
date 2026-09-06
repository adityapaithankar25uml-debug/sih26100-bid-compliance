import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.domain import HumanReviewTask, BidSubmission, User


class HumanReviewWorkspaceService:
    """Service managing human review task queue, assignments, policy-controlled routing, and resolution workflow.

    IMPORTANT:
    - Risk assessment remains advisory.
    - Review routing is explicitly policy-controlled by configured RoutingPolicy parameters.
    - Neither risk scoring nor review task creation determines bidder qualification outcome.
    """

    def evaluate_policy_review_routing(
        self,
        db: Session,
        bid_submission_id: str,
        routing_policy: Optional[Dict[str, Any]] = None
    ) -> List[HumanReviewTask]:
        """Evaluate policy-controlled review task routing rules for a bid submission."""
        policy = routing_policy or {
            "route_on_critical_risk": True,
            "route_on_govt_conflict": True,
            "route_on_missing_mandatory_evidence": True
        }
        created_tasks: List[HumanReviewTask] = []
        sub = db.query(BidSubmission).filter_by(id=bid_submission_id).first()
        if not sub:
            return created_tasks

        # Check policy rule: route on government conflict or missing mandatory evidence
        if policy.get("route_on_govt_conflict"):
            from app.models.domain import GovernmentVerificationRecord
            govs = db.query(GovernmentVerificationRecord).filter_by(bid_submission_id=bid_submission_id).all()
            for g in govs:
                if g.business_status in ("CONFLICTING", "NOT_VERIFIED") or g.identity_match_status == "MISMATCH":
                    task = self.create_review_task(
                        db=db,
                        bid_submission_id=bid_submission_id,
                        review_reason=f"Policy-controlled routing: Government source {g.source_code} returned {g.business_status} with identity {g.identity_match_status}.",
                        severity="HIGH",
                        priority="HIGH",
                        verification_record_id=g.id,
                        review_code="ROUTING_GOVT_CONFLICT"
                    )
                    created_tasks.append(task)
        return created_tasks

    def create_review_task(
        self,
        db: Session,
        bid_submission_id: str,
        review_reason: str,
        severity: str = "MEDIUM",
        priority: str = "MEDIUM",
        document_id: Optional[str] = None,
        verification_record_id: Optional[str] = None,
        evaluation_id: Optional[str] = None,
        tender_id: Optional[str] = None,
        tender_requirement_id: Optional[str] = None,
        bidder_id: Optional[str] = None,
        policy_version_id: Optional[str] = None,
        review_code: Optional[str] = None,
        suggested_action: Optional[str] = None,
        evidence_refs: Optional[List[str]] = None
    ) -> HumanReviewTask:
        """Create a human review task in the queue."""
        # Check if identical pending task already exists
        existing = db.query(HumanReviewTask).filter_by(
            bid_submission_id=bid_submission_id,
            review_reason=review_reason,
            status="PENDING"
        ).first()
        if existing:
            return existing

        task = HumanReviewTask(
            bid_submission_id=bid_submission_id,
            document_id=document_id,
            verification_record_id=verification_record_id,
            evaluation_id=evaluation_id,
            tender_id=tender_id,
            tender_requirement_id=tender_requirement_id,
            bidder_id=bidder_id,
            policy_version_id=policy_version_id,
            review_code=review_code or f"REV_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            review_reason=review_reason,
            severity=severity,
            priority=priority,
            status="PENDING",
            suggested_action=suggested_action or "Inspect supporting document evidence and government source verification.",
            evidence_refs_json=evidence_refs or [],
            review_history_json=[{
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "action": "CREATED",
                "reason": review_reason
            }]
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def list_review_tasks(
        self,
        db: Session,
        status_filter: Optional[str] = None,
        priority_filter: Optional[str] = None,
        assigned_officer_id: Optional[str] = None
    ) -> List[HumanReviewTask]:
        """Query human review task queue with filters."""
        q = db.query(HumanReviewTask)
        if status_filter:
            q = q.filter_by(status=status_filter)
        if priority_filter:
            q = q.filter_by(priority=priority_filter)
        if assigned_officer_id:
            q = q.filter_by(assigned_officer_id=assigned_officer_id)
        return q.order_by(HumanReviewTask.created_at.desc()).all()

    def assign_review_task(
        self,
        db: Session,
        task_id: str,
        officer_id: str
    ) -> HumanReviewTask:
        """Assign review task to a specific procurement officer."""
        task = db.query(HumanReviewTask).filter_by(id=task_id).first()
        if not task:
            raise ValueError(f"Review task {task_id} not found")

        task.assigned_officer_id = officer_id
        task.status = "IN_REVIEW"
        history = task.review_history_json or []
        history.append({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "action": "ASSIGNED",
            "officer_id": officer_id
        })
        task.review_history_json = history
        db.commit()
        db.refresh(task)
        return task

    def resolve_review_task(
        self,
        db: Session,
        task_id: str,
        officer_id: str,
        decision: str,
        resolution_summary: str,
        comments: Optional[str] = None
    ) -> HumanReviewTask:
        """Resolve a human review task with officer decision and explanation."""
        task = db.query(HumanReviewTask).filter_by(id=task_id).first()
        if not task:
            raise ValueError(f"Review task {task_id} not found")

        task.assigned_officer_id = officer_id
        task.decision = decision
        task.comments = comments
        task.resolution_summary = resolution_summary
        task.status = "RESOLVED" if decision in ("APPROVED", "OVERRIDDEN", "RESOLVED") else "REJECTED"
        task.decided_at = datetime.datetime.utcnow()

        history = task.review_history_json or []
        history.append({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "action": "RESOLVED",
            "officer_id": officer_id,
            "decision": decision,
            "summary": resolution_summary
        })
        task.review_history_json = history

        db.commit()
        db.refresh(task)
        return task


review_service = HumanReviewWorkspaceService()
