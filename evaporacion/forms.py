from .models import Evaporacion
from django import forms

#formulario para la edicion de la tabla de sql de evaporacion
class evaporacionForm(forms.ModelForm):
    class Meta:
        model = Evaporacion
        exclude = ['id', 'fecha', 'operario']
        
#formulario para el filtrado de fechas        
class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
