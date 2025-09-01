# loan/interfaces/serializers/client_serializers.py
from rest_framework import serializers
from ..implementation.models import Client

class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["full_name", "national_id", "contact"]

class ClientDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    class Meta:
        model = Client
        fields = ["id", "full_name", "national_id", "contact", "created_by", "created_at"]
