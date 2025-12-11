#!/bin/bash

# Activar entorno virtual
source /home/ec2-user/smartconnect/venv/bin/activate

# Ir al directorio del proyecto
cd /home/ec2-user/smartconnect

# Iniciar Gunicorn
gunicorn config.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile /home/ec2-user/smartconnect/gunicorn-access.log \
    --error-logfile /home/ec2-user/smartconnect/gunicorn-error.log \
    --daemon

echo "✅ Gunicorn iniciado en 127.0.0.1:8000"
