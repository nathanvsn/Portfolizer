from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inclui as URLs do app `portfolio` para a navegação dos usuários
    path('', include('portfolios.urls')),  # Assumindo que o app se chama 'portfolio'
]
