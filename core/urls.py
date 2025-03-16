from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('carga_datos/', views.create_task, name='carga_datos'),
    path('exito/', views.exito, name='exito'),
    path('protected/', views.MyView.as_view(), name='protected'),
    path('BD/', views.BD, name='BD'), #vista para acceso a las distintas tablas de la base de datos
    ]