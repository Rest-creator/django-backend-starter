# interfaces/views/payment_views.py
"""
API endpoints for cart, checkout, and payment confirmation.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..services.payment_services import PaymentService
from ..repositories.payment_repository import CartRepository, OrderRepository, PaymentRepository
from ..serializers.payment_serializers import CartItemSerializer, PaymentSerializer

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    service = PaymentService(CartRepository(), OrderRepository(), PaymentRepository())

    def create(self, request):
        """
        Add product to cart.
        """
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        price = float(request.data.get("price"))
        item = self.service.add_to_cart(request.user.id, product_id, quantity, price)
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CheckoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    service = PaymentService(CartRepository(), OrderRepository(), PaymentRepository())

    def create(self, request):
        """
        Create an Order + Payment record.
        Later this will call the gateway (Stripe, PayPal, EcoCash).
        """
        method = request.data.get("method", "mobile_money")
        payment = self.service.checkout(request.user.id, method)
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Confirm payment after gateway responds.
        This would normally be triggered by a webhook.
        """
        success = request.data.get("success", True)
        transaction_ref = request.data.get("transaction_ref")
        self.service.confirm_payment(pk, success, transaction_ref)
        return Response({"message": "Payment status updated"}, status=status.HTTP_200_OK)
