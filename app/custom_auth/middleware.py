from django.shortcuts import redirect
from django.urls import reverse

class ProfileRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Verifica se o usuário possui um perfil
            has_freelancer_profile = hasattr(request.user, 'freelancer_profile')
            has_client_profile = hasattr(request.user, 'client_profile')
            
            # Se não tiver nenhum perfil, redireciona para a página de escolha
            if not has_freelancer_profile and not has_client_profile:
                if request.path != reverse('users:choose_profile'):
                    return redirect('users:choose_profile')
        
        response = self.get_response(request)
        return response
