from django.db import models
from uuid import uuid4

class OrderStatusChoices(models.TextChoices):
    PENDING     = 'pending', 'Pending'
    PROCESSING  = 'processing', 'Processing'
    SHIPPED     = 'shipped', 'Shipped'
    DELIVERED   = 'delivered', 'Delivered'
    CANCELLED   = 'cancelled', 'Cancelled'


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey('Users.User', related_name='user_orders_set' , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField( max_length=20, choices=OrderStatusChoices.choices, default=OrderStatusChoices.PENDING)
    total_price = models.FloatField()
    is_payment_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.uuid} by {self.user.username}"

class OrderItem(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.quantity} x {self.product_size.product.Product_name} - {self.product_size.size}"


