# loan/interfaces/serializers/loan_serializers.py
from rest_framework import serializers

from ..implementation.models import LoanApplication
from ..models import LoanApplication


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
            "id",
            "client",
            "amount_requested",
            "term_months",
            "status",
            "submitted_by",
            "reviewed_by",
            "decision_date",
            "created_at",
            "notes",
        ]


class LoanDecisionSerializer(serializers.Serializer):
    approve = serializers.BooleanField()


class LoanApplicationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = [
            "amount_requested",
            "term_months",
            "loan_purpose",
            "daily_repayment",
            "interest_rate",
            "interest_amount",
            "total_payable",
            "decision_date",
            "notes"
        ]

    # def update(self, instance, validated_data):
    #     request_user = self.context["request"].user
    #     if instance.created_by != request_user:
    #         restricted_fields = [

    #         ]
    #     return super().update(instance, validated_data)


class LoanApplicationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = "__all__"