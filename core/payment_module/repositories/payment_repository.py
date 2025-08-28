# infrastructure/repositories/payment_repository.py
"""
Repositories handle database persistence using Django ORM.
They expose Entities back to the Service layer.
"""

from typing import List
from ..entities.payment_entity import CartItemEntity, OrderEntity, PaymentEntity
from marketplace.models import CartItem, Order, Payment


class CartRepository:
    def add_item(self, user_id: int, product_id: int, quantity: int, price: float) -> CartItemEntity:
        """
        Add product to cart. If already exists, increment quantity.
        """
        item, created = CartItem.objects.get_or_create(
            user_id=user_id,
            product_id=product_id,
            defaults={"quantity": quantity, "price": price}
        )
        if not created:
            item.quantity += quantity
            item.save()

        return CartItemEntity(item.id, item.user_id, item.product_id, item.quantity, item.price)

    def get_user_cart(self, user_id: int) -> List[CartItemEntity]:
        """
        Fetch all items in a user's cart.
        """
        items = CartItem.objects.filter(user_id=user_id)
        return [CartItemEntity(i.id, i.user_id, i.product_id, i.quantity, i.price) for i in items]

    def clear_cart(self, user_id: int):
        """
        Empty user's cart after successful checkout.
        """
        CartItem.objects.filter(user_id=user_id).delete()


class OrderRepository:
    def create(self, user_id: int, total_amount: float) -> OrderEntity:
        """
        Create a new order in PENDING state.
        """
        order = Order.objects.create(user_id=user_id, total_amount=total_amount, status="PENDING")
        return OrderEntity(order.id, order.user_id, order.total_amount, order.status, order.created_at)

    def update_status(self, order_id: int, status: str) -> None:
        """
        Update order status (PAID / FAILED).
        """
        Order.objects.filter(id=order_id).update(status=status)


class PaymentRepository:
    def create(self, order_id: int, amount: float, method: str, status: str, transaction_ref: str = None) -> PaymentEntity:
        """
        Create a payment record tied to an order.
        """
        pay = Payment.objects.create(
            order_id=order_id, amount=amount, method=method, status=status, transaction_ref=transaction_ref
        )
        return PaymentEntity(pay.id, pay.order_id, pay.amount, pay.method, pay.status, pay.transaction_ref, pay.created_at)

    def update_status(self, payment_id: int, status: str, transaction_ref: str = None):
        """
        Update payment status after gateway response.
        """
        Payment.objects.filter(id=payment_id).update(status=status, transaction_ref=transaction_ref)
