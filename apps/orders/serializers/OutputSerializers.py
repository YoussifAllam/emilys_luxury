from rest_framework.serializers import ModelSerializer , SerializerMethodField
from apps.orders.models import Order , OrderItem , OrderDetails
from apps.Dresses.models import Dresses as Dresses_model

class GetOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['uuid',  'status', 'total_price']

class GETDressesSerializer(ModelSerializer):
    main_image = SerializerMethodField()

    class Meta:
        model = Dresses_model
        fields = ['id', 'designer_name','main_image']

    def get_main_image(self, obj):
        # Assuming the related name for the image set is 'image_set'
        images = obj.image_set.all()
        if images.exists():
            # Return the URL of the first image. Adjust the logic here if you have specific criteria for selecting the image.
            return images.first().image.url
        return None



class GetOrderItemSerializer(ModelSerializer):
    dress = GETDressesSerializer(read_only=True , source = 'Target_dress')
    class Meta:
        model = OrderItem
        fields = ['uuid' , 'dress' ]


class GetOrderDetailSerializer(ModelSerializer):
    items = GetOrderItemSerializer(many=True, read_only=True, source='items_set')
    class Meta:
        model = Order
        fields = ['uuid', 'status','arrival_date' , 'items']

        
class GetOrderBillingDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'
