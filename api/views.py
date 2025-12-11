from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Departamento, Sensor, Usuario, Barrera, Evento
from .serializers import (
    DepartamentoSerializer, SensorSerializer, UsuarioSerializer,
    BarreraSerializer, EventoSerializer
)
from .permissions import IsAdminUser

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """API Root - Bienvenida a SmartConnect API"""
    return Response({
        'mensaje': 'Bienvenido a SmartConnect API',
        'version': '1.0',
        'endpoints': {
            'publicos': {
                'info_proyecto': request.build_absolute_uri('/api/info/'),
                'obtener_token': request.build_absolute_uri('/api/token/'),
                'refrescar_token': request.build_absolute_uri('/api/token/refresh/'),
                'verificar_token': request.build_absolute_uri('/api/token/verify/'),
            },
            'recursos': {
                'departamentos': request.build_absolute_uri('/api/departamentos/'),
                'sensores': request.build_absolute_uri('/api/sensores/'),
                'barreras': request.build_absolute_uri('/api/barreras/'),
                'eventos': request.build_absolute_uri('/api/eventos/'),
                'usuarios': request.build_absolute_uri('/api/usuarios/'),
            },
            'administracion': {
                'panel_admin': request.build_absolute_uri('/admin/'),
            }
        },
        'autenticacion': {
            'tipo': 'JWT Bearer Token',
            'header': 'Authorization: Bearer <token>',
            'ejemplo_login': {
                'url': request.build_absolute_uri('/api/token/'),
                'metodo': 'POST',
                'body': {'username': 'admin', 'password': 'Admin2024!'}
            }
        },
        'documentacion': {
            'repositorio': 'https://github.com/matiascastillo57/Trabajo-4',
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def info_estudiante(request):
    """Informacion del proyecto y el estudiante"""
    return Response({
        'estudiante': {
            'nombre': 'Jorge Matias Castillo',
            'rut': 'TU-RUT-AQUI',
            'carrera': 'Ingenieria en Informatica',
            'universidad': 'Universidad de Chile',
            'curso': 'Desarrollo de Aplicaciones Web',
            'profesor': 'Nombre del Profesor'
        },
        'proyecto': {
            'nombre': 'SmartConnect API',
            'version': '1.0',
            'descripcion': 'Sistema de gestion de sensores y barreras IoT',
            'tecnologias': ['Django', 'Django REST Framework', 'MariaDB', 'JWT', 'Apache', 'Gunicorn']
        },
        'servidor': {
            'ip': request.get_host().split(':')[0],
            'puerto': 80,
            'sistema_operativo': 'Amazon Linux 2023',
            'url_base': request.build_absolute_uri('/api/')
        }
    })

class DepartamentoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Departamentos"""
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['get'])
    def sensores(self, request, pk=None):
        """GET /api/departamentos/{id}/sensores/"""
        departamento = self.get_object()
        sensores = Sensor.objects.filter(departamento=departamento)
        serializer = SensorSerializer(sensores, many=True)
        return Response({
            'departamento': departamento.nombre,
            'total_sensores': sensores.count(),
            'sensores': serializer.data
        })

class SensorViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Sensores"""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """POST /api/sensores/{id}/cambiar_estado/"""
        sensor = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in ['activo', 'inactivo', 'mantenimiento']:
            return Response(
                {'error': 'Estado invalido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        estado_anterior = sensor.estado
        sensor.estado = nuevo_estado
        sensor.save()
        
        return Response({
            'mensaje': 'Estado cambiado exitosamente',
            'sensor': sensor.nombre,
            'estado_anterior': estado_anterior,
            'estado_nuevo': sensor.estado
        })

class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class BarreraViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Barreras"""
    queryset = Barrera.objects.all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def abrir(self, request, pk=None):
        """POST /api/barreras/{id}/abrir/"""
        barrera = self.get_object()
        
        if barrera.estado == 'bloqueada':
            return Response(
                {'error': 'La barrera esta bloqueada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        estado_anterior = barrera.estado
        barrera.estado = 'abierta'
        barrera.save()
        
        Evento.objects.create(
            tipo='apertura',
            descripcion=f'Barrera {barrera.nombre} abierta',
            barrera=barrera,
            sensor=barrera.sensor,
            metadata={'estado_anterior': estado_anterior}
        )
        
        return Response({
            'mensaje': f'Barrera {barrera.nombre} abierta',
            'estado': barrera.estado
        })
    
    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        """POST /api/barreras/{id}/cerrar/"""
        barrera = self.get_object()
        
        if barrera.estado == 'bloqueada':
            return Response(
                {'error': 'La barrera esta bloqueada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        estado_anterior = barrera.estado
        barrera.estado = 'cerrada'
        barrera.save()
        
        Evento.objects.create(
            tipo='cierre',
            descripcion=f'Barrera {barrera.nombre} cerrada',
            barrera=barrera,
            sensor=barrera.sensor,
            metadata={'estado_anterior': estado_anterior}
        )
        
        return Response({
            'mensaje': f'Barrera {barrera.nombre} cerrada',
            'estado': barrera.estado
        })

class EventoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Eventos"""
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = Evento.objects.all()
        
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        sensor_id = self.request.query_params.get('sensor', None)
        if sensor_id:
            queryset = queryset.filter(sensor_id=sensor_id)
        
        return queryset
