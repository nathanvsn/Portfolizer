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
    
    # Paginação
    paginator = Paginator(projects, 10)

    try:
        paginated_projects = paginator.page(page)
    except PageNotAnInteger:
        paginated_projects = paginator.page(1)
    except EmptyPage:
        paginated_projects = paginator.page(paginator.num_pages)

    next_page_number = paginated_projects.next_page_number if paginated_projects.has_next() else None

    return render(request, 'projetos/index.html', {
        'projects': paginated_projects,
        'next_page_number': next_page_number,
    })
