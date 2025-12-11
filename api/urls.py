
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear router de DRF
router = DefaultRouter()
router.register(r'departamentos', views.DepartamentoViewSet, basename='departamento')
router.register(r'sensores', views.SensorViewSet, basename='sensor')
router.register(r'usuarios', views.UsuarioViewSet, basename='usuario')
router.register(r'barreras', views.BarreraViewSet, basename='barrera')
router.register(r'eventos', views.EventoViewSet, basename='evento')

urlpatterns = [
    # Vista raíz de la API (público)
    path('', views.api_root, name='api-root'),
    
    # Información del estudiante (público)
    path('info/', views.info_estudiante, name='info-estudiante'),
    
    # Incluir todas las rutas del router
    path('', include(router.urls)),
]
