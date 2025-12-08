from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Sensor, Departamento, Usuario, Evento, Barrera
from .serializers import (
    SensorSerializer, DepartamentoSerializer, 
    UsuarioSerializer, EventoSerializer, BarreraSerializer
)

@api_view(['GET'])
@permission_classes([AllowAny])
def info_estudiante(request):
    """
    Endpoint público con información del estudiante.
    """
    # Obtener IP real desde el request
    host = request.get_host()
    # Quitar el puerto si existe
    if ':' in host:
        host = host.split(':')[0]
    
    data = {
        "estudiante": {
            "nombre": "Jorge Matías Castillo",
            "rut": "TU-RUT-AQUI",
            "carrera": "Ingeniería en Informática",
            "universidad": "Universidad de Chile",
            "curso": "Desarrollo de Aplicaciones Web",
            "profesor": "Nombre del Profesor"
        },
        "proyecto": {
            "nombre": "SmartConnect API",
            "version": "1.0",
            "descripcion": "Sistema de gestión de sensores y barreras IoT",
            "tecnologias": ["Django", "Django REST Framework", "MariaDB", "JWT", "Apache", "Gunicorn"]
        },
        "servidor": {
            "ip": host,  # Mostrará la IP sin puerto
            "puerto": 80,
            "sistema_operativo": "Amazon Linux 2023",
            "url_base": f"http://{host}/api/"
        }
    }
    return Response(data)


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def sensores(self, request, pk=None):
        departamento = self.get_object()
        sensores = departamento.sensores.all()
        serializer = SensorSerializer(sensores, many=True)
        return Response(serializer.data)


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Sensor.objects.all()
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
        departamento = self.request.query_params.get('departamento', None)
        if departamento:
            queryset = queryset.filter(departamento_id=departamento)
        return queryset
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        sensor = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado not in ['activo', 'inactivo', 'mantenimiento']:
            return Response(
                {"error": "Estado inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sensor.estado = nuevo_estado
        sensor.save()
        
        return Response({
            "message": f"Estado cambiado a {nuevo_estado}",
            "sensor": SensorSerializer(sensor).data
        })


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Usuario.objects.all()
        rol = self.request.query_params.get('rol', None)
        if rol:
            queryset = queryset.filter(rol=rol)
        return queryset


class BarreraViewSet(viewsets.ModelViewSet):
    queryset = Barrera.objects.all()
    serializer_class = BarreraSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def abrir(self, request, pk=None):
        barrera = self.get_object()
        barrera.estado = 'abierta'
        barrera.save()
        
        Evento.objects.create(
            tipo='apertura',
            descripcion=f'Barrera {barrera.nombre} abierta',
            sensor=barrera.sensor,
            barrera=barrera
        )
        
        return Response({
            "message": "Barrera abierta",
            "barrera": BarreraSerializer(barrera).data
        })
    
    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        barrera = self.get_object()
        barrera.estado = 'cerrada'
        barrera.save()
        
        Evento.objects.create(
            tipo='cierre',
            descripcion=f'Barrera {barrera.nombre} cerrada',
            sensor=barrera.sensor,
            barrera=barrera
        )
        
        return Response({
            "message": "Barrera cerrada",
            "barrera": BarreraSerializer(barrera).data
        })


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Evento.objects.all()
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        sensor = self.request.query_params.get('sensor', None)
        if sensor:
            queryset = queryset.filter(sensor_id=sensor)
        return queryset.order_by('-timestamp')
