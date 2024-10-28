from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),

    path('portfolio/', include('portfolios.urls')),
    path('projetos/', include('projetos.urls')),
    path('users/', include('custom_auth.urls')),
    path('freelancers/', include('freelance.urls')),
]

# Adicione esta linha para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)