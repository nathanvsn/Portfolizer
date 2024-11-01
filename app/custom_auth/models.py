from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone



class User(AbstractUser):
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    is_email_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    @property
    def is_pro(self):
        return self.profile.is_pro
    
    @property
    def is_ultra(self):
        return self.profile.is_ultra
    
    @property
    def is_freelancer(self):
        return hasattr(self, 'freelancer_profile')
    
    @property
    def is_client(self):
        return hasattr(self, 'client_profile')

    def __str__(self):
        return self.username
    
    def generate_verification_token(self):
        self.email_verification_token = get_random_string(64)
        self.save()

    # Quando o perfil for criado, criar um perfil de usuário
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, 'profile'):
            UserProfile.objects.create(user=self)

class UserProfile(models.Model):
    FREE = 'free'
    PRO = 'pro'
    ULTRA = 'ultra'
    
    USER_TYPES = [
        (FREE, 'Free User'),
        (PRO, 'Pro User'),
        (ULTRA, 'Ultra User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default=FREE)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    
    # Propriedades para facilitar o acesso ao tipo de usuário
    @property
    def is_free(self):
        return self.user_type == self.FREE

    @property
    def is_pro(self):
        return self.user_type == self.PRO

    @property
    def is_ultra(self):
        return self.user_type == self.ULTRA

class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @staticmethod
    def generate_token(user):
        # Cria um novo token de verificação para o usuário e define o tempo de expiração
        token = get_random_string(64)
        expires_at = timezone.now() + timedelta(hours=24)  # Expira em 24 horas
        return EmailVerificationToken.objects.create(user=user, token=token, expires_at=expires_at)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Email verification token for {self.user.username}"