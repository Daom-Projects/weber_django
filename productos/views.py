# productos/views.py
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import Producto
from .forms import ProductoForm

class ProductoListView(ListView):
    """
    Vista para mostrar una lista de todos los productos.
    """
    # 1. El modelo con el que vamos a trabajar.
    model = Producto

    # 2. La plantilla que vamos a renderizar.
    template_name = 'productos/lista_productos.html'

    # 3. El nombre de la variable de contexto en la plantilla.
    # Por defecto es 'object_list', pero 'productos' es más intuitivo.
    context_object_name = 'productos'

class ProductoDetailView(DetailView):
    """
    Vista para mostrar los detalles de un único producto.
    """
    model = Producto
    template_name = 'productos/detalle_producto.html'

class ProductoCreateView(CreateView):
    """
    Vista para crear un nuevo producto.
    """
    model = Producto
    # Le decimos a la vista que use nuestro formulario personalizado.
    form_class = ProductoForm
    # Usaremos la misma plantilla para crear y para actualizar.
    template_name = 'productos/producto_form.html'

    # URL a la que se redirigirá al usuario después de crear el producto con éxito.
    # reverse_lazy se usa aquí porque las URLs no se cargan hasta que Django las necesita.
    success_url = reverse_lazy('productos:lista')

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