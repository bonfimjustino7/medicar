from django.http import Http404, JsonResponse
from rest_framework import serializers, status
from core.models import Especialidade, Agenda, Medico
from rest_framework.response import Response


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
