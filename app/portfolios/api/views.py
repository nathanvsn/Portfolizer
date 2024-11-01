from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters as rest_framework_filters
from django.shortcuts import get_object_or_404
from portfolios.models import Project, Vote

from .serializers import ProjectSerializer
from .filters import ProjectFilter
from django_filters import rest_framework as django_filters

class ToggleVoteView(GenericAPIView):
    """
    CBV para adicionar ou remover um voto em um projeto.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        
        # Verifica se o usuário já votou no projeto
        vote_exists = project.user_has_voted(request.user)

        if vote_exists:
            # Remove o voto
            vote = Vote.objects.get(user=request.user, project=project)
            vote.delete()
            project.remove_vote()
            message = "Voto removido com sucesso."
        else:
            # Cria o voto
            Vote.objects.create(user=request.user, project=project)
            project.add_vote()
            message = "Voto registrado com sucesso."
        
        return Response({"detail": message, "votes_count": project.votes}, status=status.HTTP_200_OK)


class ProjectListAPIView(ListAPIView):
    """
    CBV para listar todos os projetos, com filtros de data e votos.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 15
    filter_backends = [django_filters.DjangoFilterBackend, rest_framework_filters.OrderingFilter]
    filterset_class = ProjectFilter
    ordering_fields = ['votes', 'created_at']  # Permite ordenar pela contagem de votos e data de criação
