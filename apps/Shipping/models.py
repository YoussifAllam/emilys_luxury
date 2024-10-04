from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Shipping(models.Model):
    flatRate = models.FloatField(verbose_name="Shipping Flat rate", default=0)

    class Meta:
        verbose_name = "Shipping Flat rate"
        verbose_name_plural = "Shipping Flat rate"

    def delete(self, *args, **kwargs):
        raise ValidationError("Deletion of this object is not allowed.")

    @staticmethod
    def can_create_popup():
        return not Shipping.objects.exists()

    def save(self, *args, **kwargs):
        if not self.pk and not Shipping.can_create_popup():
            raise ValidationError("Cannot create more than one Shipping instance.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Shaping Flat Rate : $ {self.flatRate}"


class INSURANCE(models.Model):
    INSURANCE = models.FloatField(verbose_name="INSURANCE amount", default=0)

    class Meta:
        verbose_name = "INSURANCE"
        verbose_name_plural = "INSURANCE"

    def delete(self, *args, **kwargs):
        raise ValidationError("Deletion of this object is not allowed.")

    @staticmethod
    def can_create_popup():
        return not INSURANCE.objects.exists()

    def save(self, *args, **kwargs):
        if not self.pk and not INSURANCE.can_create_popup():
            raise ValidationError("Cannot create more than one Shipping instance.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"INSURANCE : $ {self.INSURANCE}"
