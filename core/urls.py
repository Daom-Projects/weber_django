# core/urls.py
from django.urls import path
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    # Esta URL servirá el esqueleto HTML de nuestro frontend.
    path('frontend/', TemplateView.as_view(template_name='core/frontend.html'), name='frontend'),
]