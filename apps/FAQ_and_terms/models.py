from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class FAQ(models.Model):
    
    question = models.CharField(max_length=200)
    answer = models.TextField()
    Which_Page = [
        ('Investor', 'Investor'),
        ('user', 'user'),
    ]
    Which_Page = models.CharField(choices=Which_Page , max_length=200)

    class Meta:
        verbose_name = 'F & Q'
        verbose_name_plural = 'F & Q'

class terms_and_condations(models.Model):
    title = models.CharField(max_length=200)
    description = HTMLField()
    Which_Page = [
        ('Investor', 'Investor'),
        ('user', 'user'),
    ]
    Which_Page = models.CharField(choices=Which_Page , max_length=200)

    class Meta:
        verbose_name = 'Terms & Condations'
        verbose_name_plural = 'Terms & Condations'