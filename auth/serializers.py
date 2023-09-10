from typing import Any

from rest_framework import serializers

from .models import OTP, CustomUser, LoginToken


class CustomUserSerialzer(serializers.Serializer[CustomUser]):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField()
    email = serializers.CharField()
    age = serializers.IntegerField()
    phone_number = serializers.CharField()
    # TODO: change type field type to studentTeacherField
    type = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)

    def create(self, validated_data: Any):
        return CustomUser.objects.create(**validated_data)


class LoginTokenSerialzer(serializers.Serializer[LoginToken]):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.CharField()
    token = serializers.CharField()
    is_active = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def create(self, validated_data: Any):
        return LoginToken.objects.create(**validated_data)


class OTPSerialzer(serializers.Serializer[OTP]):
    id = serializers.UUIDField(read_only=True)
    otp = serializers.CharField(max_length=6, required=False)
    phone_number = serializers.CharField(max_length=17)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data: Any):
        return OTP.objects.create(**validated_data)
