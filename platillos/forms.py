from django import forms
from .models import Platillo


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