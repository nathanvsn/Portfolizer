from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import (CustomLoginForm, CustomUserCreationForm, PersonalDataForm, SocialMediaForm,
                    FreelancerTagForm)
from .models import EmailVerificationToken
from freelance.models import Freelancer, Client
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('pages:home')  # Redireciona após login bem-sucedido
        else:
            messages.error(request, 'Erro ao fazer login. Verifique suas credenciais.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'custom_auth/login.html', {'form': form})


@login_required
def settings(request):
    if request.method == 'POST':
        personal_form = PersonalDataForm(request.POST, request.FILES, instance=request.user)
        social_form = SocialMediaForm(request.POST, instance=request.user)
        
        if personal_form.is_valid() and social_form.is_valid():
            personal_form.save()
            social_form.save()
            messages.success(request, 'As suas configurações foram atualizadas com sucesso.')
            return redirect('users:settings')
        else:
            messages.error(request, 'Ocorreu um erro ao salvar as suas configurações.')
    else:
        personal_form = PersonalDataForm(instance=request.user)
        social_form = SocialMediaForm(instance=request.user)
    
    return render(request, 'custom_auth/settings.html', {
        'personal_form': personal_form,
        'social_form': social_form,
    })
    
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('pages:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'custom_auth/register.html', {'form': form})


def verify_email(request, token):
    try:
        verification_token = EmailVerificationToken.objects.get(token=token)
        if verification_token.is_expired():
            messages.error(request, "O token de verificação expirou.")
            return redirect('login')
        user = verification_token.user
        user.is_email_verified = True
        user.save()
        verification_token.delete()  # Remove o token após o uso
        messages.success(request, "E-mail verificado com sucesso!")
        return redirect('users:login')
    except EmailVerificationToken.DoesNotExist:
        return HttpResponse("Token inválido ou já utilizado.", status=400)

@login_required
def choose_profile(request):
    if request.method == 'POST':
        profile_types = request.POST.getlist('profile_type')
        # Verificar se o usuário já possui um perfil
        if Freelancer.objects.filter(user=request.user).exists() or Client.objects.filter(user=request.user).exists():
            messages.error(request, "Você já possui um perfil cadastrado.")
            return redirect('users:setup_profile')
        
        if 'freelancer' in profile_types:
            # Criar perfil de Freelancer
            Freelancer.objects.create(user=request.user)
        if 'client' in profile_types:
            # Criar perfil de Cliente
            Client.objects.create(user=request.user)
        return redirect('users:setup_profile')
    return render(request, 'custom_auth/profile_settings/choose_profile.html')

@login_required
def setup_profile(request):
    user = request.user
    personal_data_form = PersonalDataForm(instance=user)
    freelancer_tag_form = None

    # Se o perfil for Freelancer, adiciona o formulário de tags
    if user.is_freelancer:
        freelancer_tag_form = FreelancerTagForm(instance=user.freelancer_profile)

    if request.method == 'POST':
        personal_data_form = PersonalDataForm(request.POST, request.FILES, instance=user)
        
        if user.is_freelancer:
            freelancer_tag_form = FreelancerTagForm(request.POST, instance=user.freelancer_profile)
        
        if personal_data_form.is_valid() and (not user.is_freelancer or freelancer_tag_form.is_valid()):
            personal_data_form.save()
            
            if user.is_freelancer:
                freelancer_tag_form.save()
            
            return redirect('pages:home')  # Redireciona após salvar o perfil

    return render(request, 'custom_auth/profile_settings/setup_profile.html', {
        'personal_data_form': personal_data_form,
        'freelancer_tag_form': freelancer_tag_form,
        'profile_type': 'freelancer' if user.is_freelancer else 'client'
    })
