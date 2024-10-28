from django.views.generic import ListView, DetailView
from freelance.models import Freelancer

class FreelancerListView(ListView):
    model = Freelancer
    template_name = 'freelances/freelancers/list.html'
    context_object_name = 'freelancers'
    paginate_by = 10 

    def get_queryset(self):
        return Freelancer.objects.filter(is_active=True)

class FreelancerDetailView(DetailView):
    model = Freelancer
    template_name = 'freelances/freelancers/detail.html'
    context_object_name = 'freelancer'
