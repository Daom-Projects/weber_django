# productos/urls.py
from django.urls import path
from . import views

# app_name nos ayuda a organizar las URLs y a referenciarlas fácilmente en las plantillas.
app_name = 'productos'

urlpatterns = [
    # La ruta vacía ('') corresponde a la raíz /productos/
    # Le asignamos la vista ProductoListView y un nombre para referenciarla.
    path('', views.ProductoListView.as_view(), name='lista'),

    # <int:pk> es un "convertidor de ruta". Captura un entero de la URL
    # y lo pasa a la vista como un argumento llamado 'pk' (primary key).
    path('<int:pk>/', views.ProductoDetailView.as_view(), name='detalle'),
    # Ruta para crear un nuevo producto.
    path('crear/', views.ProductoCreateView.as_view(), name='crear'),
    # Ruta para editar un producto existente.
    path('<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='editar'),
    # Ruta para eliminar un producto existente.
    path('<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='eliminar'),
]