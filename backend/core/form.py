from django import forms
from core.models import Agenda
import datetime

class AgendaForm(forms.ModelForm):

    class Meta:
        fields = ('medico', 'dia', 'horario',)

    def clean(self):

        dados = super().clean()
        agendas = Agenda.objects.filter(dia__day=dados['dia'].day, medico=dados['medico'])

        if agendas:
            return self.add_error('dia', self.error_class(['Este médico já agendado para esse dia.']))

        if dados['dia'].day < datetime.datetime.now().day:
            return self.add_error('dia', self.error_class(['Não é possivel marcar agendas para dias passados.']))