from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class investmenter_details (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=30)
    account_owner_name = models.CharField(max_length=40)
    credit_card_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=30)