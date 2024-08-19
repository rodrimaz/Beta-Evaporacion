from django.forms import ModelForm
from .models import Evaporacion, Falla
from django import forms
from .models import Parcelascsv  # Asegúrate de que Parcelascsv es el modelo adecuado

class FallaForm(forms.Form):
    parcela_sector = forms.ModelChoiceField(
        queryset=Parcelascsv.objects.all(),  # Recupera todas las parcelas
        to_field_name='parcela',  # Muestra los valores de la columna 'parcela'
        label='Parcela/Sector',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    falla = forms.CharField(max_length=255, label='Falla', widget=forms.TextInput(attrs={'class': 'form-control'}))
    posible_causa = forms.CharField(max_length=255, label='Posible Causa', widget=forms.TextInput(attrs={'class': 'form-control'}))
    posible_solucion = forms.CharField(max_length=255, label='Posible Solución', widget=forms.TextInput(attrs={'class': 'form-control'}))
    imagen = forms.ImageField(label='Imagen', required=False)
#formulario para la EDICION de fallas

class FallaEdit(forms.ModelForm):
    ESTADO_CHOICES = [
        ('Anulada', 'Anulada'),
        ('Finalizada', 'Finalizada')
    ]
    
    estado = forms.ChoiceField(choices=ESTADO_CHOICES)

    class Meta:
        model = Falla
        fields = ['estado', 'conclusion']


            
#formulario para la edicion de la tabla de sql de evaporacion
class evaporacionForm(forms.ModelForm):
    class Meta:
        model = Evaporacion
        exclude = ['Id_evaporacion', 'fecha', 'operario']
        
#formulario para el filtrado de fechas        
class DateFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
