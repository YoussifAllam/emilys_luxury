
from django.forms import ModelForm
from .models import Dresses , dress_images
from django.forms import inlineformset_factory

class dressImagesForm(ModelForm):
    class Meta:
        model = dress_images
        fields = ['image']

ProductImagesFormSet = inlineformset_factory(Dresses, dress_images, form=dressImagesForm, extra=3)