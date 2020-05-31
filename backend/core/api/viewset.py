import datetime

from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status

from core.models import Especialidade, Agenda, Medico, Consulta
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import EspecialidadeSerializers, MedicoSerializers, ConsultasSerializers, AgendaSerializers


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
        queryset = self.queryset
        especialidades = self.request.query_params.getlist('especialidade')  # pega as especialidades dos params da request
        if especialidades:
            queryset = Medico.objects.filter(especialidade_id__in=especialidades)  # filtra as especialidades

        return queryset

class ConsultaViewSet(viewsets.ModelViewSet):

    queryset = Consulta.objects.all()
    serializer_class = ConsultasSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        qs = qs.exclude(agenda__dia__lt=datetime.datetime.now().date())
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = request.user

        consulta = Consulta.objects.create(**serializer.validated_data)
        return Response(serializer.to_representation(consulta), status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        consulta = self.get_object()
        if consulta.agenda.dia < datetime.datetime.now().date(): # is now ?
            raise ValidationError({'detail': 'Você não pode desmarcar essa consulta. Ela já aconteceu.'})

        elif consulta.agenda.dia == datetime.datetime.now().date(): # is now ?
            if consulta.horario <= datetime.datetime.now().time():
                raise ValidationError({'detail': 'Você não pode desmarcar essa consulta. Ela já aconteceu.'})

        super(ConsultaViewSet, self).destroy(request, *args, **kwargs)


class AgendaViewSet(viewsets.ModelViewSet):

    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,]


    def get_queryset(self):
        consultas_marcadas = list(Consulta.objects.all().values_list('horario', flat=True))
        #queryset = self.queryset.exclude(dia__lt=datetime.datetime.now().date(), horario__horario__in=consultas_marcadas, )
        queryset = self.queryset.exclude(horario__horario__in=consultas_marcadas,)

        medicos = self.request.query_params.getlist('medico')
        especialidades = self.request.query_params.getlist('especialidade')
        data_inicio = self.request.query_params.get('data_inicio')
        data_final = self.request.query_params.get('data_final')

        if medicos:
            queryset = queryset.filter(medico_id__in=medicos)

        if especialidades:
            queryset = queryset.filter(medico__especialidade_id__in=especialidades)

        if data_inicio and data_final:
            queryset = queryset.filter(dia__range=[data_inicio, data_final])

        return queryset