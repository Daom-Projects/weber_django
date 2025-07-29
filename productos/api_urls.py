# productos/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. Creamos una instancia del router.
router = DefaultRouter()

# 2. Registramos nuestro ViewSet en el router.
#    - El prefijo 'r''' es vacío porque el prefijo ya está en config/urls.py.
#    - Le pasamos la clase ViewSet.
#    - `basename` se usa para generar los nombres de las URLs (ej: 'producto-list').
router.register(r'', views.ProductoViewSet, basename='producto')

# 3. Las URLs de la API ahora son generadas automáticamente por el router.
urlpatterns = router.urls