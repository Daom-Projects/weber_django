# transacciones/models.py

from django.db import models
from safedelete.models import SafeDeleteModel
from core.enums import MetodoPago, EstadoTransaccion, TipoTransaccion, MotivoDevolucion, TipoDevolucion, EstadoDevolucion

class Transaccion(SafeDeleteModel):
    """
    Transacciones base (compras y ventas) por sucursal.
    """
    numero_factura = models.CharField(max_length=80)
    sucursal = models.ForeignKey(
        'organizacion.Sucursal',
        on_delete=models.PROTECT,
        related_name='transacciones'
    )
    # Múltiples FK al mismo modelo, usamos related_name para evitar conflictos.
    proveedor = models.ForeignKey(
        'usuarios.PerfilUsuario',
        on_delete=models.PROTECT,
        related_name='compras_realizadas',
        null=True,
        blank=True
    )
    cliente = models.ForeignKey(
        'usuarios.PerfilUsuario',
        on_delete=models.PROTECT,
        related_name='ventas_recibidas',
        null=True,
        blank=True
    )
    empleado = models.ForeignKey(
        'usuarios.PerfilUsuario',
        on_delete=models.PROTECT,
        related_name='transacciones_registradas'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    valor_base = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=50, choices=MetodoPago.choices())
    estado = models.CharField(max_length=20, choices=EstadoTransaccion.choices(), default=EstadoTransaccion.BORRADOR)
    tipo_transaccion = models.CharField(max_length=10, choices=TipoTransaccion.choices())
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        unique_together = [['sucursal', 'numero_factura', 'tipo_transaccion']]

    def __str__(self):
        return f"{self.get_tipo_transaccion_display()} #{self.numero_factura} - {self.sucursal.nombre}"

class DetalleTransaccion(SafeDeleteModel):
    """
    Detalles de productos dentro de una transacción.
    """
    transaccion = models.ForeignKey(Transaccion, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('productos.Producto', on_delete=models.PROTECT)
    lote = models.CharField(max_length=50, null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    costo_unitario = models.DecimalField(max_digits=15, decimal_places=4)
    precio_venta_calculado = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = "Detalle de Transacción"
        verbose_name_plural = "Detalles de Transacciones"

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.transaccion.numero_factura}"

class Devolucion(SafeDeleteModel):
    """
    Devoluciones de productos, ligadas a un detalle de transacción específico.
    """
    sucursal = models.ForeignKey('organizacion.Sucursal', on_delete=models.PROTECT)
    numero = models.CharField(max_length=50)
    fecha = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=50, choices=MotivoDevolucion.choices())
    # Una devolución está ligada al item específico de la factura original.
    detalle_transaccion = models.ForeignKey(DetalleTransaccion, on_delete=models.PROTECT)
    tipo_devolucion = models.CharField(max_length=10, choices=TipoDevolucion.choices())
    cantidad_devuelta = models.DecimalField(max_digits=10, decimal_places=3)
    monto_devolucion = models.DecimalField(max_digits=15, decimal_places=2)
    estado = models.CharField(max_length=20, choices=EstadoDevolucion.choices(), default=EstadoDevolucion.PENDIENTE)
    observaciones = models.TextField()
    empleado = models.ForeignKey('usuarios.PerfilUsuario', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Devolución"
        verbose_name_plural = "Devoluciones"
        unique_together = [['sucursal', 'numero']]

    def __str__(self):
        return f"Devolución #{self.numero} - {self.sucursal.nombre}"