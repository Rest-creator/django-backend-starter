# loan/interfaces/serializers/loan_serializers.py
from rest_framework import serializers
from ..implementation.models import LoanApplication

class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ["client", "amount_requested", "term_months", "notes"]

class LoanDetailSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    submitted_by = serializers.StringRelatedField()
    reviewed_by = serializers.StringRelatedField()
    class Meta:
        model = LoanApplication
        fields = [
            "id", "client", "amount_requested", "term_months", "status",
            "submitted_by", "reviewed_by", "decision_date", "created_at", "notes"
        ]

class LoanDecisionSerializer(serializers.Serializer):
    approve = serializers.BooleanField()
