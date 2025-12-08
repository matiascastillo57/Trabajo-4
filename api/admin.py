from django.contrib import admin
from .models import Sensor, Departamento, Usuario, Evento, Barrera

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'created_at']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion']

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'mac_address', 'estado', 'departamento', 'created_at']
    list_filter = ['estado', 'departamento']
    search_fields = ['nombre', 'mac_address']

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'departamento', 'activo', 'created_at']
    list_filter = ['rol', 'activo', 'departamento']
    search_fields = ['user__username', 'user__email']

@admin.register(Barrera)
class BarreraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'estado', 'sensor', 'created_at']
    list_filter = ['estado', 'departamento']
    search_fields = ['nombre', 'ubicacion']

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'sensor', 'barrera', 'timestamp']
    list_filter = ['tipo', 'timestamp']
    search_fields = ['descripcion']
    date_hierarchy = 'timestamp'
