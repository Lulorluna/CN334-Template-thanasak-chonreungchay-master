from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProductOrder
from .serializers import ProductOrderSerializer


class OrderByProductIdView(APIView):
    def get(self, request, product_id):
        product_orders = ProductOrder.objects.filter(product__id=product_id)
        if not product_orders.exists():
            return Response({"error": "Product or Order ID not Found!"}, status=404)

        product = product_orders.first().product
        product_data = {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
        }

        serializer = ProductOrderSerializer(product_orders, many=True)
        return Response({"product": product_data, "orders": serializer.data})
