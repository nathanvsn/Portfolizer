# Rotas com subdomains

from django.urls import path
from . import views

urlpatterns = [
    path('', views.ultra_subdomain_view, name='ultra_user_portfolio'),  # Página inicial do subdomínio
]