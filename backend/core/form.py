from django import forms
from core.models import Agenda
import datetime

class AgendaForm(forms.ModelForm):

    class Meta:
        fields = ('medico', 'dia', 'horario',)

    def clean(self):

        dados = super().clean()
        agendas = Agenda.objects.filter(dia=dados['dia'], medico=dados['medico'])

        if agendas and not self.instance.id:
            return self.add_error('dia', self.error_class(['Este médico já está agendado para esse dia.']))

        if dados['dia'] < datetime.datetime.now().date():
            return self.add_error('dia', self.error_class(['Não é possivel marcar agendas para dias passados.']))
