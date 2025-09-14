# visualizacion_expedientes/urls.py
from django.urls import path
from . import views

app_name = 'visualizacion_expedientes'

urlpatterns = [
    path('expedientes-jerarquicos/', views.expedientes_jerarquicos, name='expedientes_jerarquicos'),
]