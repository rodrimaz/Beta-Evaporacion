from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import evaporacionForm
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.signals import user_logged_in
import datetime
from django.dispatch import receiver
from django.db.models import F
from django.db.models import Q
from django.http import Http404
from .models import Evaporacion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
import openpyxl
from openpyxl.styles import Font
from django.http import HttpResponse
from datetime import datetime
from .forms import FallaForm, FallaEdit
from django.template.loader import render_to_string
from .models import Falla


def falla_editar(request, id):
    falla = get_object_or_404(Falla, id_falla=id)
    if request.method == "POST":
        form = FallaEdit(request.POST, instance=falla)
        if form.is_valid():
            falla_editada = form.save(commit=False)
            falla_editada.fecha_conclusion = timezone.now()
            falla_editada.operario_conclusion = request.user.username
            falla_editada.save()
            return redirect('fallas_lista') 
    else:
        form = FallaEdit(instance=falla)
    return render(request, 'falla_editar.html', {'form': form})

# Funcion carga de fallas nuevas
@login_required(login_url='signin')
def fallas(request):
    if request.method == 'POST':
        form = FallaForm(request.POST, request.FILES)
        if form.is_valid():
            falla = form.save(commit=False)
            falla.operario = request.user  # Aseguramos que el operario es el usuario autenticado
            falla.imagen = request.FILES.get('imagen')
            falla.save()
            
            # Obtener nombre completo del usuario
            usuario_nombre_completo = f"{request.user.first_name} {request.user.last_name}"
            
            # Enviar el correo electrónico
            subject = f"Reporte de fallas del Área {falla.area} sector {falla.parcela_sector}"
            message = f"""
                {usuario_nombre_completo} ha registrado una nueva falla en el Área {falla.area}, sector {falla.parcela_sector}.
                
                Falla: {falla.falla}
                Posible Causa: {falla.posible_causa}
                Posible Solución: {falla.posible_solucion}
                
                ID de la Falla: {falla.id_falla}
                
                Puede ver la información completa entrando al siguiente enlace:
                http://127.0.0.1:8000/fallas_lista/
            """
            try:
                email = EmailMessage(
                    subject,
                    message,
                    'no_reply@bio4.com.ar',  # Dirección desde la cual quieres enviar los correos
                    ['rodrigoimaz@outlook.com'],  # Dirección de correo del destinatario
                    cc=[request.user.email]  # Poner en copia al usuario que carga la falla
                )
                email.send()
            except Exception as e:
                # Registrar el error
                print(f"Error al enviar el correo electrónico: {e}")

            return redirect('fallas_lista')  # Redirigir a una página de éxito o donde desees
        else:
            print("El formulario no es válido")
            print(form.errors)
    else:
        form = FallaForm()
    return render(request, 'fallas.html', {'form': form})

# Funcion para el listado de fallas

def fallas_lista(request):
    fallas = Falla.objects.all().order_by('-fecha')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_id = request.GET.get('search_id')

    if start_date:
        fallas = fallas.filter(fecha__date__gte=start_date)
    if end_date:
        fallas = fallas.filter(fecha__date__lte=end_date)
    if search_id:
        fallas = fallas.filter(id_falla__icontains=search_id)

    return render(request, 'fallas_lista.html', {'fallas': fallas, 'start_date': start_date, 'end_date': end_date, 'search_id': search_id})


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
            evaporacion.Id_evaporacion, evaporacion.fecha, evaporacion.operario, evaporacion.caudal_vl,
            evaporacion.PT01_PT02, evaporacion.PT03, evaporacion.PT04, evaporacion.PT05,
            evaporacion.ST_EFECTO_2_SALIDA, evaporacion.densidad, evaporacion.observaciones,
            evaporacion.OT_EYECTOR_1, evaporacion.OT_EYECTOR_2, evaporacion.potencia_sepevap,
            evaporacion.totalizador_condensado, evaporacion.filetes_FERM, evaporacion.OT_vva_traspaso_ef1_a_ef3,
            evaporacion.viscosidad, evaporacion.temperatura, evaporacion.densidad_LAB, evaporacion.nivel_tk_condensado,
            evaporacion.OT_BO2101, evaporacion.presion_BO2101, evaporacion.presion_ingreso_IC2101,
            evaporacion.presion_egreso_IC2101_ingreso_IC2103, evaporacion.presion_egreso_IC2103,
            evaporacion.presion_ingreso_IC2104, evaporacion.presion_egreso_IC2104, evaporacion.T_ingreso_agua_IC701,
            evaporacion.T_salida_agua_IC701, evaporacion.presion_ingreso_agua_IC701, evaporacion.presion_salida_agua_IC701,
            evaporacion.presion_salida_vahos_IC701
        ])
    
    # Create an HTTP response with the Excel file.
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=evaporaciones.xlsx'
    wb.save(response)
    return response




@method_decorator(login_required, name='dispatch')
class EvaporacionListView(ListView):
    model = Evaporacion
    template_name = 'evaporacion_list.html'
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
    template_name = 'evaporacion_form.html'
    fields = [
        'caudal_vl', 'PT01_PT02', 'PT03', 'PT04', 'PT05', 'ST_EFECTO_2_SALIDA', 'densidad', 'observaciones',
        'OT_EYECTOR_1', 'OT_EYECTOR_2', 'potencia_sepevap', 'totalizador_condensado', 'filetes_FERM',
        'OT_vva_traspaso_ef1_a_ef3', 'viscosidad', 'temperatura', 'densidad_LAB', 'nivel_tk_condensado',
        'OT_BO2101', 'presion_BO2101', 'presion_ingreso_IC2101', 'presion_egreso_IC2101_ingreso_IC2103',
        'presion_egreso_IC2103', 'presion_ingreso_IC2104', 'presion_egreso_IC2104', 'T_ingreso_agua_IC701',
        'T_salida_agua_IC701', 'presion_ingreso_agua_IC701', 'presion_salida_agua_IC701', 'presion_salida_vahos_IC701'
    ]
    success_url = reverse_lazy('evaporacion_list')

# Eliminar campo de la tabla de evaporacion de la base de datos
@method_decorator(login_required, name='dispatch')
class EvaporacionDeleteView(DeleteView):
    model = Evaporacion
    template_name = 'confirm_delete.html' #Utilizable para cualquier eliminar (no depende del tipo de tabla)
    success_url = reverse_lazy('evaporacion_list')


class MyView(LoginRequiredMixin, TemplateView):
    template_name = 'deslogueado.html'
    login_url = 'signin'

#Carga de datos (evaporacion)
@login_required(login_url='signin')
def evaporacion(request):
    if request.method == 'POST':
        hora = timezone.now()
        print(hora)
        # Obtener los valores del formulario
        PT04 = request.POST.get('PT04', 0)
        PT05 = request.POST.get('PT05', 0)
        PT03 = request.POST.get('PT03', 0)
        OTEYECTOR1 = request.POST.get('OTEYECTOR1', 0)
        PT01PT02 = request.POST.get('PT01PT02', 0)
        OTEYECTOR2 = request.POST.get('OTEYECTOR2', 0)
        PRESIONBO2101 = request.POST.get('PRESIONBO2101', 0)
        PRESIONOUTIC2103  = request.POST.get('PRESIONOUTIC2103', 0)
        PRESIONINIC2104 = request.POST.get('PRESIONINIC2104', 0)
        PRESIONOUTIC2104 = request.POST.get('PRESIONOUTIC2104', 0)
        PRESIONOUTIC2101 = request.POST.get('PRESIONOUTIC2101', 0)
        PRESIONINIC2101 = request.POST.get('PRESIONINIC2101', 0)
        CONDENSADO = request.POST.get('CONDENSADO', 0)
        POTENCIAINSTA = request.POST.get('POTENCIAINSTA', 0)
        OTBO2101 = request.POST.get('OTBO2101', 0)
        LCV01 = request.POST.get('LCV01', 0)
        CAUDALVL = request.POST.get('CAUDALVL', 0)
        ST2EF = request.POST.get('ST2EF', 0)
        DENSIDAD = request.POST.get('DENSIDAD', 0)
        OBS= request.POST.get('OBS', 0)
        # Crear una instancia del modelo Evaporacion con los valores del formulario
        evaporacion = Evaporacion(
            
            operario=request.user.username,
            caudal_vl=float(CAUDALVL),  
            PT01_PT02=float(PT01PT02),
            PT03=float(PT03),
            PT04=float(PT04),
            PT05=float(PT05),
            ST_EFECTO_2_SALIDA=float(ST2EF),
            densidad=float(DENSIDAD),
            observaciones=(OBS),
            OT_EYECTOR_1=float(OTEYECTOR1),
            OT_EYECTOR_2=float(OTEYECTOR2),
            potencia_sepevap=float(POTENCIAINSTA),
            totalizador_condensado=float(CONDENSADO),
            filetes_FERM=0,
            OT_vva_traspaso_ef1_a_ef3=float(LCV01),
            viscosidad=0,
            temperatura=0,
            densidad_LAB=0,
            nivel_tk_condensado=0,
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
            presion_salida_vahos_IC701=0
        )

        # Guardar la instancia en la base de datos
        evaporacion.save()

        # Redirigir a la página de éxito o a donde desees
        return redirect('exito')

    return render(request, 'evaporacion.html')  # Ajusta el nombre del template según tu estructura

#Carga de datos (evaporacion)
@login_required(login_url='signin')
def evaporacionpar(request):
    if request.method == 'POST':
        hora = timezone.now()
        print(hora)
        # Obtener los valores del formulario y los guarda en variables
        PT04 = request.POST.get('PT04', 0)
        PT05 = request.POST.get('PT05', 0)
        PT03 = request.POST.get('PT03', 0)
        OTEYECTOR1 = request.POST.get('OTEYECTOR1', 0)
        PT01PT02 = request.POST.get('PT01PT02', 0)
        OTEYECTOR2 = request.POST.get('OTEYECTOR2', 0)
        CONDENSADO = request.POST.get('CONDENSADO', 0)
        POTENCIAINSTA = request.POST.get('POTENCIAINSTA', 0)
        CAUDALVL = request.POST.get('CAUDALVL', 0)
        ST2EF = request.POST.get('ST2EF', 0)
        DENSIDAD = request.POST.get('DENSIDAD', 0)
        OBS= request.POST.get('OBS', 0)
        TINGRESO = request.POST.get('TINGRESO', 0)
        TEGRESO = request.POST.get('TEGRESO', 0)
        PRESIONINGRESO = request.POST.get('PRESIONINGRESO', 0)
        PRESIONSALIDA = request.POST.get('PRESIONSALIDA', 0)
        PRESIONIC701 = request.POST.get('PRESIONIC701', 0)
        LCV01 = request.POST.get('LCV01', 0)
        # Crear una instancia del modelo Evaporacion con los valores del formulario, se le asigna a cada campo del modelo, su variable correspondiente
        evaporacion = Evaporacion(
            
            operario=request.user.username,
            caudal_vl=float(CAUDALVL), 
            PT01_PT02=float(PT01PT02),
            PT03=float(PT03),
            PT04=float(PT04),
            PT05=float(PT05),
            ST_EFECTO_2_SALIDA=float(ST2EF),
            densidad=float(DENSIDAD),
            observaciones=(OBS),
            OT_EYECTOR_1=float(OTEYECTOR1),
            OT_EYECTOR_2=float(OTEYECTOR2),
            potencia_sepevap=float(POTENCIAINSTA),
            totalizador_condensado=float(CONDENSADO),
            filetes_FERM=0,
            OT_vva_traspaso_ef1_a_ef3=float(LCV01),
            viscosidad=0,
            temperatura=0,
            densidad_LAB=0,
            nivel_tk_condensado=0,
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
        )

        # Guardar la instancia en la base de datos
        evaporacion.save()

        # Redirigir a la página de éxito o a donde desees
        return redirect('exito')

    return render(request, 'evaporacionpar.html')




#Acceso a pantalla de EXITO
def exito(request):
    return render(request, 'exito.html')


#Acceso a pantalla de Carga de datos
@login_required(login_url='signin')
def create_task(request):
    return render(request, 'carga_datos.html')

#Acceso a pantalla de Base de datos
@login_required(login_url='signin')
def BD(request):
    return render(request, 'BD.html')

#Acceso a pantalla HOME
def home(request):
    return render(request, 'home.html')

#Desconexion manual
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('home')

#Logueo
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('home')

