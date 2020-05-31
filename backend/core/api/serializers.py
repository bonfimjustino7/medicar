import datetime

from rest_framework import serializers, status
from core.models import Especialidade, Agenda, Medico, Consulta, Horario
from rest_framework.exceptions import ValidationError


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

class HorarioSerializers(serializers.RelatedField):

    def to_representation(self, value):
        return value.horario

    class Meta:
        model = Horario

class AgendaSerializers(serializers.ModelSerializer):
    medico = MedicoSerializers(read_only=True)
    medico_id = serializers.IntegerField(write_only=True)
    horario = HorarioSerializers(many=True, read_only=True)

    class Meta:
        model = Agenda
        fields = ('id', 'medico', 'medico_id', 'dia', 'horario',)

class ConsultasSerializers(serializers.ModelSerializer):
    agenda_id = serializers.IntegerField(write_only=True)
    medico = serializers.SerializerMethodField()
    dia = serializers.SerializerMethodField()

    class Meta:
        model = Consulta
        fields = ('id', 'dia', 'horario','data_agendamento','agenda_id', 'medico')

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
            if hora_consulta <= d.now().time():
                raise ValidationError({'detail': 'Não é possivel marcar consultas para horários passados.'})


        consulta = Consulta.objects.filter(user=self.context['request'].user, horario=self.initial_data['horario'], agenda__dia=agenda.dia)
        if consulta:
            raise ValidationError({'detail': 'Você já possui uma consulta neste dia e também neste horário.'})

        if consultas:
            raise ValidationError({'detail': 'Não é possivel marcar a consulta, pois o dia e horário já estão alocados.'})


        return super().is_valid(raise_exception)