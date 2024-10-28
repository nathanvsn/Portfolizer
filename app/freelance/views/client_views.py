from django.views.generic import ListView, DetailView
from django.db.models import Avg, Count
from freelance.models import Work
from freelance.forms import WorkForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class WorkListView(ListView):
    model = Work
    template_name = 'freelances/works/list.html'
    context_object_name = 'works'
    paginate_by = 10

    def get_queryset(self):
        works = Work.objects.filter(is_active=True).select_related('client__user')
        
        # Calcular média de rating e total de votos
        for work in works:
            reviews = work.client.user.received_reviews.all()
            work.total_votes = reviews.count()
            work.average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0  # Média ou 0 se não houver votos

        return works
class WorkDetailView(DetailView):
    model = Work
    template_name = 'freelances/works/detail.html'
    context_object_name = 'work'
    

class WorkCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Work
    form_class = WorkForm
    template_name = 'freelances/works/create.html'
    success_url = reverse_lazy('freelance:work_list')

    def form_valid(self, form):
        form.instance.client = self.request.user.client_profile  # Associa o cliente logado ao trabalho
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'client_profile')  # Apenas clientes podem acessar

