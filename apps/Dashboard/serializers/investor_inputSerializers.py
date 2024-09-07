from rest_framework.serializers import ModelSerializer  , ChoiceField
from apps.Dresses.models import Dresses , dress_images

class Dress_images_Serializer(ModelSerializer):
    class Meta:
        model = dress_images
        fields = ['image']

class DressesSerializer(ModelSerializer):
    status = ChoiceField(choices=['available', 'unavailable'], required=True)
    class Meta:
        model = Dresses
        fields = ['id' , 'designer_name' , 'status' , 'measurement' ,
                   'Color' , 'price_for_3days' , 'price_for_6days' , 'price_for_8days' ,
                  'actual_price' , 'description' , 'delivery_information' ,'product_type','status' ]
    
    