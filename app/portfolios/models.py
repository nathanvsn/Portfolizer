from django.db import models
from custom_auth.models import User
from taggit.managers import TaggableManager
from django.db import transaction
from django.utils import timezone
from datetime import timedelta

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=255)
    description = models.TextField()
    markdown_content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Portfolio de {self.user.username}"
    
    @property
    def is_pro(self):
        return self.user.profile.user_type == 'pro'

    @property
    def is_ultra(self):
        return self.user.profile.user_type == 'ultra'
    
    @property
    def can_create_more_projects(self):
        user_type = self.user.profile.user_type
        if user_type == 'free':
            return self.projects.count() < 5
        elif user_type == 'pro':
            return self.projects.count() < 15
        else:
            return True

class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=400, blank=True, null=True)
    img = models.ImageField(upload_to='project_images/', blank=True, null=True)
    votes = models.IntegerField(default=0)
    tags =TaggableManager(blank = True)
    markdown_content = models.TextField(blank=True)
    html_content = models.TextField(blank=True)
    css_content = models.TextField(blank=True)
    js_content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Projeto {self.name} do portfólio de {self.portfolio.user.username}"

    @property
    def can_upload_more_images(self):
        user_type = self.portfolio.user.profile.user_type
        if user_type == 'free':
            return self.resources.count() < 3
        elif user_type == 'pro':
            return self.resources.count() < 10
        else:
            return True  # Sem limite para Ultra
    
    def total_storage_used(self):
        return sum(resource.file_size for resource in self.resources.all())

    @property
    def can_upload_more_resources(self):
        user_type = self.portfolio.user.profile.user_type
        total_used = self.total_storage_used()
        
        if user_type == 'ultra' and total_used < 1000 * 1024 * 1024:
            return True
        elif user_type == 'pro' or user_type == 'free':
            return False
        return False
    
    def user_has_voted(self, user):
        """Verifica se o usuário já votou neste projeto."""
        return self.user_votes.filter(user=user).exists()
    
    def add_vote(self):
        with transaction.atomic():
            self.votes += 1
            self.save()

    def remove_vote(self):
        with transaction.atomic():
            if self.votes > 0:
                self.votes -= 1
            self.save()

    # Pegar os projetos pelas tags
    def get_projects_by_tags(self, tags):
        return Project.objects.filter(tags__name__in=tags).distinct()
    
def user_directory_path(instance, filename):
    # Define o caminho de upload como: 'user_<id>/<filename>'
    return f'user_{instance.project.portfolio.user.id}/{filename}'


class Resource(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='resources')
    file = models.FileField(upload_to=user_directory_path)  # Usando a função customizada
    file_type = models.CharField(max_length=20)  # Tipo do arquivo (ex: image/png, application/pdf)
    file_size = models.PositiveIntegerField()  # Armazenar o tamanho do arquivo em bytes

    def __str__(self):
        return f"Recurso {self.file.name} do projeto {self.project.name}"

    @property
    def total_storage_used(self):
        return sum(resource.file_size for resource in self.project.resources.all())

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="user_votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
        
    @classmethod  # Adicionei o decorator de classe
    def filtro_projetos_data(cls, period):
        days = {'week': 7, 'month': 30}
        return Project.objects.filter(created_at__gte=timezone.now() - timedelta(days=days.get(period, 7))).order_by('-votes')

