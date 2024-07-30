from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here.

class SiteOwner_receivable(models.Model):
    Percentage = models.FloatField( help_text='Percentage due to the website owner make sure its between 0 and 100' , default = 0,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)]
                                   )

    def delete(self, *args, **kwargs):
        raise ValidationError("Deletion of this object is not allowed.")

    @staticmethod
    def can_create_popup():
        return not SiteOwner_receivable.objects.exists()

    def save(self, *args, **kwargs):
        if not self.pk and not SiteOwner_receivable.can_create_popup():
            raise ValidationError("Cannot create more than one Popup instance.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.Percentage}'
    