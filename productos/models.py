# productos/models.py
from django.db import models
from safedelete.models import SafeDeleteModel
from core.enums import EstadoGeneral, EstadoProducto

class Categoria(SafeDeleteModel):
    """
    Categorías jerárquicas para los productos.
    Una categoría puede tener una categoría padre.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)

    # Para categorías jerárquicas, nos relacionamos con el mismo modelo.
    # on_delete=SET_NULL: si se borra una categoría padre, sus hijas no se borran,
    # simplemente se quedan sin padre (se vuelven de nivel superior).
    categoria_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategorias'
    )

    estado = models.CharField(
        max_length=10,
        choices=EstadoGeneral.choices(),
        default=EstadoGeneral.ACTIVO
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
        # Asegura que no haya dos categorías con el mismo nombre bajo el mismo padre.
        unique_together = [['nombre', 'categoria_padre']]

    def __str__(self):
        return self.nombre

class Producto(SafeDeleteModel):
    """
    Productos del sistema.
    """
    codigo = models.CharField(
        "SKU del producto", max_length=50, unique=True, null=True, blank=True
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)

    # Usamos DecimalField para precisión monetaria y de stock.
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Campo para atributos flexibles (color, talla, marca, etc.)
    atributos = models.JSONField(
        "Atributos Adicionales", null=True, blank=True, default=dict
    )

    estado = models.CharField(
        max_length=20,
        choices=EstadoProducto.choices(),
        default=EstadoProducto.ACTIVO
    )

    # Relación Many-to-Many a través de un modelo intermedio.
    # Esto nos permite añadir campos extra a la relación (ej. es_principal).
    categorias = models.ManyToManyField(
        Categoria,
        through='ProductoCategoria',
        related_name='productos'
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class ProductoCategoria(SafeDeleteModel):
    """
    Modelo intermedio (tabla pivote) para la relación N-N
    entre Producto y Categoria.
    """
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    # Campos adicionales en la relación
    es_principal = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
        # Un producto no puede tener la misma categoría dos veces.
        unique_together = [['producto', 'categoria']]

    def __str__(self):
        return f"{self.producto.nombre} -> {self.categoria.nombre}"