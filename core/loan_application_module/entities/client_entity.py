# loan/core/entities/client.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ClientEntity:
    id: Optional[int]
    full_name: str
    national_id: str
    contact: str
    created_by_id: int
    created_at: datetime
