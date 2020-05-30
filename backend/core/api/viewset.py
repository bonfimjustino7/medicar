from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from core.models import Especialidade, Agenda, Medico
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .serializers import EspecialidadeSerializers, MedicoSerializers


class EspecialidadeViewSet(viewsets.ModelViewSet):

    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializers
    authentication_classes = [TokenAuthentication]  # define qual tipo de authenticacao
    permission_classes = [IsAuthenticated] # fecha o endpoint para aceitar requests authenticadas
    filter_backends = [SearchFilter]  # define o filtro backend
    search_fields = ['nome']  # define qual o campo estará habilitado para busca

class MedicoViewSet(viewsets.ModelViewSet):

    queryset = Medico.objects.all()
    serializer_class = MedicoSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter,]  # define o filtro backend
    search_fields = ['nome']  # define qual o campo estará habilitado para busca

    def get_queryset(self):
        especialidades = self.request.query_params.getlist('especialidade')  # pega as especialidades dos params da request

        queryset = Medico.objects.filter(especialidade_id__in=especialidades)  # filtra as especialidades
        return queryset
