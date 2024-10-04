from rest_framework import serializers
from .models import *


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["answer", "question"]


class terms_and_condationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = terms_and_condations
        fields = ["title", "description"]
