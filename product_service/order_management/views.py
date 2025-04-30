from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from order_management.models import *
from order_management.serializers import ProductOrderSerializer


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


class ProductSummaryView(APIView):
    def get(self, request):
        product_count = Product.objects.count()
        order_count = Order.objects.count()
        total_quantity_sold = (
            ProductOrder.objects.aggregate(total=Sum("quantity"))["total"] or 0
        )

        return Response(
            {
                "product_count": product_count,
                "order_count": order_count,
                "total_quantity_sold": total_quantity_sold,
            }
        )
