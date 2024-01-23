from django.forms import ModelForm
from .models import Evaporacion
from django import forms


class evaporacionForm(forms.ModelForm):
    class Meta:
        model = Evaporacion
        exclude = ['Id_evaporacion', 'fecha', 'operario']
