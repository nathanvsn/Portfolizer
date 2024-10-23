from django.contrib import admin
from .models import User, UserProfile

# Gerenciar o UserProfile dentro do User 
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline, )
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    # O filtro correto para acessar o campo user_type do UserProfile
    list_filter = ['is_active', 'is_staff', 'profile__user_type']
    # Atualizando os fieldsets para incluir o campo username
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),  # Incluindo o campo username
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('email',)
