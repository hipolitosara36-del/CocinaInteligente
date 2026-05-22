from django.urls import path
from . import views

urlpatterns = [

    path('', views.lista_platillos, name='lista_platillos'),

    path('crear/', views.crear_platillo, name='crear_platillo'),

    path('<int:id>/', views.detalle_platillo, name='detalle_platillo'),

    path('editar/<int:id>/', views.editar_platillo, name='editar_platillo'),

    path('eliminar/<int:id>/', views.eliminar_platillo, name='eliminar_platillo'),

    path('buscar/', views.buscar_platillos, name='buscar_platillos'),

    path(
        'disponibilidad/',
        views.filtrar_por_disponibilidad,
        name='filtrar_por_disponibilidad'
    ),

]