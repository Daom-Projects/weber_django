# productos/views.py
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import Producto
from .forms import ProductoForm

# --- Importaciones para DRF ---
from rest_framework import viewsets # Importamos viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly # Importar
from .serializers import ProductoSerializer

class ProductoListView(ListView):
    """
    Vista para mostrar una lista de todos los productos.
    """
    # 1. El modelo con el que vamos a trabajar.
    model = Producto

    # 2. El nombre de la variable de contexto en la plantilla.
    # Por defecto es 'object_list', pero 'productos' es más intuitivo.
    context_object_name = 'productos'

    # 3. Sobrescribimos get_queryset para manejar la búsqueda
    def get_queryset(self):
        queryset = super().get_queryset()
        # Obtenemos el parámetro 'q' de la URL (?q=...)
        query = self.request.GET.get('q')
        if query:
            # Filtramos por nombre O por código que contenga la búsqueda
            queryset = queryset.filter(
                Q(nombre__icontains=query) | Q(codigo__icontains=query) | Q(descripcion__icontains=query)
            )
        return queryset

    # 4. Sobrescribimos get_template_names para elegir la plantilla correcta
    def get_template_names(self):
        # HTMX añade un encabezado 'HX-Request' a sus peticiones
        if self.request.headers.get('HX-Request'):
            # Si es una petición de HTMX, devolvemos solo la tabla
            return ['productos/partials/tabla_productos.html']
        # Si es una carga de página normal, devolvemos la página completa
        return ['productos/lista_productos.html']

class ProductoDetailView(DetailView):
    """
    Vista para mostrar los detalles de un único producto.
    """
    model = Producto
    template_name = 'productos/detalle_producto.html'

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    # success_url se usará solo para peticiones no-HTMX
    success_url = reverse_lazy('productos:lista')

    def get_template_names(self):
        if self.request.headers.get('HX-Request'):
            return ['productos/partials/producto_form_modal.html']
        return ['productos/producto_form.html']

    def form_valid(self, form):
        # Si la petición es de HTMX, devolvemos una respuesta diferente
        if self.request.headers.get('HX-Request'):
            # Guardamos el objeto
            self.object = form.save()
            # Obtenemos todos los productos para actualizar la tabla
            context = {'productos': Producto.objects.all()}
            # Renderizamos la tabla parcial con la lista de productos actualizada
            response = render(self.request, 'productos/partials/tabla_productos.html', context)
            # Añadimos un encabezado especial para que HTMX sepa que debe actualizar la tabla
            # y también que debe disparar un evento para cerrar el modal.
            response['HX-Retarget'] = '#product-table-container'
            response['HX-Trigger'] = 'close-modal' # Disparamos un evento personalizado
            return response

        # Si no es HTMX, comportamiento normal
        return super().form_valid(form)

class ProductoUpdateView(UpdateView):
    """
    Vista para editar un producto existente.
    """
    model = Producto
    form_class = ProductoForm
    # Reutilizamos la misma plantilla del formulario de creación.
    template_name = 'productos/producto_form.html'

    # Después de editar con éxito, redirigimos a la página de detalle de ese mismo producto.
    def get_success_url(self):
        return reverse_lazy('productos:detalle', kwargs={'pk': self.object.pk})

class ProductoDeleteView(DeleteView):
    """
    Vista para eliminar (soft delete) un producto.
    """
    model = Producto
    # La plantilla que mostrará el mensaje de confirmación.
    template_name = 'productos/producto_confirm_delete.html'

    # Después de eliminar, volvemos a la lista de productos.
    success_url = reverse_lazy('productos:lista')

# --- VISTAS DE API ---
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    # --- AÑADIR ESTA LÍNEA ---
    # Sobrescribimos la política de permisos por defecto solo para esta vista.
    permission_classes = [IsAuthenticatedOrReadOnly]