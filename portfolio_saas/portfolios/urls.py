from django.urls import path
from . import views

urlpatterns = [
    # Rota para a página inicial do portfólio do usuário, acessada por seu username
    path('<str:username>/', views.user_portfolio, name='user_portfolio'),
    
    # Rota para exibir um projeto específico pelo nome do projeto
    path('<str:username>/<str:project_name>/', views.project_detail, name='project_detail'),
    
    # Rota para criar novos projetos
    path('<str:username>/create-project/', views.create_project, name='create_project'),

    # Rota para upload de imagens ou recursos no projeto
    path('<str:username>/<str:project_name>/upload-resource/', views.upload_resource, name='upload_resource'),
]
