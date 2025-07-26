# ubicaciones/admin.py
from django.contrib import admin
from .models import Departamento, Municipio
from core.enums import EstadoGeneral # Importamos nuestro enum

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    """
    Personalización del panel de administración para Departamentos.
    """
    # Columnas a mostrar en la lista
    list_display = ('nombre', 'codigo_dane', 'region', 'estado')

    # Campos por los que se puede buscar
    search_fields = ('nombre', 'codigo_dane')

    # Filtros que aparecen en la barra lateral derecha
    list_filter = ('region', 'estado')

    # Paginación: cuántos items por página
    list_per_page = 20

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    """
    Personalización del panel de administración para Municipios.
    """
    list_display = ('nombre', 'get_departamento_nombre', 'codigo_dane', 'estado')
    search_fields = ('nombre', 'codigo_dane')
    list_filter = ('departamento', 'estado')
    list_per_page = 20

    # Para ordenar por campos de modelos relacionados, usamos la notación __
    ordering = ('departamento__nombre', 'nombre')

    # Para mostrar campos de relaciones ForeignKey en list_display
    @admin.display(description='Departamento', ordering='departamento__nombre')
    def get_departamento_nombre(self, obj):
        return obj.departamento.nombre

    # Acción personalizada para activar registros en lote
    @admin.action(description="Marcar seleccionados como Activo")
    def hacer_activos(self, request, queryset):
        queryset.update(estado=EstadoGeneral.ACTIVO)

    # Acción personalizada para inactivar registros en lote
    @admin.action(description="Marcar seleccionados como Inactivo")
    def hacer_inactivos(self, request, queryset):
        queryset.update(estado=EstadoGeneral.INACTIVO)

    # Hacemos que las acciones estén disponibles en el admin
    actions = ['hacer_activos', 'hacer_inactivos']