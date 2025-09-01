# loan/core/repositories/client_repository.py
from typing import Optional, List
from ..implementation.models import Client
from ..entities.client_entity import ClientEntity

class ClientRepository:
    def create(self, *, full_name: str, national_id: str, contact: str, created_by_id: int) -> ClientEntity:
        obj = Client.objects.create(
            full_name=full_name, national_id=national_id, contact=contact, created_by_id=created_by_id
        )
        return ClientEntity(obj.id, obj.full_name, obj.national_id, obj.contact, obj.created_by_id, obj.created_at)

    def get_by_id(self, client_id: int) -> Optional[ClientEntity]:
        try:
            c = Client.objects.get(id=client_id)
            return ClientEntity(c.id, c.full_name, c.national_id, c.contact, c.created_by_id, c.created_at)
        except Client.DoesNotExist:
            return None

    def list_for_agent(self, agent_id: int) -> List[ClientEntity]:
        qs = Client.objects.filter(created_by_id=agent_id).order_by("-created_at")
        return [ClientEntity(c.id, c.full_name, c.national_id, c.contact, c.created_by_id, c.created_at) for c in qs]
