from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class user_invitation_points(models.Model):
    user = models.OneToOneField('Users.User' , on_delete=models.CASCADE , related_name='user_invitation_points_set')
    num_of_points = models.IntegerField(default=0)

    # class Meta:
    #     unique_together = (('user', 'num_of_points'))


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

