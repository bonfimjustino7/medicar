import datetime

from django.conf import settings
from django.db import models

# Create your models here.
class Especialidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=4)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=9, null=True, blank=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Médico(a)'
        verbose_name_plural ='Médico(a)s'

class Horario(models.Model):
    horario = models.TimeField()

    def __str__(self):
        return str(self.horario)

class Agenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, verbose_name='Médico')
    dia = models.DateField()
    horario = models.ManyToManyField(Horario)
    #has_preenchido = models.BooleanField(default=False, blank=True, null=True)

    # @property
    # def is_preenchido(self):
    #     horarios_cadastrados = [hour.horario.strftime('%H:%M') for hour in self.horario.all()]
    #     horarios_agendados = [consulta.horario.strftime('%H:%M') for consulta in self.consulta_set.all()]
    #
    #     if horarios_agendados == horarios_cadastrados:
    #         return True
    #     return False


    class Meta:
        ordering = ['dia']

    def __str__(self):
        return '%s - %s' % (self.medico, self.dia)

class Consulta(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuário')
    data_agendamento = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    horario = models.TimeField()


    def __str__(self):
        return str(self.user)