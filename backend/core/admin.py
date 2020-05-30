from django.contrib import admin

# Register your models here.
from core.models import Especialidade, Medico, Agenda

from core.form import AgendaForm


@admin.register(Especialidade)
class Especialidade(admin.ModelAdmin):
    pass


@admin.register(Medico)
class Medico(admin.ModelAdmin):
    pass


@admin.register(Agenda)
class Agenda(admin.ModelAdmin):
    list_display = ('medico', 'dia', 'horario',)
    form = AgendaForm