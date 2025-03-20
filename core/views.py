from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

class MyView(LoginRequiredMixin, TemplateView):
    template_name = 'core/deslogueado.html'
    login_url = 'signin'

#Acceso a pantalla de EXITO
def exito(request):
    return render(request, 'core/exito.html')

#Acceso a pantalla de Carga de datos
@login_required(login_url='signin')
def create_task(request):
    return render(request, 'core/carga_datos.html')

#Acceso a pantalla de Base de datos
@login_required(login_url='signin')
def BD(request):
    return render(request, 'core/BD.html')

#Acceso a pantalla HOME
def home(request):
    return render(request, 'core/home.html')

#Desconexion manual
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('home')

#Logueo
def signin(request):
    if request.method == 'GET':
        return render(request, 'core/signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'core/signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('home')