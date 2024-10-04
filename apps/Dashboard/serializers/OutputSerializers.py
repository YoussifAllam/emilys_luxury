from rest_framework.serializers import ModelSerializer, SerializerMethodField
from apps.orders.models import Order, OrderItem, OrderDetails
from apps.Dresses.models import Dresses as Dresses_model
from apps.Dresses.models import favorite_dresses
from apps.invitation.models import user_invitation_points


class GETDressesSerializer(ModelSerializer):
    main_image = SerializerMethodField()

    class Meta:
        model = Dresses_model
        fields = ["id", "designer_name", "main_image"]

    def get_main_image(self, obj):
        # Assuming the related name for the image set is 'image_set'
        images = obj.image_set.all()
        if images.exists():
            # Return the URL of the first image. Adjust the logic here if you have specific criteria for selecting the image.
            return images.first().image.url
        return None


class GetOrderItemSerializer(ModelSerializer):
    dress = GETDressesSerializer(read_only=True, source="Target_dress")

    class Meta:
        model = OrderItem
        fields = ["uuid", "dress"]


class GetOrderSerializer(ModelSerializer):
    # items = GetOrderItemSerializer(many=True, read_only=True, source='items_set')
    class Meta:
        model = Order
        fields = [
            "uuid",
            "status",
            "arrival_date",
            "is_payment_completed",
            "total_price",
        ]


class UserPointsSerializers(ModelSerializer):
    class Meta:
        model = user_invitation_points
        fields = ["user_code", "num_of_points"]


class DressesSerializer_for_fav(ModelSerializer):
    main_image = SerializerMethodField()

    class Meta:
        model = Dresses_model
        fields = [
            "id",
            "designer_name",
            "measurement",
            "price_for_3days",
            "actual_price",
            "is_approved",
            "main_image",
        ]

    def get_main_image(self, obj):
        # Assuming the related name for the image set is 'image_set'
        images = obj.image_set.all()
        if images.exists():
            # Return the URL of the first image. Adjust the logic here if you have specific criteria for selecting the image.
            return images.first().image.url
        return None


class FavDressesListSerializer(ModelSerializer):
    fav_dress = DressesSerializer_for_fav(read_only=True, source="dress")

    class Meta:
        model = favorite_dresses
        fields = ["fav_dress"]


class ShippingAddressSerializer(ModelSerializer):
    address = SerializerMethodField()

    class Meta:
        model = OrderDetails
        fields = "__all__"  # ['address']

    def get_address(self, obj):
        return f"{obj.city}, {obj.street_address}"
