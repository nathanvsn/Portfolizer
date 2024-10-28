from django.urls import path
from .views.freelancer_views import FreelancerListView, FreelancerDetailView
from .views.client_views import WorkListView, WorkDetailView, WorkCreateView

app_name = 'freelance'

urlpatterns = [
    path('freelancers/', FreelancerListView.as_view(), name='freelancer_list'),
    path('freelancers/<int:pk>/', FreelancerDetailView.as_view(), name='freelancer_detail'),
    
    
    path('works/', WorkListView.as_view(), name='work_list'),
    path('works/<int:pk>/', WorkDetailView.as_view(), name='work_detail'),
    path('works/add/', WorkCreateView.as_view(), name='work_create'),
]