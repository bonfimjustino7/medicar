from django.urls import path, include
from rest_framework import routers
from core.api import viewset

router = routers.DefaultRouter()
router.register(r'especialidades', viewset.EspecialidadeViewSet)
router.register(r'medicos', viewset.MedicoViewSet)
router.register(r'consultas', viewset.ConsultaViewSet)
router.register(r'agendas', viewset.AgendaViewSet)
router.register(r'cadastro', viewset.CreateUserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]