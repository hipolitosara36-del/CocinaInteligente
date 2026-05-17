from django.shortcuts import render
from django.db.models import Count
from .models import Reservacion


def menu_principal(request):
    """Menú principal con acceso a las consultas"""
    return render(request, 'menu.html')


def horas_pico(request):
    """Consulta 1: Horas con más reservaciones"""
    horas = (Reservacion.objects
    .values('hora_inicio')
    .annotate(total=Count('id'))
    .order_by('-total')[:10])

    context = {
        'consultas': horas,
        'titulo': 'Horas Pico',
        'descripcion': 'Horarios con mayor demanda de reservaciones'
    }
    return render(request, 'consulta_base.html', context)


def reservaciones_por_dia(request):
    """Consulta 2: Reservaciones por día"""
    dias = (Reservacion.objects
            .values('fecha')
            .annotate(total=Count('id'))
            .order_by('fecha'))

    context = {
        'consultas': dias,
        'titulo': 'Reservaciones por Día',
        'descripcion': 'Cantidad de reservaciones por fecha'
    }
    return render(request, 'consulta_base.html', context)


def total_por_estado(request):
    """Consulta 3: Total por estado"""
    estados = (Reservacion.objects
               .values('estado')
               .annotate(total=Count('id')))

    context = {
        'consultas': estados,
        'titulo': 'Reservaciones por Estado',
        'descripcion': 'Distribución de estados de reservaciones'
    }
    return render(request, 'consulta_base.html', context)