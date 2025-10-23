# loan/interfaces/serializers/client_serializers.py
from rest_framework import serializers
from ..implementation.models import (
    Client,
    NextOfKin,
    LoanApplication,
    LoanRepayment
    )

class NextOfKinReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = "__all__"


class NextOfKinWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = [
            "name",
            "relationship",
            "contact",
            "address"
        ]


class LoanRepaymentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = "__all__"


class LoanApplicationReadSerializer(serializers.ModelSerializer):
    loan_repayments = LoanRepaymentReadSerializer()

    class Meta:
        model = LoanApplication
        fields = "__all__"


class ClientReadSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    next_of_kin = NextOfKinReadSerializer(many=True, read_only=True)
    loan_applications = LoanApplicationReadSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = "__all__"


class ClientWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "national_id",
            "phone_number",
            ]