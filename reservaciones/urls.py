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

# Consultas 7, 8, 9
    path('promedio-personas/', views.promedio_personas, name='promedio_personas'),
    path('reservaciones-por-personas/', views.reservaciones_por_personas, name='reservaciones_por_personas'),
    path('cantidad-no-shows/', views.cantidad_no_shows, name='cantidad_no_shows'),

# Consultas 10, 11
    path('reservaciones-dia-estado/', views.reservaciones_dia_estado, name='reservaciones_dia_estado'),
    path('promedio-calificaciones/', views.promedio_calificaciones, name='promedio_calificaciones'),
]