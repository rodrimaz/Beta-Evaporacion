"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from tasks import views
from tasks.views import EvaporacionListView, EvaporacionUpdateView, EvaporacionDeleteView, falla_editar

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('carga_datos/', views.create_task, name='carga_datos'),
    path('exito/', views.exito, name='exito'),
    path('evaporacion/', views.evaporacion, name='evaporacion'), #vista para carga de datos evaporacion
    path('evaporacionpar/', views.evaporacionpar, name='evaporacionpar'), #vista para carga de datos evaporacionpar
    path('protected/', views.MyView.as_view(), name='protected'),
    path('BD/', views.BD, name='BD'), #vista para acceso a las distintas tablas de la base de datos
    path('evaporaciones/', EvaporacionListView.as_view(), name='evaporacion_list'), #vista para la tabla de evaporacion de la base de datos
    path('evaporaciones/edit/<int:pk>/', EvaporacionUpdateView.as_view(), name='evaporacion_edit'), #llamada a la funcion editar de evaporacion
    path('evaporaciones/delete/<int:pk>/', EvaporacionDeleteView.as_view(), name='evaporacion_delete'), #llamada a la funcion eliminar de evaporacion
    path('export_evaporaciones/', views.export_evaporaciones, name='export_evaporaciones'), #llamada a la funcion exportar de evaporacion
    path('fallas/', views.fallas, name='fallas'),
    path('fallas_lista/', views.fallas_lista, name='fallas_lista'),
    path('editar_falla/<int:id>/', falla_editar, name='falla_editar'),
]

# Agregar la configuración para servir archivos de medios estáticos
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)