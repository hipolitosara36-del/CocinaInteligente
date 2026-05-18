from django.shortcuts import render
from django.db.models import Count
from .models import Reservacion, Resena
from django.db.models import Count, Q
from django.db.models import F, ExpressionWrapper, fields
from datetime import timedelta
import re

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


def clientes_frecuentes(request):
    """Consulta 4: Clientes con más reservaciones"""
    from django.db.models import Count

    clientes = (Reservacion.objects
    .values('cliente__nombre')
    .annotate(total=Count('id'))
    .order_by('-total')[:10])  # Top 10 clientes

    context = {
        'consultas': clientes,
        'titulo': 'Clientes Frecuentes',
        'descripcion': 'Top 10 clientes con más reservaciones realizadas',
        'tipo': 'cliente'
    }
    return render(request, 'consulta_base.html', context)


def mesas_populares(request):
    """Consulta 5: Mesas más utilizadas"""
    from django.db.models import Count

    mesas = (Reservacion.objects
    .values('mesa__numero_mesa', 'mesa__capacidad')
    .annotate(total_usos=Count('id'))
    .order_by('-total_usos')[:10])

    # Se agrega información de capacidad en las messas
    for mesa in mesas:
        mesa['display'] = f"Mesa {mesa['mesa__numero_mesa']} (Cap. {mesa['mesa__capacidad']} pers.)"

    context = {
        'consultas': mesas,
        'titulo': 'Mesas Más Utilizadas',
        'descripcion': 'Ranking de mesas con mayor número de reservaciones',
        'tipo': 'mesa'
    }
    return render(request, 'consulta_base.html', context)


def tiempo_promedio_estancia(request):
    """Consulta 6: Tiempo promedio de estancia"""

    # Calcular duración en minutos para cada reservación
    reservaciones = Reservacion.objects.all()

    total_minutos = 0
    count = 0

    for reserva in reservaciones:
        # Convertir hora_inicio y hora_fin a minutos
        inicio_min = reserva.hora_inicio.hour * 60 + reserva.hora_inicio.minute
        fin_min = reserva.hora_fin.hour * 60 + reserva.hora_fin.minute

        # Si la hora_fin es menor (ej: 23:00 a 01:00), sumar 24 horas
        if fin_min < inicio_min:
            fin_min += 24 * 60

        duracion = fin_min - inicio_min
        total_minutos += duracion
        count += 1

    if count > 0:
        promedio_minutos = total_minutos / count
        horas = int(promedio_minutos // 60)
        minutos = int(promedio_minutos % 60)
        promedio_texto = f"{horas} horas y {minutos} minutos"
        promedio_decimal = round(promedio_minutos / 60, 2)
    else:
        promedio_texto = "Sin datos"
        promedio_decimal = 0

    context = {
        'promedio_texto': promedio_texto,
        'promedio_horas': promedio_decimal,
        'total_reservaciones': count,
        'titulo': 'Tiempo Promedio de Estancia',
        'descripcion': 'Duración promedio que los clientes permanecen en el restaurante',
        'tipo': 'tiempo'
    }
    return render(request, 'consulta_tiempo.html', context)

def promedio_personas(request):
    """Consulta 7: Promedio de personas por reservación"""
    from django.db.models import Avg

    promedio = Reservacion.objects.aggregate(promedio=Avg('numero_personas'))
    promedio_valor = round(promedio['promedio'], 2) if promedio['promedio'] else 0

    # Distribución por número de personas
    distribucion = (Reservacion.objects
                    .values('numero_personas')
                    .annotate(total=Count('id'))
                    .order_by('numero_personas'))

    context = {
        'promedio': promedio_valor,
        'distribucion': distribucion,
        'total_reservaciones': Reservacion.objects.count(),
        'titulo': 'Promedio de Personas por Reservación',
        'descripcion': 'Análisis del tamaño promedio de grupos que reservan en el restaurante',
        'tipo': 'promedio'
    }
    return render(request, 'consulta_promedio.html', context)


def reservaciones_por_personas(request):
    """Consulta 8: Número de reservaciones por número de personas"""
    from django.db.models import Count

    grupos = (Reservacion.objects
              .values('numero_personas')
              .annotate(total=Count('id'))
              .order_by('numero_personas'))

    # Calcular porcentajes
    total = Reservacion.objects.count()
    for grupo in grupos:
        grupo['porcentaje'] = round((grupo['total'] / total) * 100, 1) if total > 0 else 0

    context = {
        'consultas': grupos,
        'total': total,
        'titulo': 'Reservaciones por Número de Personas',
        'descripcion': 'Distribución de reservaciones según el tamaño del grupo',
        'tipo': 'grupos'
    }
    return render(request, 'consulta_grupos.html', context)


def cantidad_no_shows(request):
    """Consulta 9: Cantidad de No-Shows"""
    from django.db.models import Count, Q

    no_shows = Reservacion.objects.filter(estado='no_show').count()
    confirmadas = Reservacion.objects.filter(estado='confirmada').count()
    canceladas = Reservacion.objects.filter(estado='cancelada').count()
    total = Reservacion.objects.count()

    porcentaje_no_shows = round((no_shows / total) * 100, 1) if total > 0 else 0
    porcentaje_confirmadas = round((confirmadas / total) * 100, 1) if total > 0 else 0
    porcentaje_canceladas = round((canceladas / total) * 100, 1) if total > 0 else 0

    # Últimos no-shows (para identificar patrones)
    ultimos_no_shows = (Reservacion.objects
    .filter(estado='no_show')
    .select_related('cliente', 'mesa')
    .order_by('-fecha', '-hora_inicio')[:5])

    context = {
        'no_shows': no_shows,
        'confirmadas': confirmadas,
        'canceladas': canceladas,
        'total': total,
        'porcentaje_no_shows': porcentaje_no_shows,
        'porcentaje_confirmadas': porcentaje_confirmadas,
        'porcentaje_canceladas': porcentaje_canceladas,
        'ultimos_no_shows': ultimos_no_shows,
        'titulo': 'Cantidad de No-Shows',
        'descripcion': 'Clientes que no asistieron a su reservación sin cancelar',
        'tipo': 'no_shows'
    }
    return render(request, 'consulta_no_shows.html', context)


def reservaciones_dia_estado(request):
    """Consulta 10: Reservaciones por día y estado (tabla cruzada)"""
    from django.db.models import Count, Q

    # Obtener todas las fechas únicas
    fechas = Reservacion.objects.values('fecha').distinct().order_by('fecha')

    # Estados posibles
    estados = ['confirmada', 'cancelada', 'no_show']
    estados_nombres = {
        'confirmada': '✓ Confirmada',
        'cancelada': '✗ Cancelada',
        'no_show': '⚠ No Show'
    }
    estados_colores = {
        'confirmada': '#28a745',
        'cancelada': '#dc3545',
        'no_show': '#ffc107'
    }

    # Construir tabla de datos
    datos_por_dia = []
    total_por_estado = {estado: 0 for estado in estados}

    for fecha in fechas:
        fila = {
            'fecha': fecha['fecha'],
            'total': 0,
            'estados': {}
        }
        for estado in estados:
            count = Reservacion.objects.filter(fecha=fecha['fecha'], estado=estado).count()
            fila['estados'][estado] = count
            fila['total'] += count
            total_por_estado[estado] += count

        # Solo agregar si tiene al menos una reservación
        if fila['total'] > 0:
            datos_por_dia.append(fila)

    context = {
        'datos_por_dia': datos_por_dia,
        'estados': estados,
        'estados_nombres': estados_nombres,
        'estados_colores': estados_colores,
        'total_por_estado': total_por_estado,
        'total_general': sum(total_por_estado.values()),
        'titulo': 'Reservaciones por Día y Estado',
        'descripcion': 'Distribución detallada de reservaciones: confirmadas, canceladas y no-shows por fecha'
    }
    return render(request, 'consulta_dia_estado.html', context)


def promedio_calificaciones(request):
    """Consulta 11: Promedio de calificación de reseñas"""
    from django.db.models import Avg, Count

    # Promedio general
    promedio = Resena.objects.aggregate(
        promedio=Avg('calificacion'),
        total=Count('id')
    )

    promedio_valor = round(promedio['promedio'], 2) if promedio['promedio'] else 0
    total_resenas = promedio['total'] or 0

    # Distribución de calificaciones (1 a 5 estrellas)
    distribucion = []
    for i in range(1, 6):
        count = Resena.objects.filter(calificacion=i).count()
        porcentaje = round((count / total_resenas) * 100, 1) if total_resenas > 0 else 0
        distribucion.append({
            'estrellas': i,
            'count': count,
            'porcentaje': porcentaje
        })

    # Últimas reseñas
    ultimas_resenas = (Resena.objects
    .select_related('reservacion', 'reservacion__cliente')
    .order_by('-reservacion__fecha', '-reservacion__hora_inicio')[:5])

    # Recomendación según el promedio
    if promedio_valor >= 4.5:
        recomendacion = "Excelente servicio. Mantener la calidad y considerar programa de fidelización."
        color = "#28a745"
    elif promedio_valor >= 4.0:
        recomendacion = "Buen servicio. Identificar áreas de oportunidad para llegar a excelencia."
        color = "#17a2b8"
    elif promedio_valor >= 3.0:
        recomendacion = "Servicio aceptable. Revisar quejas recurrentes y mejorar puntos débiles."
        color = "#ffc107"
    else:
        recomendacion = "Atención prioritaria. Realizar encuestas para identificar problemas graves."
        color = "#dc3545"

    context = {
        'promedio': promedio_valor,
        'total_resenas': total_resenas,
        'distribucion': distribucion,
        'ultimas_resenas': ultimas_resenas,
        'recomendacion': recomendacion,
        'color_recomendacion': color,
        'titulo': 'Promedio de Calificación de Reseñas',
        'descripcion': 'Análisis de satisfacción del cliente basado en reseñas y calificaciones'
    }
    return render(request, 'consulta_calificaciones.html', context)

