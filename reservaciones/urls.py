from django.urls import path
from . import views

urlpatterns = [
    # Menú principal
    path('', views.menu_principal, name='menu'),

    # Consultas 1, 2 y 3
    path('horas-pico/', views.horas_pico, name='horas_pico'),
    path('reservaciones-por-dia/', views.reservaciones_por_dia, name='reservaciones_por_dia'),
    path('total-por-estado/', views.total_por_estado, name='total_por_estado'),

    # Consultas 4, 5, y 6
    path('clientes-frecuentes/', views.clientes_frecuentes, name='clientes_frecuentes'),
    path('mesas-populares/', views.mesas_populares, name='mesas_populares'),
    path('tiempo-promedio/', views.tiempo_promedio_estancia, name='tiempo_promedio_estancia'),
]