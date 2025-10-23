# loan/core/entities/loan.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class LoanApplicationEntity:
    id: Optional[int]
    client_id: int
    amount_requested: float
    term_months: int
    status: str
    submitted_by_id: int
    reviewed_by_id: Optional[int]
    decision_date: Optional[datetime]
    created_at: datetime
    notes: str
