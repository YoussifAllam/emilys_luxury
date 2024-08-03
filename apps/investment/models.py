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
    payout_account_id = models.CharField(max_length=50)
    iban = models.CharField(max_length=50)

class investmenter_dresses(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User,  on_delete=models.CASCADE , related_name='investmenter_dresses_set')
    dress = models.OneToOneField('Dresses.Dresses', on_delete=models.CASCADE,related_name='investmenter_dresses')

    class Meta:
        unique_together = ('user', 'dress')

class investmenter_balance(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    user = models.ForeignKey(User,  on_delete=models.CASCADE , related_name='investmenter_bank_set')
    total_balance = models.FloatField(default=0)
    curr_balance = models.FloatField(default=0)

    def __str__(self) -> str:
        return f'{self.user} , {self.total_balance} , {self.curr_balance}'