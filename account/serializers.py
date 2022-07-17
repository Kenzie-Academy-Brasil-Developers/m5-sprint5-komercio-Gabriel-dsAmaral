from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status

from .models import Account


class AccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, write_only=True)
    is_seller = serializers.BooleanField(default=False)
    date_joined = serializers.DateTimeField(read_only=True)

    def validate_email(self, email: str):
        email_exists = Account.objects.filter(email=email).exists()

        if email_exists:
            raise serializers.ValidationError(detail="email already exists", code=400)

        return email

    def validate_password(self, password: str):
        password = make_password(password)
        return password

    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        return account

    def update(self, instance: Account, validated_data: dict):
        non_updatable = {"is_active", "password", "email"}

        for key, value in validated_data.items():
            if key in non_updatable:
                raise serializers.ValidationError(
                    detail=f"You can not update the {key} property.",
                    code=422,
                )

            setattr(instance, key, value)
            instance.save()

        return instance


class AccountIsActiveSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()

    def update(self, instance: Account, validated_data: dict):
        setattr(instance, "is_active", validated_data["is_active"])
        instance.save()

        return instance
