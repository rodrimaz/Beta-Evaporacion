from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import openpyxl
from datetime import datetime
from .models import Evaporacion
from .forms import EvaporacionForm

# Exportar lista a EXCEL
def export_evaporaciones(request):
    evaporaciones = Evaporacion.objects
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filename = "Evaporaciones"
    if start_date:
        evaporaciones = evaporaciones.filter(fecha__date__gte=start_date)
        filename += "_from_" + start_date
    if end_date:
        evaporaciones = evaporaciones.filter(fecha__date__lte=end_date)
        filename += "_to_" + end_date
    filename += ".xlsx"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Evaporaciones"
    
    headers = [field.verbose_name for field in Evaporacion._meta.get_fields()]  
    ws.append(headers)
    for evaporacion in evaporaciones.values():
        ws.append(list(evaporacion.values()))

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    wb.save(response)
    return response

@method_decorator(login_required, name='dispatch')
class EvaporacionListView(ListView):
    model = Evaporacion
    paginate_by = 100
    template_name = 'evaporacion/evaporacion_list.html'
    context_object_name = 'evaporaciones'
    ordering = ['-operario', '-fecha']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        if start_date:
            queryset = queryset.filter(fecha__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(fecha__date__lte=end_date)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        context['display'] = 'none' if not context['start_date'] and not context['end_date'] else 'block'
        context['headers'] = [field.verbose_name for field in Evaporacion._meta.get_fields()] + ['Acciones']
        return context
    
#Edicion de tabla evaporacion de la base de datos
@method_decorator(login_required, name='dispatch')
class EvaporacionUpdateView(UpdateView):
    model = Evaporacion
    template_name = 'evaporacion/evaporacion_form.html'
    fields = [
        'totalizador_condensado', 
        'OT_BO2101', 
        'presion_salida_IC2102',
        'presion_BO2101',
        'presion_ingreso_IC2101', 
        'presion_egreso_IC2101_ingreso_IC2103', 
        'presion_egreso_IC2103', 
        'temp_ingreso_agua_IC701', 
        'temp_salida_agua_IC701', 
        'presion_ingreso_agua_IC701', 
        'presion_salida_agua_IC701', 
        'presion_salida_vahos_IC701',
        'observaciones'
    ]
    success_url = reverse_lazy('evaporacion_list')

@method_decorator(login_required, name='dispatch')
class EvaporacionDeleteView(DeleteView):
    model = Evaporacion
    template_name = 'evaporacion/confirm_delete.html'
    success_url = reverse_lazy('evaporacion_list')

#Carga de datos (evaporacion)
@login_required(login_url='signin')
def evaporacion(request):
    if request.method == 'POST':
        form = EvaporacionForm(request.POST)
        if form.is_valid():
            evaporacion = Evaporacion(
                operario=request.user.username,
                OT_BO2101=float(form.cleaned_data['OT_BO2101']),
                presion_salida_IC2102=float(form.cleaned_data['presion_salida_IC2102']),
                presion_BO2101=float(form.cleaned_data['presion_BO2101']),
                presion_ingreso_IC2101=float(form.cleaned_data['presion_ingreso_IC2101']),
                presion_egreso_IC2101_ingreso_IC2103=float(form.cleaned_data['presion_egreso_IC2101_ingreso_IC2103']),
                presion_egreso_IC2103=float( form.cleaned_data['presion_egreso_IC2103']),
                observaciones=form.cleaned_data['observaciones']
            )
            evaporacion.save()
            return redirect('exito')
    return render(request, 'evaporacion/evaporacion.html')

#Carga de datos (evaporacion)
@login_required(login_url='signin')
def evaporacionpar(request):
    if request.method == 'POST':
        form = EvaporacionForm(request.POST)
        if form.is_valid():
            evaporacion_par = Evaporacion(
                operario=request.user.username,
                totalizador_condensado= float(form.cleaned_data['totalizador_condensado']),
                temp_ingreso_agua_IC701= float(form.cleaned_data['temp_ingreso_agua_IC701']),
                temp_salida_agua_IC701= float(form.cleaned_data['temp_salida_agua_IC701']),
                presion_ingreso_agua_IC701= float(form.cleaned_data['presion_ingreso_agua_IC701']),
                presion_salida_agua_IC701= float(form.cleaned_data['presion_salida_agua_IC701']),
                presion_salida_vahos_IC701= float(form.cleaned_data['presion_salida_vahos_IC701']),
                observaciones=form.cleaned_data['observaciones']
            )
            evaporacion_par.save()
            return redirect('exito')

    return render(request, 'evaporacion/evaporacionpar.html')



