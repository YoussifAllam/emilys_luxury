from django.db import models
from uuid import uuid4
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3 , default='SAR')
    description = models.TextField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
