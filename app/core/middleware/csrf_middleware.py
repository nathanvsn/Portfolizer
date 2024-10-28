from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class DynamicCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        origin = request.META.get('HTTP_ORIGIN')
        if origin and origin.endswith(".portfolizer.com.br"):
            # Modifica o cabeçalho de origem para o domínio principal confiável
            request.META['HTTP_ORIGIN'] = 'https://portfolizer.com.br'
