# loan/core/services/loan_service.py
from typing import List, Optional
from ..implementation.models import LoanApplication
from ..entities.loan_entity import LoanApplicationEntity
from ..repository.client_repository import ClientRepository
from ..repository.loan_repository import LoanRepository


class LoanService:
    def __init__(self, client_repo: ClientRepository, loan_repo: LoanRepository):
        self.client_repo = client_repo
        self.loan_repo = loan_repo

    def submit_application(
        self,
        *,
        agent_id: int,
        client_id: int,
        amount_requested: float,
        term_months: int,
        notes: str = ""
    ) -> LoanApplicationEntity:
        client = self.client_repo.get_by_id(client_id)
        if not client:
            raise ValueError("Client does not exist.")
        if amount_requested <= 0:
            raise ValueError("Amount must be positive.")
        if not (1 <= term_months <= 120):
            raise ValueError("Term must be between 1 and 120 months.")
        return self.loan_repo.create(
            client_id=client_id,
            amount_requested=amount_requested,
            term_months=term_months,
            submitted_by_id=agent_id,
            notes=notes,
        )

    def list_for_client(self, client_id: int) -> List[LoanApplicationEntity]:
        return self.loan_repo.list_for_client(client_id)

    def list_for_agent(self, agent_id: int) -> List[LoanApplicationEntity]:
        return self.loan_repo.list_for_agent(agent_id)

    def decide(
        self, *, loan_id: int, admin_id: int, approve: bool
    ) -> Optional[LoanApplicationEntity]:
        new_status = (
            LoanApplication.STATUS_APPROVED
            if approve
            else LoanApplication.STATUS_REJECTED
        )
        entity = self.loan_repo.update_status(
            loan_id, new_status, reviewed_by_id=admin_id
        )
        # Hook: send notification to client about decision here (email/SMS/push)
        return entity
