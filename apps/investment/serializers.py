# serializers.py
from rest_framework import serializers
from .models import investmenter_details
from django.contrib.auth import get_user_model
from apps.Users.serializers import User_investmentSerializer

User = get_user_model()

class AddInvestmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    class Meta: 
        model = investmenter_details
        fields = ['uuid', 'user', 'mobile', 'account_owner_name', 'credit_card_number', 'bank_name']


class GetInvestmentSerializer(serializers.ModelSerializer):
    User_details = User_investmentSerializer(source='user', read_only=True)
    class Meta: 
        model = investmenter_details
        fields = ['uuid', 'User_details' ,'mobile', 'account_owner_name', 'credit_card_number', 'bank_name']