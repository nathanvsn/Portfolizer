# middleware.py
from django.conf import settings
from django.shortcuts import redirect
from django.http import Http404
from custom_auth.models import User
from publicsuffix2 import get_sld

# Função utilitária para extrair o subdomínio
def get_subdomain_from_request(request):
    full_host = request.get_host()
    sld = get_sld(full_host)  # Obter o domínio de segundo nível
    domain_parts = full_host.split('.')
    sld_parts = sld.split('.')

    # Identificar as partes do subdomínio removendo as partes do domínio principal
    subdomain_parts = domain_parts[:-(len(sld_parts))]

    # Retornar o domínio principal e as partes do subdomínio
    return sld, subdomain_parts

class SubdomainRoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Validar o host antes de prosseguir
        if request.get_host() not in settings.ALLOWED_HOSTS:
            raise Http404("Host não permitido.")

        # Captura o subdomínio
        sld, subdomain_parts = get_subdomain_from_request(request)
        if len(subdomain_parts) > 0:  # Exemplo: ultra.localhost.com
            request.is_subdomain = True
            request.subdomain = subdomain_parts[0]
        else:
            request.is_subdomain = False
            request.subdomain = None

        response = self.get_response(request)
        return response

class SubdomainRouterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Checa se o subdomínio está presente
        if getattr(request, 'is_subdomain', False):
            # Adiciona as rotas do subdomínio, sem sobrescrever as rotas principais
            print('Subdomínio detectado')
            request.urlconf = 'portfolios.ultra.urls'  # Adiciona as rotas específicas do subdomínio
        else:
            # Mantém o conjunto completo de rotas do domínio principal
            print('Domínio principal detectado')
            request.urlconf = settings.ROOT_URLCONF  # Usar as rotas normais, como 'core.urls'

        response = self.get_response(request)
        return response

class SubdomainSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Validar o host antes de prosseguir
        if request.get_host() not in settings.ALLOWED_HOSTS:
            raise Http404("Host não permitido.")

        # Captura o subdomínio
        sld, subdomain_parts = get_subdomain_from_request(request)
        if len(subdomain_parts) > 0:
            # Verificar se o usuário existe
            try:
                user = User.objects.get(username=subdomain_parts[-1])
            except User.DoesNotExist:
                raise Http404("Usuário não encontrado.")

            # Verificar se o usuário realmente é "Ultra"
            if user.profile.user_type != 'ultra':
                print('Usuário não é Ultra')

                # Montar a URL sem o subdomínio
                scheme = request.scheme  # Obter o esquema (http ou https)
                url = f"{scheme}://{sld}/portfolio/{user.username}/"

                # Redirecionar para a URL padrão (sem subdomínio)
                return redirect(url)

        print('Subdomínio verificado com sucesso')

        # Continuar a requisição normalmente
        response = self.get_response(request)
        return response
