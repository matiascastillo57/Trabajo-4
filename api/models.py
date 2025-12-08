from django.db import models
from django.contrib.auth.models import User

class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departamentos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Sensor(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    
    mac_address = models.CharField(max_length=17, unique=True)
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, related_name='sensores')
    ultima_lectura = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sensores'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} ({self.mac_address})"


class Usuario(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('operador', 'Operador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operador')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} ({self.rol})"


class Barrera(models.Model):
    ESTADO_CHOICES = [
        ('abierta', 'Abierta'),
        ('cerrada', 'Cerrada'),
        ('bloqueada', 'Bloqueada'),
    ]
    
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='cerrada')
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True, related_name='barreras')
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'barreras'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.estado}"


class Evento(models.Model):
    TIPO_CHOICES = [
        ('apertura', 'Apertura'),
        ('cierre', 'Cierre'),
        ('alerta', 'Alerta'),
        ('acceso_denegado', 'Acceso Denegado'),
    ]
    
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='eventos')
    barrera = models.ForeignKey(Barrera, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'eventos'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.tipo} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
