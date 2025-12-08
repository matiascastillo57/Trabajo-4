from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Sensor, Departamento, Usuario, Evento, Barrera

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class DepartamentoSerializer(serializers.ModelSerializer):
    total_sensores = serializers.SerializerMethodField()
    
    class Meta:
        model = Departamento
        fields = ['id', 'nombre', 'descripcion', 'activo', 'total_sensores', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_total_sensores(self, obj):
        return obj.sensores.count()


class SensorSerializer(serializers.ModelSerializer):
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Sensor
        fields = ['id', 'mac_address', 'nombre', 'estado', 'departamento', 
                  'departamento_nombre', 'ultima_lectura', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_mac_address(self, value):
        import re
        if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', value):
            raise serializers.ValidationError("Formato de MAC address inválido")
        return value.upper()


class UsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(write_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'user', 'username', 'password', 'email', 'rol', 
                  'departamento', 'departamento_nombre', 'telefono', 'activo', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        usuario = Usuario.objects.create(user=user, **validated_data)
        return usuario


class BarreraSerializer(serializers.ModelSerializer):
    sensor_nombre = serializers.CharField(source='sensor.nombre', read_only=True)
    departamento_nombre = serializers.CharField(source='departamento.nombre', read_only=True)
    
    class Meta:
        model = Barrera
        fields = ['id', 'nombre', 'ubicacion', 'estado', 'sensor', 'sensor_nombre',
                  'departamento', 'departamento_nombre', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class EventoSerializer(serializers.ModelSerializer):
    sensor_nombre = serializers.CharField(source='sensor.nombre', read_only=True)
    barrera_nombre = serializers.CharField(source='barrera.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.user.username', read_only=True)
    
    class Meta:
        model = Evento
        fields = ['id', 'tipo', 'descripcion', 'sensor', 'sensor_nombre',
                  'barrera', 'barrera_nombre', 'usuario', 'usuario_nombre',
                  'timestamp', 'metadata']
        read_only_fields = ['id', 'timestamp']
