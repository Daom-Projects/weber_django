# productos/forms.py
from django import forms
from .models import Producto
from core.enums import EstadoProducto

class ProductoForm(forms.ModelForm):
    """
    Formulario generado a partir del modelo Producto.
    """
    class Meta:
        model = Producto
        # Especificamos los campos del modelo que queremos incluir en el formulario.
        # Omitimos campos como 'stock' que se calcularán automáticamente.
        fields = [
            'codigo',
            'nombre',
            'descripcion',
            'stock_minimo',
            'estado',
            # ¡No incluimos 'categorias' aquí! Lo manejaremos de otra forma.
        ]

        # Opcional: Para añadir clases de CSS y otros atributos a los campos HTML.
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }