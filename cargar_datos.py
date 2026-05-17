import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CocinaInteligente.settings')
django.setup()

from reservaciones.models import Cliente, Mesa, Reservacion, Resena

# 1. Cargar reservaciones
df_reservas = pd.read_csv('data/reservaciones.csv')

for _, row in df_reservas.iterrows():
    # Cliente: obtener o crear por nombre
    cliente, _ = Cliente.objects.get_or_create(nombre=row['nombre_cliente'])

    # busca la mesa por numero_mesa, si no existe la crea
    mesa, _ = Mesa.objects.get_or_create(
        numero_mesa=row['numero_mesa'],
        defaults={'capacidad': row['capacidad']}
    )

    # Mesa: crear siempre (si hay duplicada, podrías buscar por capacidad)
    #mesa = Mesa.objects.create(capacidad=row['capacidad'])

    # Reservación
    reservacion = Reservacion.objects.create(
        fecha=pd.to_datetime(row['fecha']).date(),
        hora_inicio=row['hora_inicio'],
        hora_fin=row['hora_fin'],
        numero_personas=row['numero_personas'],
        estado=row['estado'],
        cliente=cliente,
        mesa=mesa
    )

# 2. Cargar reseñas
df_resenas = pd.read_csv('data/resenas.csv')

for _, row in df_resenas.iterrows():
    try:
        cliente = Cliente.objects.get(nombre=row['nombre_cliente'])

        # Buscar reservaciones del cliente que NO tengan reseña aún
        reserva_sin_resena = (
            Reservacion.objects
            .filter(cliente=cliente)
            .exclude(resena__isnull=False)  # que no tenga reseña
            .order_by('-fecha', '-hora_inicio')
            .first()
        )

        if reserva_sin_resena:
            Resena.objects.create(
                calificacion=row['calificacion'],
                reservacion=reserva_sin_resena
            )
        else:
            print(f"Sin reservación disponible para {row['nombre_cliente']}")

    except Cliente.DoesNotExist:
        print(f"Cliente {row['nombre_cliente']} no encontrado")