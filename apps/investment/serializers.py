# serializers.py
from rest_framework.serializers import ModelSerializer , PrimaryKeyRelatedField
from .models import investmenter_details , investmenter_dresses
from django.contrib.auth import get_user_model
from apps.Users.serializers import User_investmentSerializer
from apps.Dresses.models import Dresses , dress_images
from apps.Dresses.serializers import HomeDressesSerializer
User = get_user_model()

class AddInvestmentSerializer(ModelSerializer):
    user = PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    class Meta: 
        model = investmenter_details
        fields = ['uuid', 'user', 'mobile', 'account_owner_name', 'credit_card_number', 'bank_name']

class GetInvestmentSerializer(ModelSerializer):
    User_details = User_investmentSerializer(source='user', read_only=True)
    class Meta: 
        model = investmenter_details
        fields = ['uuid', 'User_details' ,'mobile', 'account_owner_name', 'credit_card_number', 'bank_name']

class InvestorDressCreateSerializer(ModelSerializer):
    class Meta:
        model = investmenter_dresses
        
        fields = ['uuid', 'user', 'dress']
        read_only_fields = ['user', 'dress']


class InvestorDressListSerializer(ModelSerializer):
    dress = HomeDressesSerializer(read_only=True)

    class Meta:
        model = investmenter_dresses
        fields = ['uuid',  'dress']