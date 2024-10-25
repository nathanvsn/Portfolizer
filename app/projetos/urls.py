from django.urls import path
from . import views

app_name = 'projetos'

urlpatterns = [
    path('', views.index, name='index'),
]