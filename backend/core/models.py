from django.db import models

# Create your models here.
class Especialidade(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=6)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=9, null=True, blank=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Médico(a)'
        verbose_name_plural ='Médico(a)s'

class Agenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, verbose_name='Médico')
    dia = models.DateField()
    horario = models.TimeField('horário')

    class Meta:
        ordering = ['dia', 'horario']

    def __str__(self):
        return str(self.medico)

