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
from django.contrib import admin
from django.urls import path
from tasks import views
from tasks.views import EvaporacionListView, EvaporacionUpdateView, EvaporacionDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('carga_datos/', views.create_task, name='carga_datos'),
    path('exito/', views.exito, name='exito'),
    path('evaporacion/', views.evaporacion, name='evaporacion'),
    path('evaporacionpar/', views.evaporacionpar, name='evaporacionpar'),
    path('protected/', views.MyView.as_view(), name='protected'),
    path('BD/', views.BD, name='BD'),
    path('evaporaciones/', EvaporacionListView.as_view(), name='evaporacion_list'),
    path('evaporaciones/edit/<int:pk>/', EvaporacionUpdateView.as_view(), name='evaporacion_edit'),
    path('evaporaciones/delete/<int:pk>/', EvaporacionDeleteView.as_view(), name='evaporacion_delete'),
]
