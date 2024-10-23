from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('pages.urls')),

    path('portfolio/', include('portfolios.urls')),
    
    path('users/', include('custom_auth.urls')),
]

# Adicione esta linha para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)