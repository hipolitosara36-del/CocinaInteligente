from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Mesa(models.Model):
    numero_mesa = models.IntegerField(unique=True)
    capacidad = models.IntegerField()

    def __str__(self):
        return f"Mesa {self.numero_mesa}"


class Reservacion(models.Model):
    ESTADOS = [
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('no_show', 'No Show'),
    ]

    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    numero_personas = models.IntegerField()
    estado = models.CharField(max_length=15, choices=ESTADOS)

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.fecha} {self.hora_inicio}"


class Resena(models.Model):
    calificacion = models.IntegerField()  # ej: 1 a 5
    reservacion = models.OneToOneField(Reservacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reseña {self.calificacion} para {self.reservacion}"


