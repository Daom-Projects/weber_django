# transacciones/admin.py

from django.contrib import admin
from .models import Transaccion, DetalleTransaccion, Devolucion

class DetalleTransaccionInline(admin.TabularInline):
    """
    Inline para gestionar los detalles (productos) dentro de una transacción.
    """
    model = DetalleTransaccion
    extra = 1 # Muestra un campo vacío para añadir un nuevo detalle.
    autocomplete_fields = ['producto']

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    """
    Panel de administración para Transacciones (Compras/Ventas).
    """
    list_display = ('__str__', 'fecha', 'sucursal', 'empleado', 'tipo_transaccion', 'total', 'estado')
    list_filter = ('tipo_transaccion', 'estado', 'sucursal', 'fecha')
    search_fields = ('numero_factura', 'cliente__nombres', 'proveedor__nombres')
    autocomplete_fields = ['sucursal', 'proveedor', 'cliente', 'empleado']

    # Incrustamos los detalles directamente en el formulario de la transacción.
    inlines = [DetalleTransaccionInline]

    list_per_page = 20

@admin.register(DetalleTransaccion)
class DetalleTransaccionAdmin(admin.ModelAdmin):
    """
    Admin para DetalleTransaccion.
    Se registra principalmente para habilitar el autocompletado en otros admins.
    """
    list_display = ('__str__', 'producto', 'transaccion')
    # Esta es la parte crucial que necesita DevolucionAdmin para su autocompletado
    search_fields = ['producto__nombre', 'transaccion__numero_factura', 'lote']

@admin.register(Devolucion)
class DevolucionAdmin(admin.ModelAdmin):
    """
    Panel de administración para Devoluciones.
    """
    list_display = ('__str__', 'fecha', 'sucursal', 'empleado', 'tipo_devolucion', 'estado')
    list_filter = ('tipo_devolucion', 'estado', 'sucursal', 'fecha')
    search_fields = ('numero', 'detalle_transaccion__transaccion__numero_factura')
    autocomplete_fields = ['sucursal', 'empleado', 'detalle_transaccion']

    list_per_page = 20

# Nota importante: No registramos 'DetalleTransaccion' por sí solo.
# ¿Por qué? Porque no tiene sentido de negocio crear, ver o editar un "detalle"
# sin el contexto de su transacción principal. Su gestión debe ocurrir
# exclusivamente a través del inline en TransaccionAdmin.