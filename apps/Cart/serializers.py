from rest_framework import serializers
from apps.Dresses.models import Dresses, dress_images
from .models import *
from .Tasks import Cart_items_tasks


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = dress_images
        fields = ["image"]


class DressesSerializer(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Dresses
        fields = [
            "id",
            "product_image",
            "designer_name",
            "actual_price",
            "description",
            "status",
        ]

    def get_product_image(self, obj):
        product_image = obj.image_set.first()
        if product_image:
            return ProductImagesSerializer(product_image).data["image"]
        return None


class CartItemSerializer(serializers.ModelSerializer):
    dress = DressesSerializer()
    price = serializers.SerializerMethodField()
    error = serializers.SerializerMethodField()

    class Meta:
        model = Cart_Items
        fields = [
            "id",
            "date_added",
            "dress",
            "booking_start_date",
            "booking_end_date",
            "booking_for_n_days",
            "price",
            "error",
        ]

    def get_error(self, obj):
        if not Cart_items_tasks.booking_days_is_available(
            obj.dress, obj.booking_start_date, obj.booking_end_date
        ):
            return "The booking days are no longer available"
        if not Cart_items_tasks.dress_is_available(obj.dress):
            return "The dress is not available for booking"
        return None

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
    items = CartItemSerializer(many=True, read_only=True, source="items_set")

    class Meta:
        model = Cart
        fields = ["id", "created_at", "items"]
