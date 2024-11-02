from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
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
        queryset = Work.objects.filter(is_active=True)
        
        # Filtro por termo de busca
        search_term = self.request.GET.get('search_term')
        if search_term:
            queryset = queryset.filter(
                Q(user__username__icontains=search_term) |
                Q(user__bio__icontains=search_term)
            )

        # Filtro por tags
        tags = self.request.GET.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__name__in=tags).distinct()
        
        # Ordenação
        sort_by = self.request.GET.get('sort_by')
        if sort_by == "a-z":
            queryset = queryset.order_by("client__user__username")
        elif sort_by == "z-a":
            queryset = queryset.order_by("-client__user__username")
        elif sort_by == "ranking_desc":
            queryset = queryset.order_by("-client__rating")
        elif sort_by == "ranking_asc":
            queryset = queryset.order_by("client__rating")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar tags disponíveis com contagem de Works para cada uma
        available_tags_with_counts = (
            Work.objects.filter(is_active=True)
            .values('tags__name')
            .annotate(count=Count('tags__name'))
            .order_by('-count')
        )
        
        # Convertendo para dicionário {tag: count} para facilitar o uso no template
        context['available_tags_with_counts'] = {
            item['tags__name']: item['count'] for item in available_tags_with_counts
        }
        
        # Passar tags selecionadas como lista para o contexto
        context['selected_tags'] = self.request.GET.getlist('tags')
                
        return context

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

