import datetime

from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework import serializers, status
from core.models import Especialidade, Agenda, Medico, Consulta, Horario
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

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
            if horario.horario > datetime.datetime.now().time():  # filtra os horarios passados
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
        consultas = Consulta.objects.filter(agenda__dia=agenda.dia, horario=self.initial_data['horario'])

        if agenda.dia < d.now().date():
            raise ValidationError({'detail': 'Não é possivel marcar consultass para dias passados.'})

        if d.now().date() == agenda.dia:
            hora_consulta = d.strptime(self.initial_data['horario'], '%H:%M').time()
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
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'token')


    def is_valid(self, raise_exception=False):
        dados = self.initial_data
        if dados['password'] and dados['password2'] and dados['password'] != dados['password2']:
            raise ValidationError({'datail': 'As senhas devem combinar.'})

        return super().is_valid(raise_exception)

    def validate(self, attrs):
        data = attrs
        del data['password2']
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

        return super().validate(data)


    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        serialize = self.to_representation(user)
        serialize['token'] = Token.objects.get(user=user).key

        return serialize
