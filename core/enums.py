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

class EstadoProducto(str, enum.Enum):
    ACTIVO = 'Activo'
    INACTIVO = 'Inactivo'
    DESCONTINUADO = 'Descontinuado'
    AGOTADO = 'Agotado'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').capitalize()) for key in cls]

class TipoEmpresa(str, enum.Enum):
    PERSONA_NATURAL = 'Persona Natural'
    SAS = 'SAS'
    LTDA = 'LTDA'
    SA = 'SA'
    COOPERATIVA = 'Cooperativa'
    FUNDACION = 'Fundación'
    OTRO = 'Otro'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').capitalize()) for key in cls]

class TipoSucursal(str, enum.Enum):
    PRINCIPAL = 'Principal'
    SUBSEDE = 'Subsede'
    PUNTO_DE_VENTA = 'Punto de Venta'
    BODEGA = 'Bodega'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').capitalize()) for key in cls]

class TipoDocumento(str, enum.Enum):
    CC = 'Cédula de Ciudadanía'
    CE = 'Cédula de Extranjería'
    TI = 'Tarjeta de Identidad'
    RC = 'Registro Civil'
    PAS = 'Pasaporte'
    NIT = 'NIT'
    PPT = 'Permiso por Protección Temporal'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

class Genero(str, enum.Enum):
    MASCULINO = 'Masculino'
    FEMENINO = 'Femenino'
    OTRO = 'Otro'
    NO_ESPECIFICA = 'No especifica'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').capitalize()) for key in cls]

class RolNegocio(str, enum.Enum):
    SUPERADMIN = 'SuperAdmin'
    ADMINISTRADOR = 'Administrador'
    EMPLEADO = 'Empleado'
    CLIENTE = 'Cliente'
    PROVEEDOR = 'Proveedor'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]

class EstadoUsuario(str, enum.Enum):
    ACTIVO = 'Activo'
    INACTIVO = 'Inactivo'
    SUSPENDIDO = 'Suspendido'
    BLOQUEADO = 'Bloqueado'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]

class MetodoPago(str, enum.Enum):
    EFECTIVO = 'Efectivo'
    TARJETA_DEBITO = 'Tarjeta Debito'
    TARJETA_CREDITO = 'Tarjeta Credito'
    TRANSFERENCIA = 'Transferencia'
    CREDITO = 'Credito'
    MIXTO = 'Mixto'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').capitalize()) for key in cls]

class EstadoTransaccion(str, enum.Enum):
    BORRADOR = 'Borrador'
    EN_PROCESO = 'En_Proceso'
    FINALIZADA = 'Finalizada'
    CANCELADA = 'Cancelada'
    ANULADA = 'Anulada'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').capitalize()) for key in cls]

class TipoTransaccion(str, enum.Enum):
    VENTA = 'Venta'
    COMPRA = 'Compra'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]

class MotivoDevolucion(str, enum.Enum):
    PRODUCTO_DEFECTUOSO = 'Producto Defectuoso'
    ERROR_CANTIDAD = 'Error Cantidad'
    ERROR_PRODUCTO = 'Error Producto'
    CLIENTE_NO_SATISFECHO = 'Cliente No Satisfecho'
    VENCIMIENTO = 'Vencimiento'
    OTRO = 'Otro'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ').capitalize()) for key in cls]

class TipoDevolucion(str, enum.Enum):
    VENTA = 'Venta'
    COMPRA = 'Compra'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]

class EstadoDevolucion(str, enum.Enum):
    PENDIENTE = 'Pendiente'
    PROCESADA = 'Procesada'
    CANCELADA = 'Cancelada'
    RECHAZADA = 'Rechazada'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]

class TipoArchivo(str, enum.Enum):
    IMAGEN = 'imagen'
    DOCUMENTO = 'documento'
    VIDEO = 'video'
    AUDIO = 'audio'
    OTRO = 'otro'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.capitalize()) for key in cls]