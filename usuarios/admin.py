# usuarios/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Importamos format_html para renderizar HTML de forma segura en el admin
from django.utils.html import format_html
from .models import PerfilUsuario
from archivos.admin import ArchivoInline

# Primero, definimos el inline para el perfil.
# StackedInline se ve mejor que TabularInline cuando hay muchos campos.
class PerfilUsuarioInline(admin.StackedInline):
    """
    Inline para mostrar el PerfilUsuario en la página de edición del User.
    """
    model = PerfilUsuario
    # 'can_delete=False' evita que se pueda borrar el perfil desde el admin del usuario.
    can_delete = False
    verbose_name_plural = 'Perfiles de Usuario'
    # Para campos ForeignKey con muchos registros, el autocompletado es esencial.
    autocomplete_fields = ['municipio', 'sucursal']

    # 1. Definimos los campos de solo lectura
    readonly_fields = ('get_foto_perfil_preview',)

    @admin.display(description='Vista Previa de Foto de Perfil')
    def get_foto_perfil_preview(self, obj):
        # Usamos la propiedad 'foto_perfil' que definimos en el modelo
        foto = obj.foto_perfil
        if foto and hasattr(foto.ruta_archivo, 'url'):
            return format_html('<img src="{}" width="150" height="150" />', foto.ruta_archivo.url)
        return "No hay foto de perfil."


# Ahora definimos un nuevo UserAdmin que incluye nuestro inline.
class CustomUserAdmin(BaseUserAdmin):
    """
    Extendemos el UserAdmin base para incluir el perfil en la misma página.
    """
    inlines = (PerfilUsuarioInline,)

    # Opcional: Para mostrar campos del perfil en la lista de usuarios.
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rol_negocio')

    @admin.display(description='Rol de Negocio', ordering='perfil__rol_negocio')
    def get_rol_negocio(self, obj):
        # Es importante manejar el caso de que un usuario aún no tenga perfil.
        if hasattr(obj, 'perfil'):
            return obj.perfil.rol_negocio
        return 'Sin Perfil'

# Finalmente, des-registramos el UserAdmin base y registramos el nuestro.
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# También podemos registrar PerfilUsuario por sí solo para tener acceso directo (opcional)
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """
    Panel de administración para ver los Perfiles directamente.
    """
    list_display = ('usuario', 'nombre_completo', 'rol_negocio', 'sucursal', 'estado')
    search_fields = ('nombres', 'apellidos', 'documento', 'usuario__username')
    list_filter = ('rol_negocio', 'estado', 'sucursal')
    autocomplete_fields = ['usuario', 'municipio', 'sucursal']

    # Incrustamos el formulario para subir archivos directamente aquí
    inlines = [ArchivoInline]