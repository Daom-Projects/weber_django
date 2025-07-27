# productos/admin.py

from django.contrib import admin
from .models import Categoria, Producto, ProductoCategoria
from archivos.admin import ArchivoInline # Importamos el inline de archivos
from safedelete.admin import SafeDeleteAdmin

# --- Inlines ---
# Este inline nos permitirá añadir/editar/eliminar las categorías de un producto
# directamente desde la página de edición del producto.

class ProductoCategoriaInline(admin.TabularInline):
    """
    Inline para gestionar la relación N-N entre Producto y Categoria.
    Se mostrará en la página de detalle del Producto.
    """
    model = ProductoCategoria
    # 'extra' controla cuántos campos vacíos para añadir nuevas relaciones se muestran.
    extra = 1
    autocomplete_fields = ['categoria']


# --- ModelAdmins ---

@admin.register(Categoria)
class CategoriaAdmin(SafeDeleteAdmin):
    """
    Panel de administración para Categorías.
    """
    list_display = ('nombre', 'categoria_padre', 'estado') + SafeDeleteAdmin.list_display
    search_fields = ('nombre',)
    list_filter = ('estado', 'categoria_padre') + SafeDeleteAdmin.list_filter
    # Habilitamos la búsqueda para el campo de autocompletado en el inline.
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(SafeDeleteAdmin):
    """
    Panel de administración para Productos.
    """
    list_display = ('nombre', 'codigo', 'stock', 'estado') + SafeDeleteAdmin.list_display
    search_fields = ('nombre', 'codigo')
    list_filter = ('estado', 'categorias') + SafeDeleteAdmin.list_filter

    # Aquí conectamos el inline que definimos arriba.
    inlines = [ProductoCategoriaInline, ArchivoInline]

    # Para evitar confusión, excluimos el campo 'categorias' del formulario principal,
    # ya que ahora lo gestionamos a través del inline.
    exclude = ('categorias',)