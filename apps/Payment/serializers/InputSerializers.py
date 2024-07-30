from rest_framework import serializers
from ..models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    order_uuid = serializers.UUIDField() 
    class Meta:
        model = Payment
        fields = '__all__'
