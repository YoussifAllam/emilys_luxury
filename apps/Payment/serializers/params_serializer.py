from rest_framework import serializers


class Check_vaild_refund_params(serializers.Serializer):
    order_id = serializers.CharField(required=True)
    # payment_id = serializers.CharField(required=True)