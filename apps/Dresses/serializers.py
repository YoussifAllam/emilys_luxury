from rest_framework.serializers import ModelSerializer  , Serializer , IntegerField ,SerializerMethodField
from .models import * 
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name' , 'email'] 

class number_of_visitors_Serializer(ModelSerializer):
    class Meta:
        model = dress_number_of_visitors
        fields = ['number_of_visitors']

class Dress_images_Serializer(ModelSerializer):
    class Meta:
        model = dress_images
        fields = ['image']

class DressesSerializer(ModelSerializer):
    images = Dress_images_Serializer(many=True , read_only=True , source='image_set')
    class Meta:
        model = Dresses
        fields = ['id' , 'designer_name' , 'status' , 'measurement' , 'Color' , 'price_for_3days' , 'price_for_6days' , 'price_for_8days' ,
                  'actual_price' , 'description' , 'delivery_information' ,'images']

class HomeDressesSerializer(ModelSerializer):
    main_image = SerializerMethodField()

    class Meta:
        model = Dresses
        fields = ['id', 'designer_name', 'measurement', 'price_for_3days', 'actual_price', 'is_approved', 'main_image']

    def get_main_image(self, obj):
        # Assuming the related name for the image set is 'image_set'
        images = obj.image_set.all()
        if images.exists():
            # Return the URL of the first image. Adjust the logic here if you have specific criteria for selecting the image.
            return images.first().image.url
        return None

class Dress_Reviews_Serializer(ModelSerializer):
    user = UserSerializer()  # Use the nested UserSerializer

    class Meta:
        model = dress_reviews
        fields = ['Rating_stars', 'feedback', 'uploaded_at', 'user']

class AverageRatingDetailSerializer(Serializer):
    stars = IntegerField()
    product_count = IntegerField()

class AverageRatingSerializer(Serializer):
    ratings_detail = AverageRatingDetailSerializer(many=True)

class FavoriteDressSerializer(ModelSerializer):
    class Meta:
        model = favorite_dresses
        fields = ['user' , 'dress']






