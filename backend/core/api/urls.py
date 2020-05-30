from django.urls import path, include
from rest_framework import routers
from core.api import viewset

router = routers.DefaultRouter()
router.register(r'especialidades', viewset.EspecialidadeViewSet)
router.register(r'medicos', viewset.MedicoViewSet)
# router.register(r'ongs', viewset.OngsViewSet)
# router.register(r'products', viewset.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('session', views.SessionUser.as_view())
]