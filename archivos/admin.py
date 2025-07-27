# archivos/admin.py (versión completa opcional)
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Archivo

class ArchivoInline(GenericTabularInline):
    """
    Inline para gestionar archivos de forma genérica.
    Se podrá incrustar en cualquier ModelAdmin cuyo modelo
    tenga una GenericRelation con Archivo.
    """
    model = Archivo
    extra = 1 # Muestra 1 campo vacío para subir un nuevo archivo.

@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    """
    (Opcional) Un panel de admin para ver TODOS los archivos del sistema.
    Útil para mantenimiento, no para la gestión diaria.
    """
    list_display = ('nombre_original', 'content_object', 'tipo_archivo')
    list_filter = ('tipo_archivo', 'content_type')
    search_fields = ('nombre_original',)