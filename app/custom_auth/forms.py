from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User
from freelance.models import Freelancer, Client

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nome de Usuário',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome de usuário'}),
        required=True
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Nome de usuário ou senha incorretos. Por favor, tente novamente.")
        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User 
        fields = ('username', 'email')
        
# Formulário para dados pessoais
class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'profile_picture']  # Campos para dados pessoais
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulário para redes sociais
class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['website', 'github', 'twitter', 'linkedin']  # Campos para redes sociais
        widgets = {
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
        }

# Formulário para tags (somente para freelancers)
class FreelancerTagForm(forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ['tags']
        widgets = {
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adicionar tags'}),
        }