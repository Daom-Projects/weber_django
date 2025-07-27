# usuarios/models.py

from django.db import models
from django.contrib.auth.models import User # Importamos el modelo User de Django
from django.contrib.contenttypes.fields import GenericRelation # Relacion genérica para archivos adjuntos
from safedelete.models import SafeDeleteModel
from core.enums import TipoDocumento, Genero, RolNegocio, EstadoUsuario



class PerfilUsuario(SafeDeleteModel):
    """
    Este modelo extiende el modelo User de Django.
    Contiene toda la información de negocio adicional del usuario.
    """
    # --- LA RELACIÓN CLAVE ---
    # OneToOneField asegura que cada usuario de Django tenga exactamente un perfil.
    # Es la forma recomendada de extender el modelo User.
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    codigo_empleado = models.CharField(max_length=20, unique=True, null=True, blank=True)
    tipo_documento = models.CharField(max_length=5, choices=TipoDocumento.choices())
    documento = models.CharField(max_length=15, unique=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    email_corporativo = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    direccion = models.CharField(max_length=300, null=True, blank=True)

    municipio = models.ForeignKey(
        'ubicaciones.Municipio',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(
        max_length=20,
        choices=Genero.choices(),
        default=Genero.NO_ESPECIFICA
    )
    rol_negocio = models.CharField(max_length=20, choices=RolNegocio.choices())

    # Campos específicos para empleados
    fecha_contratacion = models.DateField(null=True, blank=True)
    fecha_terminacion = models.DateField(null=True, blank=True)
    salario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    sucursal = models.ForeignKey(
        'organizacion.Sucursal',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=20,
        choices=EstadoUsuario.choices(),
        default=EstadoUsuario.ACTIVO
    )

    # --- RELACIÓN INVERSA GENÉRICA ---
    archivos = GenericRelation('archivos.Archivo')

    # --- Propiedad para acceso fácil ---
    @property
    def foto_perfil(self):
        # Devuelve el primer archivo de tipo imagen asociado, o None.
        return self.archivos.filter(tipo_archivo='imagen').first()

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering = ['nombres', 'apellidos']

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.documento})"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"