from rest_framework import serializers
from .models import Product
from account.serializers import AccountSerializer


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField()
    price = serializers.FloatField()
    quantity = serializers.FloatField()
    is_active = serializers.BooleanField(default=True)
    seller = AccountSerializer(read_only=True, source="account")

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)

        return product

    def update(self, instance: Product, validated_data: dict):
        non_updatable = {"seller", "account"}

        for key, value in validated_data.items():
            if key in non_updatable:
                raise serializers.ValidationError(
                    detail=f"You can not update the {key} property.",
                    code=422,
                )

            setattr(instance, key, value)
            instance.save()

        return instance
