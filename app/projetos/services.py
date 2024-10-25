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
        
        # Printar todos os projetos
        print(projects_query)

        # Aplica filtro de votos
        if date_filter:
            projects_query = Vote.filtro_projetos_data(date_filter).distinct()
            print(projects_query)

        # Aplica filtro por tags
        if tags:
            projects_query = projects_query.filter(tags__name__in=tags).distinct()
            print(projects_query)

        # Aplica filtro de busca por nome
        if search:
            projects_query = projects_query.filter(Q(name__icontains=search))
            print(projects_query)

        # Adiciona uma ordenação (por exemplo, por data de criação ou votos)
        return projects_query.order_by('-created_at')  # Altere para a ordem que desejar

