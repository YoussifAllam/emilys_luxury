from rest_framework import serializers
from ..models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order_uuid = serializers.UUIDField()
    amount = serializers.FloatField(required=False)
    status = serializers.CharField(required=False)
    currency = serializers.CharField(required=False)

    class Meta:
        model = Payment
        fields = "__all__"
