from django.forms import forms, ModelForm

from .models import Product


class createForm(ModelForm):
    class Meta:
        model = Product
        fields='__all__'
