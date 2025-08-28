# core/services/payment_service.py
"""
The Service layer enforces business rules.
It calls Repositories for persistence and will call Gateways for real payments.
"""

from ..gateways.stripe_gateway import StripeGateway
from ..entities.payment_entity import PaymentEntity
from ..repositories.payment_repository import CartRepository, OrderRepository, PaymentRepository

# ⬇️ This folder will hold integrations with real payment providers.
# Example: core/gateways/stripe_gateway.py, core/gateways/paypal_gateway.py, etc.
# For now, we simulate the payment flow without an external provider.

class PaymentService:
    def __init__(self, cart_repo: CartRepository, order_repo: OrderRepository, payment_repo: PaymentRepository):
        self.cart_repo = cart_repo
        self.order_repo = order_repo
        self.payment_repo = payment_repo

    def add_to_cart(self, user_id: int, product_id: int, quantity: int, price: float):
        """
        Add item to the cart (or update quantity if it exists).
        """
        return self.cart_repo.add_item(user_id, product_id, quantity, price)

    def checkout(self, user_id: int, method: str) -> PaymentEntity:
        """
        Convert user's cart into an Order + Payment record.
        At this stage, we INITIATE a payment with the selected method.
        """
        cart_items = self.cart_repo.get_user_cart(user_id)
        total_amount = sum(i.price * i.quantity for i in cart_items)

        # Create Order in "PENDING"
        order = self.order_repo.create(user_id, total_amount)

        # Create Payment in "INITIATED"
        payment = self.payment_repo.create(order.id, total_amount, method, "INITIATED")
        
        # Example extension
        gateway = StripeGateway()
        result = gateway.charge(total_amount, "USD", source_token)
        self.confirm_payment(payment.id, result["success"], result["transaction_ref"])


        # Clear cart after checkout initiated
        self.cart_repo.clear_cart(user_id)

        return payment

    def confirm_payment(self, payment_id: int, success: bool, transaction_ref: str = None):
        """
        Confirm payment after response from the gateway (manual or webhook).
        Update both Payment and Order statuses.
        """
        if success:
            self.payment_repo.update_status(payment_id, "SUCCESS", transaction_ref)
        else:
            self.payment_repo.update_status(payment_id, "FAILED", transaction_ref)
