# interfaces/serializers/payment_serializers.py
from rest_framework import serializers
from ..entities.payment_entity import CartItemEntity, OrderEntity, PaymentEntity


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    total_amount = serializers.FloatField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()


class PaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_id = serializers.IntegerField()
    amount = serializers.FloatField()
    method = serializers.CharField()
    status = serializers.CharField()
    transaction_ref = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
