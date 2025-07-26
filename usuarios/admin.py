# usuarios/admin.py
from django.contrib import admin
from .models import PerfilUsuario

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """
    Panel de administración placeholder para Perfiles de Usuario.
    Resuelve la dependencia de 'autocomplete_fields' de otras apps.
    Lo personalizaremos en detalle más adelante.
    """
    # --- ¡ESTA LÍNEA ES LA CLAVE! ---
    # Le decimos a Django que cuando otra app use autocompletado para este modelo,
    # debe buscar en el campo 'nombres'.
    search_fields = ['nombres']

    # También es buena práctica añadir un list_display básico.
    list_display = ['nombres']