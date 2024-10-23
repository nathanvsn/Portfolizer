from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

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
        return self.profile.is_pro  # Acessando o perfil para verificar o tipo de usuário
    
    @property
    def is_ultra(self):
        return self.profile.is_ultra  # Acessando o perfil para verificar o tipo de usuário

    def __str__(self):
        return self.username

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
