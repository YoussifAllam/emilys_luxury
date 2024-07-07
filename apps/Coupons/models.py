from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_to = models.DateTimeField(verbose_name='Valid to date')
    discount = models.IntegerField(
        verbose_name='discount Percentage value',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='discount Percentage value should be between 0 and 100'
    )

    def __str__(self):
        return self.code 