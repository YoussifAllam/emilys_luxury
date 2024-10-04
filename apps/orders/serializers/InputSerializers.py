from rest_framework.serializers import ModelSerializer
from apps.orders.models import Order, OrderItem, OrderDetails


class AddOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ["uuid", "user", "status", "total_price", "applied_coupon"]


class AddOrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "uuid",
            "order",
            "Target_dress",
            "price",
            "booking_for_n_days",
            "booking_start_date",
            "booking_end_date",
        ]


class OrederDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = "__all__"


class UpdateOrderBillingDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = "__all__"
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "street_address": {"required": False},
            "city": {"required": False},
            "Area": {"required": False},
            "zip": {"required": False},
            "phone_number": {"required": False},
            "email": {"required": False},
            "order": {"required": False},
        }
