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
from django.shortcuts import render, redirect
from .models import Evaporacion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class MyView(LoginRequiredMixin, TemplateView):
    template_name = 'deslogueado.html'
    login_url = 'signin'


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
            caudal_vl=float(CAUDALVL),  # Puedes ajustar esto según cómo manejes la autenticación de usuarios
              # Asignar el valor que corresponda o ajustar según tus necesidades
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

@login_required(login_url='signin')
def evaporacionpar(request):
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
        # Crear una instancia del modelo Evaporacion con los valores del formulario
        evaporacion = Evaporacion(
            
            operario=request.user.username,
            caudal_vl=float(CAUDALVL),  # Puedes ajustar esto según cómo manejes la autenticación de usuarios
              # Asignar el valor que corresponda o ajustar según tus necesidades
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





def exito(request):
    return render(request, 'exito.html')



def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})





@login_required(login_url='signin')
def create_task(request):
    return render(request, 'carga_datos.html')


def home(request):
    return render(request, 'home.html')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('home')


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

