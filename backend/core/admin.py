from datetime import datetime

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


class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        s = super(ReadOnlyAdmin, self).change_view(request, object_id, form_url, extra_context)
        s.context_data['change'] = False
        return s

@admin.register(Consulta)
class ConsultaAdmin(ReadOnlyAdmin):
    list_display = ('agenda', 'data_agendamento', 'user')
