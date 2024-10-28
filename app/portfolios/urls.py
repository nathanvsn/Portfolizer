from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Rota para a página inicial do portfólio do usuário, acessada por seu username
    path('<str:username>/', views.user_portfolio, name='user_portfolio'),
    
    path('file-manager/<str:username>/', views.file_manager, name='file_manager'),


    # Rota para upload de imagens ou recursos no projeto
    path('upload-resource/<str:username>/<str:project_name>/', views.upload_resource, name='upload_resource'),
    path('upload-img/<str:username>/<str:project_name>/', views.upload_img_project, name='upload_img_project'),
    path('delete-resource/<str:username>/<str:project_name>/<int:resource_id>/', views.delete_resource, name='delete_resource'),



    path('create-project/<str:username>/', views.create_project, name='create_project'),
    path('<str:username>/<str:project_name>/', views.project_detail, name='project_detail'),
    path('edit/<str:username>/<str:project_name>/', views.edit_project, name='edit_project'),
    path('project/edit-image/<str:username>/<str:project_name>/', views.edit_project_image, name='edit_project_image'),
    
    path('vote/<str:username>/<str:project_name>/', views.vote_project, name='vote_project'),

    path('<str:username>/<str:project_name>/delete/', views.delete_project, name='delete_project'),
    
    path('project/<str:username>/<str:project_name>/', views.project_detail_ajax, name='project_detail_ajax'),
    
    
]