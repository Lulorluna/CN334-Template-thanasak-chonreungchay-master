from django.db import models
from django.contrib.auth.models import User
from product_management.models import Product
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# Create your models here.
class Payment(models.Model):
    payment_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments"
    )
    method = models.CharField(max_length=50)
    card_no = models.CharField(max_length=20)
    expired = models.CharField(max_length=5)
    holder_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.method} ({self.payment_owner.username})"


class Shipping(models.Model):
    method = models.CharField(max_length=50)
    fee = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"{self.method} - {self.fee}"


class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_SHIPPED = "shipped"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "รอชำระเงิน"),
        (STATUS_PAID, "ชำระเงินแล้ว"),
        (STATUS_SHIPPED, "จัดส่งแล้ว"),
        (STATUS_CANCELLED, "ยกเลิก"),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        editable=False,
        default=0,
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    shipping = models.ForeignKey(
        Shipping,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    shipping_address = models.CharField(max_length=500, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.customer.username}"

    @property
    def calculated_total(self):
        return sum(item.unit_price * item.quantity for item in self.items.all())


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    @property
    def unit_price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.unit_price * self.quantity


# Signals to update Order.total_price when ProductOrder changes
@receiver([post_save, post_delete], sender=ProductOrder)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    order.total_price = order.calculated_total
    order.save()
