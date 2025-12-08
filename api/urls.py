from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartamentoViewSet, SensorViewSet, UsuarioViewSet,
    EventoViewSet, BarreraViewSet, info_estudiante
)

router = DefaultRouter()
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')
router.register(r'sensores', SensorViewSet, basename='sensor')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'barreras', BarreraViewSet, basename='barrera')
router.register(r'eventos', EventoViewSet, basename='evento')

urlpatterns = [
    path('', include(router.urls)),
    path('info/', info_estudiante, name='info-estudiante'),
]
