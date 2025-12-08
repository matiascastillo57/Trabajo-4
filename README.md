# 🚀 SmartConnect API

Sistema de gestión de sensores y barreras IoT desarrollado con Django REST Framework.

## 👨‍💻 Información del Proyecto

**Autor:** Jorge Matías Castillo  
**RUT:** [Tu RUT]  
**Universidad:** Universidad de Chile  
**Curso:** Desarrollo de Aplicaciones Web  
**Fecha:** Diciembre 2024

## 🛠️ Stack Tecnológico

- **Backend:** Django 5.0 + Django REST Framework 3.14
- **Base de Datos:** MariaDB 10.5
- **Autenticación:** JWT (Simple JWT)
- **Servidor Web:** Apache 2.4 (Reverse Proxy)
- **WSGI:** Gunicorn 21.2
- **Sistema Operativo:** Amazon Linux 2023
- **Cloud:** AWS EC2 con IP Elástica

## 🌐 Servidor en Producción

**URL Base:** http://54.165.225.184/api/

**Panel de Administración:** http://54.165.225.184/admin/  
- Usuario: `admin`
- Contraseña: `Admin2024!`

## 📡 Endpoints Disponibles

### Públicos (Sin autenticación)
- `GET /api/info/` - Información del estudiante y proyecto

### Autenticación
- `POST /api/token/` - Obtener token de acceso
- `POST /api/token/refresh/` - Refrescar token
- `POST /api/token/verify/` - Verificar validez del token

### Recursos (Requieren autenticación JWT)
- `GET|POST /api/departamentos/` - Listar/Crear departamentos
- `GET|PUT|PATCH|DELETE /api/departamentos/{id}/` - Operaciones CRUD
- `GET /api/departamentos/{id}/sensores/` - Sensores de un departamento

- `GET|POST /api/sensores/` - Listar/Crear sensores
- `GET|PUT|PATCH|DELETE /api/sensores/{id}/` - Operaciones CRUD
- `POST /api/sensores/{id}/cambiar_estado/` - Cambiar estado del sensor

- `GET|POST /api/usuarios/` - Listar/Crear usuarios
- `GET|PUT|PATCH|DELETE /api/usuarios/{id}/` - Operaciones CRUD

- `GET|POST /api/barreras/` - Listar/Crear barreras
- `POST /api/barreras/{id}/abrir/` - Abrir barrera
- `POST /api/barreras/{id}/cerrar/` - Cerrar barrera

- `GET|POST /api/eventos/` - Listar/Crear eventos
- `GET /api/eventos/{id}/` - Detalle de evento

## 🗄️ Modelos de Datos

### Departamento
- `nombre` (CharField, unique)
- `descripcion` (TextField)
- `activo` (BooleanField)
- Timestamps automáticos

### Sensor
- `mac_address` (CharField, unique, formato: AA:BB:CC:DD:EE:FF)
- `nombre` (CharField)
- `estado` (CharField: activo/inactivo/mantenimiento)
- `departamento` (ForeignKey)
- `ultima_lectura` (DateTimeField, nullable)
- Timestamps automáticos

### Usuario
- `user` (OneToOne con User de Django)
- `rol` (CharField: admin/operador)
- `departamento` (ForeignKey, nullable)
- `telefono` (CharField)
- `activo` (BooleanField)

### Barrera
- `nombre` (CharField)
- `ubicacion` (CharField)
- `estado` (CharField: abierta/cerrada/bloqueada)
- `sensor` (ForeignKey, nullable)
- `departamento` (ForeignKey, nullable)
- Timestamps automáticos

### Evento
- `tipo` (CharField: apertura/cierre/alerta/acceso_denegado)
- `descripcion` (TextField)
- `sensor` (ForeignKey)
- `barrera` (ForeignKey, nullable)
- `usuario` (ForeignKey, nullable)
- `timestamp` (DateTimeField)
- `metadata` (JSONField)

## 🧪 Ejemplos de Uso

### Obtener información del proyecto (sin auth)
```bash
curl http://54.165.225.184/api/info/
```

### Obtener token JWT
```bash
curl -X POST http://54.165.225.184/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin2024!"}'
```

### Listar sensores (con auth)
```bash
TOKEN="tu_token_aqui"

curl -X GET http://54.165.225.184/api/sensores/ \
  -H "Authorization: Bearer $TOKEN"
```

### Crear departamento
```bash
curl -X POST http://54.165.225.184/api/departamentos/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Producción",
    "descripcion": "Área de producción industrial",
    "activo": true
  }'
```

### Crear sensor
```bash
curl -X POST http://54.165.225.184/api/sensores/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mac_address": "AA:BB:CC:DD:EE:01",
    "nombre": "Sensor Entrada Principal",
    "estado": "activo",
    "departamento": 1
  }'
```

## 🔧 Instalación Local
```bash
# Clonar repositorio
git clone https://github.com/matiascastillo57/Trabajo-4.git
cd Trabajo-4/smartconnect

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos en config/settings.py

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar servidor de desarrollo
python manage.py runserver
```

## 📁 Estructura del Proyecto
```
smartconnect/
├── api/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── staticfiles/
├── venv/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Despliegue en AWS EC2

### Servicios configurados:
- **Apache 2.4** como reverse proxy (puerto 80)
- **Gunicorn** ejecutando Django (puerto 8000)
- **MariaDB 10.5** como base de datos
- **IP Elástica** para persistencia de IP pública

### Logs:
```bash
# Logs de Gunicorn
tail -f ~/smartconnect/gunicorn-error.log

# Logs de Apache
sudo tail -f /var/log/httpd/smartconnect_error.log
```

### Reiniciar servicios:
```bash
# Reiniciar Gunicorn
pkill gunicorn
cd ~/smartconnect && source venv/bin/activate
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --daemon

# Reiniciar Apache
sudo systemctl restart httpd
```

## 🔐 Seguridad

- Autenticación JWT con tokens de 5 horas de duración
- CORS configurado para dominios específicos
- Validación de permisos por endpoint
- Contraseñas hasheadas con PBKDF2
- CSRF protection habilitado

## 📊 Características Principales

✅ API REST completa con CRUD para 5 modelos  
✅ Autenticación y autorización con JWT  
✅ Validación de datos con serializers  
✅ Filtros y búsquedas en endpoints  
✅ Paginación automática (20 items por página)  
✅ Panel de administración Django  
✅ Documentación de API  
✅ Manejo de errores personalizado  
✅ Logs de eventos del sistema  
✅ Despliegue en producción con Apache + Gunicorn  

## 📄 Licencia

Proyecto académico - Universidad de Chile 2024

## 📞 Contacto

**Jorge Matías Castillo**  
Email: [tu email]  
GitHub: [@matiascastillo57](https://github.com/matiascastillo57)
