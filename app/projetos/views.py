from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .services import ProjectService


# View para listar os projetos
def index(request, *args, **kwargs):
    tipo = request.GET.get('tipo', 'semanal')
    tags = request.GET.getlist('tags')
    search = request.GET.get('search', '')
    page = request.GET.get('page', 1)

    # Obtém projetos filtrados através do serviço
    projects = ProjectService.get_filtered_projects(tipo, tags, search)
    print(f"Projetos: {projects}")
    print(f"Total de projetos: {projects.count()}")  # Verifique o total de projetos antes da paginação

    # Paginação
    paginator = Paginator(projects, 10)

    try:
        paginated_projects = paginator.page(page)
        print(f"Na Página {page}, temos os projetos: {paginated_projects.object_list}")
    except PageNotAnInteger:
        print(f"Erro na paginação: {page}\n")
        paginated_projects = paginator.page(1)
    except EmptyPage:
        print(f"Erro na paginação (sem páginas): {page}\n")
        paginated_projects = paginator.page(paginator.num_pages)

    next_page_number = paginated_projects.next_page_number if paginated_projects.has_next() else None

    print(f"Projetos na página: {paginated_projects}")  # Verifique os projetos na página

    return render(request, 'projetos/index.html', {
        'projects': paginated_projects,
        'next_page_number': next_page_number,
    })
