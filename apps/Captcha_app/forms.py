# myapp/forms.py

from django import forms
from captcha.fields import CaptchaField


class MyForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    captcha = CaptchaField()  # Add the CAPTCHA field
