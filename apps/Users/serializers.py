from .models import User 
from rest_framework import serializers
import re
from django.contrib.auth.password_validation import validate_password
import random


class SignUpSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    confirm_password = serializers.CharField(write_only=True, required=True)
    accept_terms = serializers.BooleanField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['uuid', 'first_name' , 'username', 'email', 'password', 'confirm_password',
                   'email_verified', 'profile_picture',  'accept_terms' , 'user_type']
        extra_kwargs = {

            'password': {'write_only': True},
            
                        'first_name': {'required': True},
                        'email': {'required': True},
                        'username': {'read_only': True}
                        }

    def validate_email(self, value):
        # Check if email is already registered
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")

        return value

    def validate_password(self, value):
        # Check for strong password
        if not re.search(r'\d', value) or not re.search('[A-Z]', value):
            raise serializers.ValidationError("Password should contain at least 1 number and 1 uppercase letter.")

        validate_password(value)
        return value

    def validate(self, data):
        # Check if passwords match
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")

        # Check if terms are accepted
        if not data.get('accept_terms'):
            raise serializers.ValidationError("Terms and conditions must be accepted.")

        return data

    def create(self, validated_data):
        name = validated_data['first_name'] 
       
        base_username = re.sub(r'\s+', '_', name).lower()

        while True:
            random_number = random.randint(1000, 9999)
            unique_username = f"{base_username}_{random_number}"
            try:
                User.objects.get(username=unique_username)
            except User.DoesNotExist:
                name = unique_username
                break

        user = User.objects.create_user(
            username=name,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],
            accept_terms = validated_data['accept_terms'],
        )
        
        return user
    
class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = ('uuid','username','first_name' ,'email','profile_picture' , 
                  'is_staff','is_superuser' ,'is_approvid' , 'user_type' , 'email_verified' ) 
        
class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_type' , 'email_verified'  ) 

class GetALLUserSerializer(serializers.ModelSerializer):
    User_Name = serializers.SerializerMethodField()

    def get_User_Name(self, obj):
        # Concatenate first name and last name with a space in between
        return f"{obj.first_name} ".strip()
    
    class Meta:
        model = User
        fields = ('User_Name','email','created_Date','last_login')

class Get_UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name' , 'email', 'uuid') 


class User_investmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name' , 'email')
