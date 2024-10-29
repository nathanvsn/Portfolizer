from django.views.generic import ListView, DetailView
from freelance.models import Freelancer
from django.db.models import Q, Count


class FreelancerListView(ListView):
    model = Freelancer
    template_name = 'freelances/freelancers/list.html'
    context_object_name = 'freelancers'
    paginate_by = 10 

    def get_queryset(self):
        queryset = Freelancer.objects.filter(is_active=True)
        
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
            queryset = queryset.order_by("user__username")
        elif sort_by == "z-a":
            queryset = queryset.order_by("-user__username")
        elif sort_by == "ranking_desc":
            queryset = queryset.order_by("-ranking")
        elif sort_by == "ranking_asc":
            queryset = queryset.order_by("ranking")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Adicionar tags disponíveis com contagem de freelancers para cada uma
        available_tags_with_counts = (
            Freelancer.objects.filter(is_active=True)
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

class FreelancerDetailView(DetailView):
    model = Freelancer
    template_name = 'freelances/freelancers/detail.html'
    context_object_name = 'freelancer'
