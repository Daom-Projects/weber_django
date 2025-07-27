# archivos/models.py

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from safedelete.models import SafeDeleteModel
from core.enums import TipoArchivo
import uuid

class Archivo(SafeDeleteModel):
    """
    Modelo polimórfico para gestionar cualquier tipo de archivo
    y enlazarlo a cualquier otro modelo del sistema.
    """

    # Campos de tu diseño original
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre_original = models.CharField(max_length=255)
    ruta_archivo = models.FileField(upload_to='archivos/%Y/%m/%d/') # Django gestionará la subida
    extension = models.CharField(max_length=10)
    tipo_archivo = models.CharField(
        max_length=20,
        choices=TipoArchivo.choices(),
        default=TipoArchivo.OTRO
    )

    # --- LA MAGIA POLIMÓRFICA ---
    # 1. El tipo de contenido (qué modelo es el padre, ej: Producto, PerfilUsuario)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # 2. El ID del objeto padre (el ID del producto o usuario específico)
    object_id = models.PositiveIntegerField()

    # 3. El campo virtual que combina los dos anteriores para darnos el objeto padre
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"
        # Índices para acelerar las búsquedas polimórficas
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self):
        return self.nombre_original