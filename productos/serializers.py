# productos/serializers.py

from rest_framework import serializers
from .models import Producto, Categoria, ProductoCategoria

class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer simple para el modelo Categoria.
    Lo usaremos para anidarlo en otros serializers.
    """
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'estado']

class ProductoCategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo intermedio ProductoCategoria.
    Nos permite mostrar los detalles de la categoría anidada.
    """
    # Anidamos el CategoriaSerializer aquí. 'read_only=True' porque
    # la gestionaremos desde el producto, no directamente.
    categoria = CategoriaSerializer(read_only=True)
    
    class Meta:
        model = ProductoCategoria
        fields = ['categoria', 'es_principal']

class ProductoSerializer(serializers.ModelSerializer):
    """
    Serializer mejorado para el modelo Producto.
    """
    # Usamos el serializer del modelo intermedio para representar la relación.
    # 'source' le dice a DRF que busque el atributo 'productocategoria_set'
    # en la instancia del Producto para obtener los datos.
    # 'many=True' porque un producto puede tener muchas categorías.
    categorias_asociadas = ProductoCategoriaSerializer(
        source='productocategoria_set', 
        many=True, 
        read_only=True
    )

    class Meta:
        model = Producto
        fields = [
            'id', 
            'codigo', 
            'nombre', 
            'descripcion', 
            'stock', 
            'estado',
            'categorias_asociadas', # Añadimos el nuevo campo anidado
        ]

    # --- Validación Personalizada ---
    def validate_codigo(self, value):
        """
        Asegura que el código (SKU) solo contenga letras, números y guiones.
        """
        if not value.isalnum() and '-' not in value:
            # Si la validación falla, lanzamos un error.
            raise serializers.ValidationError("El código SKU solo puede contener letras, números y guiones.")
        return value