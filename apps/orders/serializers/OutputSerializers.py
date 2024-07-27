from rest_framework.serializers import ModelSerializer
from apps.orders.models import Order , OrderItem

class GetOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['uuid',  'status', 'total_price']

class GetOrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['uuid', 'quantity' , 'price']


