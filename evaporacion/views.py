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
    evaporaciones = Evaporacion.objects.all()
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        try:
            # configuracion para que la DESCARGA filtrada por fechas sea desde-hasta (inclusives)
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            end_date_obj = end_date_obj.replace(hour=23, minute=59, second=59)
            evaporaciones = evaporaciones.filter(fecha__range=[start_date, end_date_obj])
        except ValueError:
            
            pass

    # Create an in-memory workbook and add a worksheet.
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Evaporaciones"
    
    # inlcuir los titulos de las columnas
    headers = [
        "ID", 
        "Fecha", 
        "Operario",
        'Totalizador condensado (m3)',
        'OT BO2101 (%)',
        'Presión de salida del IC2102',
        'Presion BO2101',
        'Presion Ingreso IC2101',
        'Presion Egreso IC2101/Ingreso IC2103',
        'Presion Egreso IC2103',
        'Temp Ingreso Agua IC701 (°C)',
        'Temp Salida Agua IC701 (°C)',
        'Presión Ingreso Agua IC701 (bar)',
        'Presión Salida Agua IC701 (bar)',
        'Presión Salida Vahos IC701 (bar)',
        'Observaciones']
    ws.append(headers)

    for evaporacion in evaporaciones:
        ws.append([
            evaporacion.id, 
            evaporacion.fecha, 
            evaporacion.operario, 
            evaporacion.totalizador_condensado,
            evaporacion.OT_BO2101,
            evaporacion.presion_salida_IC2102,
            evaporacion.presion_BO2101, 
            evaporacion.presion_ingreso_IC2101,
            evaporacion.presion_egreso_IC2101_ingreso_IC2103, 
            evaporacion.presion_egreso_IC2103,
            evaporacion.temp_ingreso_agua_IC701,
            evaporacion.temp_salida_agua_IC701, 
            evaporacion.presion_ingreso_agua_IC701, 
            evaporacion.presion_salida_agua_IC701,
            evaporacion.presion_salida_vahos_IC701,
            evaporacion.observaciones
        ])
    
    # Create an HTTP response with the Excel file.
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=evaporaciones.xlsx'
    wb.save(response)
    return response

@method_decorator(login_required, name='dispatch')
class EvaporacionListView(ListView):
    model = Evaporacion
    paginate_by = 100
    template_name = 'evaporacion/evaporacion_list.html'
    context_object_name = 'evaporaciones'
    ordering = ['-fecha']

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date and end_date:
            # configuracion para que la busqueda por fechas sea desde-hasta (inclusives)
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)
            queryset = queryset.filter(fecha__range=[start_date, end_date])
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
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

# Eliminar campo de la tabla de evaporacion de la base de datos
@method_decorator(login_required, name='dispatch')
class EvaporacionDeleteView(DeleteView):
    model = Evaporacion
    template_name = 'evaporacion/confirm_delete.html' #Utilizable para cualquier eliminar (no depende del tipo de tabla)
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



