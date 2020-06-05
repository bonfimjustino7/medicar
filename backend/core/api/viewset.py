import datetime

from django.contrib.auth.models import User
from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from core.models import Especialidade, Agenda, Medico, Consulta
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EspecialidadeSerializers, MedicoSerializers, ConsultasSerializers, AgendaSerializers, \
    CreateSerializers, UserAuthenticate


class EspecialidadeViewSet(viewsets.ModelViewSet):
    queryset = Especialidade.objects.all()
    serializer_class = EspecialidadeSerializers
    authentication_classes = [TokenAuthentication]  # define qual tipo de authenticacao
    permission_classes = [IsAuthenticated]  # fecha o endpoint para aceitar requests authenticadas
    filter_backends = [SearchFilter]  # define o filtro backend
    search_fields = ['nome']  # define qual o campo estará habilitado para busca


class MedicoViewSet(viewsets.ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, ]  # define o filtro backend
    search_fields = ['nome']  # define qual o campo estará habilitado para busca

    def get_queryset(self):
        queryset = self.queryset
        especialidades = self.request.query_params.getlist(
            'especialidade')  # pega as especialidades dos params da request
        if especialidades:
            queryset = Medico.objects.filter(especialidade_id__in=especialidades)  # filtra as especialidades

        return queryset


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultasSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset().filter(user=self.request.user).exclude(
            agenda__dia__lt=datetime.datetime.now().date()).exclude(horario__lt=datetime.datetime.now().time())
        return qs.order_by('agenda__dia', 'horario')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = request.user

        consulta = Consulta.objects.create(**serializer.validated_data)
        return Response(serializer.to_representation(consulta), status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        consulta = self.get_object()
        if consulta.agenda.dia < datetime.datetime.now().date():  # is now ?
            raise ValidationError({'detail': 'Você não pode desmarcar essa consulta. Ela já aconteceu.'})

        elif consulta.agenda.dia == datetime.datetime.now().date():  # is now ?
            if consulta.horario <= datetime.datetime.now().time():
                raise ValidationError({'detail': 'Você não pode desmarcar essa consulta. Ela já aconteceu.'})

        super(ConsultaViewSet, self).destroy(request, *args, **kwargs)


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, ]

    def get_queryset(self):
        queryset = self.queryset.exclude(dia__lt=datetime.datetime.now().date()).order_by('dia')

        try:
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
        except ValueError:
            raise ValidationError({'detail': 'Argumento de filtro inválido.'})

        new_queryset = []
        for agenda in queryset:
            horarios_disponiveis = [obj.horario for obj in agenda.horario.all()]
            for consulta in agenda.consulta_set.all():
                if consulta.horario in horarios_disponiveis:
                    horarios_disponiveis.remove(consulta.horario)

            if horarios_disponiveis:
                new_queryset.append(agenda)

        return new_queryset


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateSerializers

class CustomAuthToken(ObtainAuthToken):

    serializer_class = UserAuthenticate

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'name': user.first_name,
        })