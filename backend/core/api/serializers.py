import datetime

from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework import serializers, status
from rest_framework.authtoken.serializers import AuthTokenSerializer

from core.models import Especialidade, Agenda, Medico, Consulta, Horario
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

class EspecialidadeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ('id', 'nome',)


class MedicoSerializers(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializers(read_only=True, many=False)
    especialidade_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Medico
        fields = ('id', 'crm', 'nome', 'especialidade', 'especialidade_id')

class AgendaSerializers(serializers.ModelSerializer):
    medico = MedicoSerializers(read_only=True)
    medico_id = serializers.IntegerField(write_only=True)
    horario = serializers.SerializerMethodField()

    def get_horario(self, value):
        horarios_disponiveis = []
        for horario in value.horario.all():
            if horario.horario > datetime.datetime.now().time() or datetime.datetime.now().date() != value.dia:  # filtra os horarios passados
                horarios_disponiveis.append(horario.horario)

        for consulta in value.consulta_set.all():
            if consulta.horario in horarios_disponiveis:
                horarios_disponiveis.remove(consulta.horario)

        return [hour.strftime('%H:%M') for hour in horarios_disponiveis ]


    class Meta:
        model = Agenda
        fields = ('id', 'medico', 'medico_id', 'dia', 'horario',)


class ConsultasSerializers(serializers.ModelSerializer):
    agenda_id = serializers.IntegerField(write_only=True)
    medico = serializers.SerializerMethodField()
    dia = serializers.SerializerMethodField()

    class Meta:
        model = Consulta
        fields = ('id', 'dia', 'horario', 'data_agendamento', 'agenda_id', 'medico')

    def get_dia(self, obj):
        return obj.agenda.dia

    def get_medico(self, obj):
        serializer = MedicoSerializers(obj.agenda.medico)
        return serializer.data

    def is_valid(self, raise_exception=False):
        d = datetime.datetime

        agenda = Agenda.objects.get(id=self.initial_data['agenda_id'])
        consultas = Consulta.objects.filter(agenda__dia=agenda.dia, horario=self.initial_data['horario'], agenda__medico=agenda.medico)
        hora_consulta = d.strptime(self.initial_data['horario'], '%H:%M').time()

        if agenda.dia < d.now().date() and hora_consulta != datetime.time(hour=0):
            raise ValidationError({'detail': 'Não é possivel marcar consultass para dias passados.'})

        hora = d.strptime(self.initial_data['horario'], '%H:%M').time()
        flag = True
        for h in agenda.horario.all():
            if hora == h.horario:
                flag = False
                break

        if flag:
            raise ValidationError({'detail': 'Esse horário não está disponivel para essa agenda.'})


        if d.now().date() == agenda.dia:
            if hora_consulta < d.now().time():
                raise ValidationError({'detail': 'Não é possivel marcar consultas para horários passados.'})

        consulta = Consulta.objects.filter(user=self.context['request'].user, horario=self.initial_data['horario'],
                                           agenda__dia=agenda.dia)
        if consulta:
            raise ValidationError({'detail': 'Você já possui uma consulta neste dia e também neste horário.'})

        if consultas:
            raise ValidationError(
                {'detail': 'Não é possivel marcar a consulta, pois o dia e horário já estão alocados.'})

        return super().is_valid(raise_exception)

class CreateSerializers(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'token', 'first_name', 'email')


    def is_valid(self, raise_exception=False):
        is_valid = super().is_valid(raise_exception)
        dados = self.initial_data
        if dados['password'] and dados['password2'] and dados['password'] != dados['password2']:
            raise ValidationError({'datail': 'As senhas devem combinar.'})

        if '@' not in dados['email']:
            raise ValidationError({'detail': 'Email inválido.'})

        return is_valid

    def validate(self, attrs):
        data = attrs
        del data['password2']

        user = User.objects.filter(email=data['email'])
        if user:
            raise ValidationError({'detail': 'Já existe um usuário com esse email.'})

        if not data.get('username'):
            username = str(data['email']).split('@')[0]
            user = User.objects.filter(username=username)
            if not user:
                data['username'] = username
            else:
                raise ValidationError({'detail': 'Já existe um usuário com esse username'})

        user = User(**data)

        password = attrs.get('password')
        errors = dict()
        try:
            # validate the password and catch the exception
            password_validation.validate_password(password=password, user=User)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
            raise ValidationError(errors)

        return data


    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        serialize = self.to_representation(user)
        serialize['token'] = Token.objects.get(user=user).key

        return serialize

class UserAuthenticate(AuthTokenSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            if '@' in username:
                user = User.objects.filter(email=username)
                if user.count() == 1:
                    username = user.get()

            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


