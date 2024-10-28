from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Página de configurações
    path('settings/', views.settings, name='settings'),

    # Página de logout, usando a view built-in do Django
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('login/', auth_views.LoginView.as_view(template_name='custom_auth/login.html'), name='login'),
    path('register/', views.register, name='register'),
    
    path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('choose_profile/', views.choose_profile, name='choose_profile'),
    path('setup_profile/', views.setup_profile, name='setup_profile'),
]
