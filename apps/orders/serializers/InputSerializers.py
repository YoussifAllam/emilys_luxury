from rest_framework.serializers import ModelSerializer
from apps.orders.models import Order , OrderItem , OrderDetails

class AddOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['uuid', 'user', 'status', 'total_price','applied_coupon']

class AddOrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['uuid', 'order','Target_dress','price','booking_for_n_days','booking_start_date','booking_end_date']

class OrederDetailSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'
