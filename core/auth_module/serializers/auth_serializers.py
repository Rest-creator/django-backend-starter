from rest_framework import serializers
from ..services.auth_service import AuthService


class SignupSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    phone = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    location = serializers.CharField()

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        try:
            return AuthService.signup(validated_data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))


class SigninSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        result = AuthService.signin(data["identifier"], data["password"])
        if not result:
            raise serializers.ValidationError("Invalid credentials")
        return result
