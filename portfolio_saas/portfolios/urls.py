from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Rota para a página inicial do portfólio do usuário, acessada por seu username
    path('<str:username>/', views.user_portfolio, name='user_portfolio'),

    # Rota para upload de imagens ou recursos no projeto
    path('<str:username>/<str:project_name>/upload-resource/', views.upload_resource, name='upload_resource'),
    path('<str:username>/<str:project_name>/upload-img/', views.upload_img_project, name='upload_img_project'),
    path('<str:username>/<str:project_name>/delete-resource/<int:resource_id>/', views.delete_resource, name='delete_resource'),



    path('<str:username>/create-project/', views.create_project, name='create_project'),
    path('<str:username>/<str:project_name>/', views.project_detail, name='project_detail'),
    path('<str:username>/<str:project_name>/edit/', views.edit_project, name='edit_project'),
    path('project/<str:username>/<str:project_name>/edit-image/', views.edit_project_image, name='edit_project_image'),

    path('<str:username>/<str:project_name>/delete/', views.delete_project, name='delete_project'),
    
    path('project/<str:username>/<str:project_name>/', views.project_detail_ajax, name='project_detail_ajax'),


]
