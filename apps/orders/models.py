from django.db import models
from uuid import uuid4
from simple_history.models import HistoricalRecords


class OrderStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        "Users.User", related_name="user_orders_set", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.FloatField()
    is_payment_completed = models.BooleanField(default=False)
    applied_coupon = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.PENDING,
    )
    arrival_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Order {self.uuid} by {self.user.username}"


class OrderItem(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, related_name="items_set", on_delete=models.CASCADE)
    Target_dress = models.ForeignKey(
        "Dresses.Dresses", related_name="Dress_item_set", on_delete=models.CASCADE
    )
    price = models.FloatField()
    booking_for_n_days = models.IntegerField()
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()

    def __str__(self):
        return f"{self.uuid}"


class OrderDetails(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="order_details_set"
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    comapny_name = models.CharField(max_length=30, null=True, blank=True)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    Area = models.CharField(max_length=30)
    zip = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    application_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.uuid}"


class order_dress_booking_days(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    OrderItem = models.ForeignKey(
        OrderItem,
        related_name="OrderItem_booking_days_set",
        on_delete=models.CASCADE,
        verbose_name="Order Item id",
    )
    dress = models.ForeignKey(
        "Dresses.Dresses", on_delete=models.CASCADE, verbose_name="Dress id"
    )
    day = models.DateField()

    def __str__(self):
        return (
            f"dress : {self.dress} -- day : {self.day} -- OrderItem : {self.OrderItem}"
        )
