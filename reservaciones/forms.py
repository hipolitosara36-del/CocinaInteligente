from django import forms
from .models import Reservacion, Cliente, Mesa
from platillos.models import Platillo, Categoria


class ReservacionForm(forms.ModelForm):
    # Campo para nuevo cliente (opcional)
    nuevo_cliente = forms.CharField(
        max_length=100,
        required=False,
        label='O escribe un cliente nuevo',
        help_text='Deja vacío si ya seleccionaste un cliente existente'
    )

    class Meta:
        model = Reservacion
        fields = ['cliente', 'mesa', 'fecha', 'hora_inicio', 'hora_fin', 'numero_personas', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'mesa': forms.Select(attrs={'class': 'form-control'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'cliente': 'Cliente existente',
            'mesa': 'Mesa',
            'fecha': 'Fecha',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de fin',
            'numero_personas': 'Número de personas',
            'estado': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personalizar opciones vacías
        self.fields['cliente'].empty_label = "Seleccione un cliente existente"
        self.fields['mesa'].empty_label = "Seleccione una mesa"

    def save(self, commit=True):
        # Si se escribió un nuevo cliente
        nuevo_cliente_nombre = self.cleaned_data.get('nuevo_cliente')

        if nuevo_cliente_nombre:
            # Crear o obtener el cliente (evita duplicados)
            cliente, created = Cliente.objects.get_or_create(nombre=nuevo_cliente_nombre)
            self.instance.cliente = cliente

        return super().save(commit)



# Formulario para el crud de platillos

class PlatilloForm(forms.ModelForm):

    class Meta:
        model = Platillo

        fields = [
            'nombre',
            'descripcion',
            'precio',
            'categoria',
            'disponible',
            'imagen'
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tacos al Pastor'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del platillo'
            }),

            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),

            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),

            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

        labels = {
            'nombre': 'Nombre del platillo',
            'descripcion': 'Descripción',
            'precio': 'Precio ($)',
            'categoria': 'Categoría',
            'disponible': '¿Disponible?',
            'imagen': 'Imagen del platillo',
        }