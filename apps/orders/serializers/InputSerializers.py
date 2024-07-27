from rest_framework.serializers import ModelSerializer
from apps.orders.models import Order , OrderItem

class AddOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['uuid', 'user', 'status', 'total_price']

class AddOrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['uuid', 'order', 'product_size', 'quantity' , 'price']


