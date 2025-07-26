# core/enums.py
import enum
from django.db import models

# Opción 1: Un Enum simple y reutilizable para estados comunes.
class EstadoGeneral(str, enum.Enum):
    ACTIVO = 'Activo'
    INACTIVO = 'Inactivo'

    # Este método lo hace compatible con los 'choices' de Django
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

# Opción 2: Un Enum para regiones de Colombia. Cada región tiene propiedades adicionales.
class Region(str, enum.Enum):
    CARIBE = 'Caribe'
    CENTRO_ORIENTE = 'Centro Oriente'
    CENTRO_SUR = 'Centro Sur'
    EJE_CAFETERO = 'Eje Cafetero - Antioquia'
    LLANO = 'Llano'
    PACIFICO = 'Pacífico'

    @property
    def label(self) -> str:
        # En una app real, esto usaría el sistema de internacionalización de Django (gettext)
        return self.value.replace('_', ' ').capitalize()

    @property
    def color(self) -> str:
        return {
            self.CARIBE: 'primary',
            self.CENTRO_ORIENTE: 'info',
            self.CENTRO_SUR: 'success',
            self.EJE_CAFETERO: 'warning',
            self.LLANO: 'danger',
            self.PACIFICO: 'secondary',
        }.get(self)

    @property
    def icon(self) -> str:
        return {
            self.CARIBE: 'heroicon-o-academic-cap',
            self.CENTRO_ORIENTE: 'heroicon-o-book-open',
            self.CENTRO_SUR: 'heroicon-o-user-group',
            self.EJE_CAFETERO: 'heroicon-o-wrench-screwdriver',
            self.LLANO: 'heroicon-o-sun',
            self.PACIFICO: 'heroicon-o-water',
        }.get(self)

    # Para la compatibilidad con 'choices'
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]