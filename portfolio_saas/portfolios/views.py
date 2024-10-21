from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Project
from .forms import ProjectForm, ResourceForm

from custom_auth.models import User

@login_required
def user_portfolio(request, username):
    user = get_object_or_404(User, username=username)
    portfolio = user.portfolio
    projects = portfolio.projects.all()

    # Lógica para salvar o conteúdo markdown
    if request.method == 'POST' and request.user == user:
        markdown_content = request.POST.get('markdown_content')
        portfolio.markdown_content = markdown_content
        portfolio.save()
        return redirect('user_portfolio', username=username)

    context = {
        'portfolio': portfolio,
        'projects': projects,
    }

    return render(request, 'portfolio/user_portfolio.html', context)

@login_required
def project_detail(request, username, project_name):
    portfolio = get_object_or_404(Portfolio, user__username=username)
    project = get_object_or_404(Project, portfolio=portfolio, name=project_name)

    if portfolio.is_ultra:  # Ultra pode ter HTML/CSS/JS
        template = 'portfolio/ultra_project_detail.html'
    else:
        template = 'portfolio/project_detail.html'

    context = {
        'project': project,
    }
    return render(request, template, context)


@login_required
def create_project(request, username):
    portfolio = get_object_or_404(Portfolio, user__username=username)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.portfolio = portfolio
            project.save()
            return redirect('user_portfolio', username=username)
    else:
        form = ProjectForm()
    
    return render(request, 'portfolio/create_project.html', {'form': form})

@login_required
def upload_resource(request, username, project_name):
    project = get_object_or_404(Project, portfolio__user__username=username, name=project_name)
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.project = project
            resource.file_size = resource.file.size
            resource.save()
            return redirect('project_detail', username=username, project_name=project_name)
    else:
        form = ResourceForm()
    
    return render(request, 'portfolio/upload_resource.html', {'form': form})