from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status

from freelance.models import Freelancer, Client
from .serializers import FreelancerSerializer, ClientSerializer
from .permissions import FrelancerPermission, ClientPermission

class FreelancerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    permission_classes = [FrelancerPermission]
    
    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FreelancerListAPIView(ListAPIView):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    pagination_class = LimitOffsetPagination


class WorkRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [ClientPermission]
    
    def delete(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class WorkListAPIView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    pagination_class = LimitOffsetPagination
