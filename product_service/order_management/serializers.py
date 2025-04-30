from rest_framework import serializers
from order_management.models import *
from product_management.models import *


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = "__all__"


class ProductOrderSerializer(serializers.ModelSerializer):
    unit_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductOrder
        fields = ["order", "product", "quantity", "unit_price", "total_price"]

    def get_unit_price(self, obj):
        return obj.product.price

    def get_total_price(self, obj):
        return obj.product.price * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
    items = ProductOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
