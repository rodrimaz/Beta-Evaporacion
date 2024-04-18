from django.forms import ModelForm
from .models import Evaporacion
from django import forms


class evaporacionForm(forms.ModelForm):
    class Meta:
        model = Evaporacion
        exclude = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            # Añade otros widgets si es necesario
        }
