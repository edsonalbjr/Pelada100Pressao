from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Outras URLs do seu aplicativo aqui
]
