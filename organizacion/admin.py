# organizacion/admin.py

from django.contrib import admin
from .models import Empresa, Sucursal

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    """
    Panel de administración para Empresas.
    """
    list_display = ('nombre', 'nit', 'tipo_empresa', 'estado')
    search_fields = ('nombre', 'nit')
    list_filter = ('tipo_empresa', 'estado')
    list_per_page = 20

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    """
    Panel de administración para Sucursales.
    """
    list_display = ('nombre', 'empresa', 'municipio', 'estado', 'tipo')
    search_fields = ('nombre', 'email', 'empresa__nombre')
    list_filter = ('estado', 'tipo', 'empresa')

    # --- Campos de Autocompletado ---
    # Esto es crucial para un buen rendimiento y experiencia de usuario
    # cuando tenemos muchos municipios o usuarios.
    autocomplete_fields = ['municipio', 'administrador']

    list_per_page = 20
    ordering = ('empresa__nombre', 'nombre')