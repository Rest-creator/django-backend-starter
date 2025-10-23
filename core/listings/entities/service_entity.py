from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class ServiceEntity:
    id: int
    user_id: int
    name: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    images: Optional[List[str]] = None
