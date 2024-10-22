from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import CustomLoginForm, CustomUserCreationForm, PersonalDataForm, SocialMediaForm

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
