from django.urls import path
from . import views

urlpatterns = [
    path('evaporacion/', views.evaporacion, name='evaporacion'), #vista para carga de datos evaporacion
    path('evaporacionpar/', views.evaporacionpar, name='evaporacionpar'), #vista para carga de datos evaporacionpar
    path('evaporaciones/', views.EvaporacionListView.as_view(), name='evaporacion_list'), #vista para la tabla de evaporacion de la base de datos
    path('evaporaciones/edit/<int:pk>/', views.EvaporacionUpdateView.as_view(), name='evaporacion_edit'), #llamada a la funcion editar de evaporacion
    path('evaporaciones/delete/<int:pk>/', views.EvaporacionDeleteView.as_view(), name='evaporacion_delete'), #llamada a la funcion eliminar de evaporacion
    path('export_evaporaciones/', views.export_evaporaciones, name='export_evaporaciones') #llamada a la funcion exportar de evaporacion
]