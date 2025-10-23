# loan/core/services/client_service.py
from typing import Optional, List
from ..entities.client_entity import ClientEntity
from ..repository.client_repository import ClientRepository


class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    def create_client(
        self, *, agent_id: int, full_name: str, national_id: str, contact: str
    ) -> ClientEntity:
        # Add domain validations (e.g., formatting/length) if needed
        return self.client_repo.create(
            full_name=full_name,
            national_id=national_id,
            contact=contact,
            created_by_id=agent_id,
        )

    def get_client(self, client_id: int) -> Optional[ClientEntity]:
        return self.client_repo.get_by_id(client_id)

    def list_agent_clients(self, agent_id: int) -> List[ClientEntity]:
        return self.client_repo.list_for_agent(agent_id)
