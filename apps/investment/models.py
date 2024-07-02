from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class investmenter_details (models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, primary_key=True , on_delete=models.CASCADE)
    mobile = models.CharField(max_length=30)
    account_owner_name = models.CharField(max_length=40)
    credit_card_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=30)