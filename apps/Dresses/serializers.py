from rest_framework.serializers import ModelSerializer  , Serializer , IntegerField
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

class DressesSerializer(ModelSerializer):
    class Meta:
        model = Dresses
        fields = ['id' , 'designer_name' , 'status' , 'measurement' , 'Color' , 'price_for_3days' , 'price_for_6days' , 'price_for_8days' ,
                  'actual_price' , 'description' , 'delivery_information' ]

class HomeDressesSerializer(ModelSerializer):
    class Meta:
        model = Dresses
        fields = ['id' , 'designer_name' , 'measurement'   , 'price_for_3days' , 'actual_price' ,  'is_approved']

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






