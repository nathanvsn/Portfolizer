from django.db.models import Q
from portfolios.models import Project, Vote

# Camada de serviço para lidar com a lógica de acesso aos dados
class ProjectService:
    @staticmethod
    def get_filtered_projects(tipo, tags, search):
        # Define o filtro de tempo
        if tipo == 'mensal':
            date_filter = 'month'
        elif tipo == 'todos':
            date_filter = None
        else:
            date_filter = 'week'
        
        # Inicializa a consulta
        projects_query = Project.objects.all()

        # Aplica filtro de votos
        if date_filter:
            projects_query = Vote.filtro_projetos_data(date_filter).distinct()

        # Aplica filtro por tags
        if tags:
            projects_query = projects_query.filter(tags__name__in=tags).distinct()

        # Aplica filtro de busca por nome ou descrição
        if search:
            projects_query = projects_query.filter(Q(name__icontains=search) | Q(description__icontains=search)).distinct()
            
        # Ordenação por votos
        return projects_query.order_by('-votes')
