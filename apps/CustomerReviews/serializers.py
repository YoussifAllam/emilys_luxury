from rest_framework.serializers import ModelSerializer
from .models import CustomerReviews
from apps.Users.serializers import UserSerializer


class CustomerReviewsSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)  # Ensure the field name matches the model field

    class Meta:
        model = CustomerReviews
        fields = ['user', 'Rating_stars', 'feedback', 'uploaded_at']