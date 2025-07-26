# organizacion/models.py

from django.db import models
from safedelete.models import SafeDeleteModel
from core.enums import EstadoGeneral, TipoEmpresa, TipoSucursal

class Empresa(SafeDeleteModel):
    """
    Modelo para las empresas del sistema.
    """
    nombre = models.CharField("Razón social completa", max_length=150)
    # Usamos PositiveBigIntegerField para NITs largos, que no caben en un Integer normal.
    nit = models.PositiveBigIntegerField("NIT sin puntos ni DV", unique=True)
    email = models.EmailField("Email corporativo", max_length=100, unique=True, null=True, blank=True)

    tipo_empresa = models.CharField(
        max_length=50,
        choices=TipoEmpresa.choices(),
        default=TipoEmpresa.SAS
    )
    estado = models.CharField(
        max_length=10,
        choices=EstadoGeneral.choices(),
        default=EstadoGeneral.ACTIVO
    )
    metadatos = models.JSONField("Información adicional", null=True, blank=True, default=dict)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Sucursal(SafeDeleteModel):
    """
    Modelo para las sucursales o sedes de una empresa.
    """
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name='sucursales')
    nombre = models.CharField(max_length=100)

    # --- MANEJO DE DEPENDENCIA CIRCULAR ---
    # El modelo PerfilUsuario aún no ha sido definido. Para evitar errores de importación,
    # Django nos permite usar una 'string' con el formato 'app_name.ModelName'.
    # Esto se conoce como una "referencia tardía" o "lazy relationship".
    # Cuando Django construya todos los modelos, resolverá esta relación.
    administrador = models.ForeignKey(
        'usuarios.PerfilUsuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sucursales_administradas'
    )

    direccion = models.CharField(max_length=300)
    # Relación con un modelo ya definido en otra app
    municipio = models.ForeignKey('ubicaciones.Municipio', on_delete=models.PROTECT)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)

    tipo = models.CharField(
        max_length=50,
        choices=TipoSucursal.choices(),
        default=TipoSucursal.PRINCIPAL
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoGeneral.choices(), # Asumiendo que Mantenimiento es un estado gestionado de otra forma
        default=EstadoGeneral.ACTIVO
    )
    configuracion = models.JSONField(
        "Configuraciones específicas", null=True, blank=True, default=dict
    )

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ['empresa', 'nombre']
        unique_together = [['empresa', 'nombre']]

    def __str__(self):
        return f"{self.nombre} ({self.empresa.nombre})"