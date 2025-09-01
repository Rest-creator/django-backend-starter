# loan/core/repositories/loan_repository.py
from typing import Optional, List
from django.utils import timezone
from ..implementation.models import LoanApplication
from ..entities.loan_entity import LoanApplicationEntity

class LoanRepository:
    def create(self, *, client_id: int, amount_requested: float, term_months: int, submitted_by_id: int, notes: str = "") -> LoanApplicationEntity:
        obj = LoanApplication.objects.create(
            client_id=client_id,
            amount_requested=amount_requested,
            term_months=term_months,
            submitted_by_id=submitted_by_id,
            status=LoanApplication.STATUS_PENDING,
            notes=notes,
        )
        return self._to_entity(obj)

    def get_by_id(self, loan_id: int) -> Optional[LoanApplicationEntity]:
        try:
            return self._to_entity(LoanApplication.objects.get(id=loan_id))
        except LoanApplication.DoesNotExist:
            return None

    def list_for_client(self, client_id: int) -> List[LoanApplicationEntity]:
        qs = LoanApplication.objects.filter(client_id=client_id).order_by("-created_at")
        return [self._to_entity(obj) for obj in qs]

    def list_for_agent(self, agent_id: int) -> List[LoanApplicationEntity]:
        qs = LoanApplication.objects.filter(submitted_by_id=agent_id).order_by("-created_at")
        return [self._to_entity(obj) for obj in qs]

    def update_status(self, loan_id: int, status: str, reviewed_by_id: int) -> Optional[LoanApplicationEntity]:
        try:
            obj = LoanApplication.objects.get(id=loan_id)
            obj.status = status
            obj.reviewed_by_id = reviewed_by_id
            obj.decision_date = timezone.now()
            obj.save(update_fields=["status", "reviewed_by", "decision_date"])
            return self._to_entity(obj)
        except LoanApplication.DoesNotExist:
            return None

    @staticmethod
    def _to_entity(obj: LoanApplication) -> LoanApplicationEntity:
        return LoanApplicationEntity(
            id=obj.id,
            client_id=obj.client_id,
            amount_requested=float(obj.amount_requested),
            term_months=obj.term_months,
            status=obj.status,
            submitted_by_id=obj.submitted_by_id,
            reviewed_by_id=obj.reviewed_by_id,
            decision_date=obj.decision_date,
            created_at=obj.created_at,
            notes=obj.notes,
        )
