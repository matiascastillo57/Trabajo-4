#!/bin/bash
pkill -f 'gunicorn.*config.wsgi'
echo "🛑 Gunicorn detenido"

