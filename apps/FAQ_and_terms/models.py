from django.db import models

# from tinymce.models import HTMLField
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class FAQ(models.Model):

    question = models.CharField(max_length=200)
    answer = CKEditor5Field("Text", config_name="extends")
    Which_Page = [
        ("Investor", "Investor"),
        ("user", "user"),
    ]
    Which_Page = models.CharField(choices=Which_Page, max_length=200)

    class Meta:
        verbose_name = "F & Q"
        verbose_name_plural = "F & Q"

    def __str__(self) -> str:
        return f"{self.question}"


class terms_and_condations(models.Model):
    title = models.CharField(max_length=200)
    # description = HTMLField()
    description = CKEditor5Field("Text", config_name="extends")

    Which_Page = [
        ("Investor", "Investor"),
        ("user", "user"),
    ]
    Which_Page = models.CharField(choices=Which_Page, max_length=200)

    class Meta:
        verbose_name = "Terms & Condations"
        verbose_name_plural = "Terms & Condations"

    def __str__(self) -> str:
        return f"{self.title}"
