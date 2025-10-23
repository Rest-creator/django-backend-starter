# core/entities/payment.py
"""
Entities are plain Python objects representing core business concepts.
They have no knowledge of the database, Django, or any external APIs.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CartItemEntity:
    id: Optional[int]
    user_id: int
    product_id: int
    quantity: int
    price: float  # snapshot of price when added to cart


@dataclass
class OrderEntity:
    id: Optional[int]
    user_id: int
    total_amount: float
    status: str  # PENDING, PAID, FAILED
    created_at: datetime


@dataclass
class PaymentEntity:
    id: Optional[int]
    order_id: int
    amount: float
    method: str  # "stripe", "paypal", "mobile_money"
    status: str  # INITIATED, SUCCESS, FAILED
    transaction_ref: Optional[str]
    created_at: datetime
