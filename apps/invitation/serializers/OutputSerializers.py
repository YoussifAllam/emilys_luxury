from ..models import *
from rest_framework.serializers import ModelSerializer

class UserPointsSerializers(ModelSerializer):
    class Meta:
        model = user_invitation_points
        fields = ['num_of_points','user_code']
