# usuarios/models.py
from django.db import models
from safedelete.models import SafeDeleteModel

class PerfilUsuario(SafeDeleteModel):
    """
    Modelo placeholder para Perfiles de Usuario.
    Define la estructura mínima para resolver las dependencias de otras apps.
    Lo completaremos en detalle en el siguiente módulo.
    """
    # Añadimos un campo simple para que el modelo sea válido y Django lo detecte.
    # Este campo puede ser temporal o parte del modelo final.
    nombres = models.CharField(
        "Nombres completos",
        max_length=80,
        default="Usuario Placeholder"
    )

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return self.nombres