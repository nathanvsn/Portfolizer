from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Portfolio, Project, Resource, Vote
from .forms import ProjectForm, ResourceUploadForm
from django.contrib import messages
from django.http import JsonResponse


from custom_auth.models import User

def user_portfolio(request, username):
    user = get_object_or_404(User, username=username)
    portfolio = user.portfolio
    projects = portfolio.projects.all()

    # Verificar se o usuário logado já votou em cada projeto
    for project in projects:
        project.user_has_voted = project.user_has_voted(request.user) if request.user.is_authenticated else False

    # Lógica para salvar o conteúdo markdown
    if request.method == 'POST' and request.user == user:
        markdown_content = request.POST.get('markdown_content')
        portfolio.markdown_content = markdown_content
        portfolio.save()
        return redirect('portfolio:user_portfolio', username=username)

    context = {
        'portfolio': portfolio,
        'projects': projects,
    }

    return render(request, 'portfolios/portfolio/user_portfolio.html', context)

def project_detail(request, username, project_name):
    portfolio = get_object_or_404(Portfolio, user__username=username)
    project = get_object_or_404(Project, portfolio=portfolio, name=project_name)

    if portfolio.is_ultra:  # Ultra pode ter HTML/CSS/JS
        template = 'portfolios/portfolio/ultra_project_detail.html'
    else:
        template = 'portfolios/portfolio/project_detail.html'
        
    # Verifica se o usuário já votou no projeto
    user_has_voted = False
    if request.user.is_authenticated:
        user_has_voted = Vote.objects.filter(user=request.user, project=project).exists()


    context = {
        'project': project,
        'user_has_voted': user_has_voted,
    }
    return render(request, template, context)

def project_detail_ajax(request, username, project_name):
    # Busca o usuário pelo nome de usuário
    user = get_object_or_404(User, username=username)
    
    # Busca o projeto associado ao usuário e com o nome fornecido
    project = get_object_or_404(Project, portfolio__user=user, name=project_name)
    
    # Dados que serão retornados para o AJAX
    data = {
        'name': project.name,
        'markdown_content': project.markdown_content,
        'img_url': project.img.url if project.img else None,
    }
    
    return JsonResponse(data)

@login_required
def create_project(request, username):
    portfolio = get_object_or_404(Portfolio, user__username=username)
    
    # Verificar se o usuário pode criar mais projetos
    can_create_more_projects = portfolio.can_create_more_projects
    
    if request.method == 'POST':
        # Se o limite de projetos foi atingido, bloquear a criação
        if not can_create_more_projects:
            messages.error(request, 'Você atingiu o limite de projetos para o seu tipo de conta.')
            return JsonResponse({'error': 'Limite de projetos atingido.'})

        # Processar o formulário de criação de projeto
        project_form = ProjectForm(request.POST, request.FILES, user=request.user)
        
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.portfolio = portfolio
            project.save()
            
            # Processar as imagens opcionais (upload)
            for key in request.FILES:
                if key.startswith('project_images_'):  # Processa imagens com nome dinâmico
                    image = request.FILES[key]
                    if not project.can_upload_more_images:
                        messages.error(request, f'Você atingiu o limite de uploads de imagens para o projeto.')
                        return redirect('portfolio:create_project', username=username)
                    
                    resource = Resource(
                        project=project,
                        file=image,
                        file_type=image.content_type,
                        file_size=image.size
                    )
                    resource.save()
            
            messages.success(request, 'Projeto criado com sucesso!')
            return redirect('portfolio:user_portfolio', username=username)
        else:
            messages.error(request, 'Erro ao criar projeto. Verifique os dados e tente novamente.')
    
    else:
        # Exibir o formulário normalmente
        project_form = ProjectForm(user=request.user)

    return render(request, 'portfolios/portfolio/create_project.html', {
        'project_form': project_form,
        'can_create_more_projects': can_create_more_projects,  # Passa essa variável para o template
    })


@login_required()
def vote_project(request, username, project_name):
    project = get_object_or_404(Project, portfolio__user__username=username, name=project_name)
    
    # Verifica se o usuário já votou no projeto
    vote, created = Vote.objects.get_or_create(user=request.user, project=project)

    if created:
        print('Voto adicionado!')
        project.add_vote()
    else:
        print('Voto removido!')
        vote.delete()
        project.remove_vote() 
    
    return JsonResponse({'success': created})


@login_required
def edit_project(request, username, project_name):
    project = get_object_or_404(Project, portfolio__user__username=username, name=project_name)

    # Verifica se o usuário é o proprietário do projeto
    if request.user != project.portfolio.user:
        messages.error(request, 'Você não tem permissão para editar este projeto.')
        return redirect('portfolio:user_portfolio', username=username)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES, instance=project)
        
        if project_form.is_valid():
            project_form.save()
            messages.success(request, 'Projeto atualizado com sucesso!')
            project_name = project_form.cleaned_data['name']
            return redirect('portfolio:edit_project', username=username, project_name=project_name)
        else:
            print(project_form.errors)
            messages.error(request, 'Erro ao atualizar o projeto. Verifique os dados e tente novamente.')
    else:
        project_form = ProjectForm(instance=project)

    return render(request, 'portfolios/portfolio/edit_project.html', {
        'project': project,
        'project_form': project_form,
    })


@login_required
def edit_project_image(request, username, project_name):
    # Busca o projeto pelo username do usuário e o nome do projeto
    project = get_object_or_404(Project, portfolio__user__username=username, name=project_name)

    # Garantir que o usuário atual é o proprietário do projeto
    if request.user != project.portfolio.user:
        messages.error(request, 'Você não tem permissão para editar este projeto.')
        return redirect('portfolio:user_portfolio', username=username)

    # Verifica se há uma nova imagem sendo enviada no request
    if request.method == 'POST' and 'img' in request.FILES:
        project.img = request.FILES['img']  # Atualiza a imagem do projeto
        project.save()  # Salva a nova imagem no banco de dados
    else:
        return JsonResponse({'error': 'Nenhuma imagem enviada.'})

    # Redireciona de volta para a página de edição do projeto
    return JsonResponse({'success': True})

@login_required
def delete_project(request, username, project_name):
    project = get_object_or_404(Project, portfolio__user__username=username, name=project_name)

    # Apenas o proprietário pode excluir o projeto
    if request.user == project.portfolio.user:
        project.delete()
        messages.success(request, 'Projeto excluído com sucesso!')
    
    return JsonResponse({'success': True})

@login_required
def upload_resource(request, username, project_name):
    project = get_object_or_404(Project, portfolio__user__username=username, name=project_name)
    
    if request.method == 'POST':
        resource_form = ResourceUploadForm(request.POST, request.FILES, project=project)
        
        if resource_form.is_valid():
            resource = resource_form.save(commit=False)
            resource.project = project
            resource.save()

            messages.success(request, 'Recurso adicionado com sucesso!')
            return redirect('portfolio:project_detail', username=username, project_name=project_name)
        else:
            messages.error(request, 'Erro ao adicionar recurso. Verifique os dados e tente novamente.')
    else:
        resource_form = ResourceUploadForm(project=project)

    return render(request, 'portfolios/portfolio/upload_resource.html', {
        'resource_form': resource_form,
        'project': project,
    })

@login_required
def delete_resource(request, username, project_name, resource_id):
    project = get_object_or_404(Project, portfolio__user__username=username, name=project_name)
    resource = get_object_or_404(Resource, project=project, id=resource_id)

    # Verifica se o usuário é o proprietário do projeto
    if request.user != project.portfolio.user:
        messages.error(request, 'Você não tem permissão para excluir este recurso.')
        return redirect('portfolio:project_detail', username=username, project_name=project_name)

    resource.delete()
    messages.success(request, 'Recurso excluído com sucesso!')
    return JsonResponse({'success': True})

@login_required
def upload_img_project(request, username, project_name):
    project = get_object_or_404(Project, portfolio__user__username=username, name=project_name)

    if not project.can_upload_more_images:
        messages.error(request, 'Você atingiu o limite de imagens permitidas para o seu tipo de conta.')
        return JsonResponse({'error': 'Limite de imagens atingido.'})

    if request.method == 'POST':
        img = request.FILES.get('image')  # Pegando a imagem do formulário
        
        if img:
            file_size = img.size  # Tamanho do arquivo
            file_type = img.content_type  # Tipo de conteúdo (ex: image/jpeg)

            # Verifica se o tamanho do arquivo ultrapassa o limite de 100MB para usuários Ultra
            if not project.can_upload_more_resources:
                messages.error(request, 'Você excedeu o limite de armazenamento do projeto.')
                return JsonResponse({'error': 'Limite de armazenamento excedido.'})

            # Salvando a imagem como um recurso
            resource = Resource.objects.create(
                project=project,
                file=img,
                file_type=file_type,
                file_size=file_size
            )
            messages.success(request, 'Imagem adicionada com sucesso!')
        else:
            messages.error(request, 'Erro ao adicionar a imagem. Por favor, tente novamente.')

    return JsonResponse({'success': True})