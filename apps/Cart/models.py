from django.db import models
from uuid import uuid4
# Create your models here.

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Cart_Items(models.Model):
    status_choices = (
        {
            '3' : '3' ,
            '6' : '6' , 
            '8' : '8' , 
        }
    )
    id  = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cart = models.ForeignKey(Cart, related_name='items_set', on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    dress = models.ForeignKey('Dresses.Dresses', on_delete=models.CASCADE)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    booking_for_n_days = models.CharField(choices=status_choices , max_length=2)

    class Meta:
        db_table = 'Cart'
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.dress} "