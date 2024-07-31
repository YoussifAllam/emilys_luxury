from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
# from uuid import uuid4
import random
import string
# Create your models here.

class user_invitation_points(models.Model):
    user_code = models.CharField(max_length=10, unique=True, editable=False)
    user = models.OneToOneField('Users.User', on_delete=models.CASCADE, related_name='user_invitation_points_set')
    num_of_points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.user_code:
            self.user_code = self.generate_unique_user_code()
        super(user_invitation_points, self).save(*args, **kwargs)

    def generate_unique_user_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not user_invitation_points.objects.filter(user_code=code).exists():
                return code


class invitation_points_Trade(models.Model):
    num_of_points_for_code = models.IntegerField(
        default=0,
        verbose_name = 'number of points for code',
        help_text = 'number of points that user need to change it with coupons' , 
        
    )
    discount = models.IntegerField(
        verbose_name='discount Percentage value',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='coupon discount Percentage value should be between 0 and 100'
    )

    class Meta:
        verbose_name = 'Trade points'
        verbose_name_plural = 'Trade points'

    def delete(self, *args, **kwargs):
        raise ValidationError("Deletion of this object is not allowed.")

    @staticmethod
    def can_create_popup():
        return not invitation_points_Trade.objects.exists()

    def save(self, *args, **kwargs):
        if not self.pk and not invitation_points_Trade.can_create_popup():
            raise ValidationError("Cannot create more than one Popup instance.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.num_of_points_for_code}'
    