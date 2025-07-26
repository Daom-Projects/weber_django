# ubicaciones/models.py
from django.db import models
from safedelete.models import SafeDeleteModel
from core.enums import EstadoGeneral, Region

class Departamento(SafeDeleteModel):
    """
    Modelo que representa los Departamentos de Colombia.
    Usa Soft Delete y un Enum reutilizables
    """

    nombre = models.CharField(
        "Nombre del departamento", max_length=200, unique=True
    )
    codigo_dane = models.PositiveIntegerField(
        "Código DANE del departamento", unique=True
    )
    region = models.CharField(
        max_length=50,
        choices=Region.choices(),
        default=Region.CENTRO_ORIENTE
    )

    estado = models.CharField(
        max_length=10,
        choices=EstadoGeneral.choices(),
        default=EstadoGeneral.ACTIVO
    )

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Municipio(SafeDeleteModel):
    """
    Modelo que representa los Municipios de Colombia.
    """
    departamento = models.ForeignKey(
        Departamento, on_delete=models.CASCADE, related_name='municipios'
    )
    nombre = models.CharField("Nombre del municipio", max_length=400)
    codigo_dane = models.PositiveIntegerField("Código DANE del municipio", unique=True)

    # Usando nuestro Enum reutilizable
    estado = models.CharField(
        max_length=10,
        choices=EstadoGeneral.choices(),
        default=EstadoGeneral.ACTIVO
    )

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['departamento', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.departamento.nombre})"