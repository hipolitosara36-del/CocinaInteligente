from django.urls import path
from . import views

urlpatterns = [
    # Menú principal
    path('', views.menu_principal, name='menu'),

    # Consultas
    path('horas-pico/', views.horas_pico, name='horas_pico'),
    path('reservaciones-por-dia/', views.reservaciones_por_dia, name='reservaciones_por_dia'),
    path('total-por-estado/', views.total_por_estado, name='total_por_estado'),
]