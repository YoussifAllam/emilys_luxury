from rest_framework.serializers import ModelSerializer  , Serializer , IntegerField ,SerializerMethodField , BooleanField
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
    is_fav =  SerializerMethodField()
    class Meta:
        model = Dresses
        fields = ['id' , 'designer_name' , 'status' , 'measurement' ,
                   'Color' , 'price_for_3days' , 'price_for_6days' , 'price_for_8days' ,
                  'actual_price' , 'description' , 'delivery_information' ,'images' ,'product_type' ,  'is_fav']
        
    def get_is_fav(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorite_set.filter(user=request.user).exists()
        return False

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
    
class HomeWithFavDressesSerializer(ModelSerializer):
    main_image = SerializerMethodField()
    is_fav =  SerializerMethodField()
    class Meta:
        model = Dresses
        fields = ['id', 'designer_name', 'measurement', 'price_for_3days', 'actual_price', 'is_approved', 'main_image' , 'is_fav']

    def get_main_image(self, obj):
        # Assuming the related name for the image set is 'image_set'
        images = obj.image_set.all()
        if images.exists():
            # Return the URL of the first image. Adjust the logic here if you have specific criteria for selecting the image.
            return images.first().image.url
        return None

    def get_is_fav(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.favorite_set.filter(user=request.user).exists()
        return False

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

class Busy_days_Serializer(ModelSerializer):
    class Meta:
        model = dress_busy_days
        fields = '__all__'

class ADD_Dress_images_Serializer(ModelSerializer):
    class Meta:
        model = dress_images
        fields = ['dress','image']

