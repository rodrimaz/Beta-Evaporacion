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
        "ID", "Fecha", "Operario", "Caudal VL", "PT01_PT02", "PT03", "PT04", "PT05",
        "ST Efecto 2 Salida", "Densidad", "Observaciones", "OT Eyector 1", "OT Eyector 2",
        "Potencia SepEvap", "Totalizador Condensado", "Filetes FERM", "OT VVA Traspaso Ef1 a Ef3",
        "Viscosidad", "Temperatura", "Densidad LAB", "Nivel TK Condensado", "OT BO2101",
        "Presión BO2101", "Presión Ingreso IC2101", "Presión Egreso IC2101 Ingreso IC2103",
        "Presión Egreso IC2103", "Presión Ingreso IC2104", "Presión Egreso IC2104",
        "T Ingreso Agua IC701", "T Salida Agua IC701", "Presión Ingreso Agua IC701",
        "Presión Salida Agua IC701", "Presión Salida Vahos IC701"
    ]
    ws.append(headers)
    
    # se agregan los campos de la tabla de sql (modelo)
    for evaporacion in evaporaciones:
        ws.append([
            evaporacion.id, 
            evaporacion.fecha, 
            evaporacion.operario, 
            evaporacion.totalizador_condensado,
            evaporacion.OT_BO2101, 
            evaporacion.presion_BO2101, 
            evaporacion.presion_ingreso_IC2101,
            evaporacion.presion_egreso_IC2101_ingreso_IC2103, 
            evaporacion.presion_egreso_IC2103,
            evaporacion.presion_ingreso_IC2104, 
            evaporacion.presion_egreso_IC2104, 
            evaporacion.T_ingreso_agua_IC701,
            evaporacion.T_salida_agua_IC701, 
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
        'presion_BO2101', 
        'presion_ingreso_IC2101', 
        'presion_egreso_IC2101_ingreso_IC2103', 
        'presion_egreso_IC2103', 
        'presion_ingreso_IC2104', 
        'presion_egreso_IC2104', 
        'T_ingreso_agua_IC701', 
        'T_salida_agua_IC701', 
        'presion_ingreso_agua_IC701', 
        'przesion_salida_agua_IC701', 
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
        hora = timezone.now()
        # Obtener los valores del formulario
        PRESIONBO2101 = request.POST.get('PRESIONBO2101', 0)
        PRESIONOUTIC2103  = request.POST.get('PRESIONOUTIC2103', 0)
        PRESIONINIC2104 = request.POST.get('PRESIONINIC2104', 0)
        PRESIONOUTIC2104 = request.POST.get('PRESIONOUTIC2104', 0)
        PRESIONOUTIC2101 = request.POST.get('PRESIONOUTIC2101', 0)
        PRESIONINIC2101 = request.POST.get('PRESIONINIC2101', 0)
        OTBO2101 = request.POST.get('OTBO2101', 0)
        OBS= request.POST.get('OBS', 0)
        # Crear una instancia del modelo Evaporacion con los valores del formulario
        evaporacion = Evaporacion(
            operario=request.user.username,
            totalizador_condensado=0,
            OT_BO2101=float(OTBO2101),
            presion_BO2101=float(PRESIONBO2101),
            presion_ingreso_IC2101=float(PRESIONINIC2101),
            presion_egreso_IC2101_ingreso_IC2103=float(PRESIONOUTIC2101),
            presion_egreso_IC2103=float(PRESIONOUTIC2103),
            presion_ingreso_IC2104=float(PRESIONINIC2104),
            presion_egreso_IC2104=float(PRESIONOUTIC2104),
            T_ingreso_agua_IC701=0,
            T_salida_agua_IC701=0,
            presion_ingreso_agua_IC701=0,
            presion_salida_agua_IC701=0,
            presion_salida_vahos_IC701=0,
            observaciones=(OBS)
        )

        # Guardar la instancia en la base de datos
        evaporacion.save()

        # Redirigir a la página de éxito o a donde desees
        return redirect('exito')

    return render(request, 'evaporacion/evaporacion.html')  # Ajusta el nombre del template según tu estructura

#Carga de datos (evaporacion)
@login_required(login_url='signin')
def evaporacionpar(request):
    if request.method == 'POST':
        hora = timezone.now()
        print(hora)
        # Obtener los valores del formulario y los guarda en variables
        TINGRESO = request.POST.get('TINGRESO', 0)
        TEGRESO = request.POST.get('TEGRESO', 0)
        PRESIONINGRESO = request.POST.get('PRESIONINGRESO', 0)
        PRESIONSALIDA = request.POST.get('PRESIONSALIDA', 0)
        PRESIONIC701 = request.POST.get('PRESIONIC701', 0)
        # Crear una instancia del modelo Evaporacion con los valores del formulario, se le asigna a cada campo del modelo, su variable correspondiente
        evaporacion = Evaporacion(
            operario=request.user.username,
            totalizador_condensado=0,
            OT_BO2101=0,
            presion_BO2101=0,
            presion_ingreso_IC2101=0,
            presion_egreso_IC2101_ingreso_IC2103=0,
            presion_egreso_IC2103=0,
            presion_ingreso_IC2104=0,
            presion_egreso_IC2104=0,
            T_ingreso_agua_IC701= float(TINGRESO),
            T_salida_agua_IC701= float(TEGRESO),
            presion_ingreso_agua_IC701= float(PRESIONINGRESO),
            presion_salida_agua_IC701= float(PRESIONSALIDA),
            presion_salida_vahos_IC701= float(PRESIONIC701),
            observaciones=''
        )

        # Guardar la instancia en la base de datos
        evaporacion.save()

        # Redirigir a la página de éxito o a donde desees
        return redirect('exito')

    return render(request, 'evaporacion/evaporacionpar.html')



