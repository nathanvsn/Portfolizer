from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),             # Rota para a página inicial '/'
    path('about/', views.about, name='about'),     # Rota para a página 'Sobre nós'
    path('privacy/', views.privacy, name='privacy'), # Rota para 'Política de Privacidade'
    path('terms/', views.terms, name='terms'),     # Rota para 'Termos de Serviço'
]
