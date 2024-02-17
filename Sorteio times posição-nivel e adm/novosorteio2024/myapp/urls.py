# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('exibir_times/', views.exibir_times, name='exibir_times'),
    # Adicione outras URLs do seu aplicativo aqui
]
