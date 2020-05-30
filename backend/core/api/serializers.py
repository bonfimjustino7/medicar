from rest_framework import serializers
from core.models import Especialidade, Agenda, Medico

class EspecialidadeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Especialidade
        fields = ('id', 'nome',)