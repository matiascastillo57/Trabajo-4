# 🚀 SmartConnect API

Sistema de gestión de sensores y barreras IoT desarrollado con Django REST Framework.

## 👨‍🎓 Información del Proyecto

- **Estudiante:** Jorge Matías Castillo
- **Universidad:** INACAP
- **Carrera:** Ingeniería en Informática
- **Curso:** Desarrollo de Aplicaciones Web

## 🔧 Stack Tecnológico

- **Backend:** Django 5.0 + Django REST Framework 3.14
- **Base de Datos:** MariaDB 10.5
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **Servidor Web:** Apache 2.4 (Reverse Proxy)
- **WSGI Server:** Gunicorn
- **Sistema Operativo:** Amazon Linux 2023
- **Cloud:** AWS EC2

## 📡 Endpoints Disponibles

### Públicos (sin autenticación)
- `GET /` - Página de inicio HTML
- `GET /api/` - API Root (información de endpoints)
- `GET /api/info/` - Información del proyecto y estudiante

### Autenticación
- `POST /api/token/` - Obtener access y refresh tokens
- `POST /api/token/refresh/` - Refrescar token
- `POST /api/token/verify/` - Verificar validez del token

### Recursos (requieren autenticación)
- `GET/POST /api/departamentos/` - CRUD de departamentos
- `GET /api/departamentos/{id}/sensores/` - Sensores por departamento
- `GET/POST /api/sensores/` - CRUD de sensores
- `POST /api/sensores/{id}/cambiar_estado/` - Cambiar estado del sensor
- `GET/POST /api/barreras/` - CRUD de barreras
- `POST /api/barreras/{id}/abrir/` - Abrir barrera
- `POST /api/barreras/{id}/cerrar/` - Cerrar barrera
- `GET/POST /api/eventos/` - CRUD de eventos (con filtros)
- `GET/POST /api/usuarios/` - CRUD de usuarios

### Administración
- `/admin/` - Panel de administración de Django

## 🔐 Credenciales de Prueba

**Admin:**
- Username: `admin`
- Password: `Admin2024!`

## 🗃️ Modelos de Datos

### 1. Departamento
- nombre (único)
- descripcion
- activo
- timestamps

### 2. Sensor
- mac_address (único, formato: AA:BB:CC:DD:EE:FF)
- nombre
- estado (activo/inactivo/mantenimiento)
- departamento (FK)
- ultima_lectura
- timestamps

### 3. Usuario
- user (OneToOne con User de Django)
- rol (admin/operador)
- departamento (FK, nullable)
- telefono
- activo
- timestamp

### 4. Barrera
- nombre
- ubicacion
- estado (abierta/cerrada/bloqueada)
- sensor (FK, nullable)
- departamento (FK, nullable)
- timestamps

### 5. Evento
- tipo (apertura/cierre/alerta/acceso_denegado)
- descripcion
- sensor (FK)
- barrera (FK, nullable)
- usuario (FK, nullable)
- timestamp
- metadata (JSON)

## 🚀 Instalación y Despliegue

### Requisitos Previos
- Python 3.11+
- MariaDB 10.5+
- Apache 2.4+
- Git

### 1. Clonar el Repositorio
```bash
git clone https://github.com/matiascastillo57/Trabajo-4.git
cd Trabajo-4
```

### 2. Crear Entorno Virtual
```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos
```sql
CREATE DATABASE smartconnect;
CREATE USER 'smartuser'@'localhost' IDENTIFIED BY 'SmartPass2024!';
GRANT ALL PRIVILEGES ON smartconnect.* TO 'smartuser'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Aplicar Migraciones
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Recopilar Archivos Estáticos
```bash
python manage.py collectstatic
```

### 7. Ejecutar Servidor de Desarrollo
```bash
python manage.py runserver
```

## 🔧 Configuración de Producción

### Apache como Reverse Proxy
Ver archivo: `/etc/httpd/conf.d/smartconnect.conf`

### Gunicorn
```bash
gunicorn config.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 3 \
  --timeout 120 \
  --daemon
```

## 📝 Ejemplo de Uso

### Obtener Token
```bash
curl -X POST http://54.165.225.184/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin2024!"}'
```

### Listar Departamentos
```bash
curl http://54.165.225.184/api/departamentos/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Crear Sensor
```bash
curl -X POST http://54.165.225.184/api/sensores/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "nombre": "Sensor Puerta Principal",
    "estado": "activo",
    "departamento": 1
  }'
```

## 🌐 URLs de Producción

- **Web:** http://54.165.225.184/
- **API:** http://54.165.225.184/api/
- **Admin:** http://54.165.225.184/admin/

## 📦 Dependencias Principales
```
Django==5.0.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.1
mysqlclient==2.2.1
gunicorn==21.2.0
django-cors-headers==4.3.1
```

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos para INACAP.

## 👤 Autor

**Jorge Matías Castillo**
- GitHub: [@matiascastillo57](https://github.com/matiascastillo57)
- Proyecto: SmartConnect API v1.0

---

**Fecha de Desarrollo:** Diciembre 2025  
**Institución:** INACAP - Ingeniería en Informática
