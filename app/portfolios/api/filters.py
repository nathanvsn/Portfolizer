from django_filters import rest_framework as filters
from django.utils import timezone
from datetime import timedelta
from portfolios.models import Project

class ProjectFilter(filters.FilterSet):
    period = filters.CharFilter(method='filter_by_period', label='Period')

    class Meta:
        model = Project
        fields = ['period']  # 'period' não é um campo de modelo, mas será usado no filtro personalizado

    def filter_by_period(self, queryset, name, value):
        # Define o filtro por período (semana, mês) e ordena por votos
        days = {'week': 7, 'month': 30}
        period_days = days.get(value, None)
        
        if period_days:
            start_date = timezone.now() - timedelta(days=period_days)
            queryset = queryset.filter(created_at__gte=start_date)
        
        return queryset.order_by('-votes')
