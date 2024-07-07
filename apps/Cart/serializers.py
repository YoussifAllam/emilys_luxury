from rest_framework import serializers
from apps.Dresses.models import Dresses, dress_images
from .models import *

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = dress_images
        fields = ['image']

class DressesSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Dresses
        fields = ['id', 'product_image']

    def get_product_image(self, obj):
        product_image = obj.image_set.first()
        if product_image:
            return ProductImagesSerializer(product_image).data['image']
        return None

class CartItemSerializer(serializers.ModelSerializer):
    dress = DressesSerializer()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Cart_Items
        fields = ['id', 'date_added', 'dress', 'booking_start_date', 'booking_end_date', 'booking_for_n_days', 'price']

    def get_price(self, obj):
        booking_days = int(obj.booking_for_n_days)
        if booking_days == 3:
            return obj.dress.price_for_3days
        elif booking_days == 6:
            return obj.dress.price_for_6days
        elif booking_days == 8:
            return obj.dress.price_for_8days
        return None
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='items_set')

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items']
