from django.contrib import admin, messages

# Register your models here.
from core.models import Especialidade, Medico, Agenda, Horario, Consulta

from core.form import AgendaForm


@admin.register(Especialidade)
class Especialidade(admin.ModelAdmin):
    pass


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    pass


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('medico', 'dia')
    form = AgendaForm

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('agenda', 'data_agendamento', 'user')