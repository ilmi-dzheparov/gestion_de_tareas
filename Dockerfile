FROM python:3.11-slim

# Configuraciones de Python para optimizar la salida de logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalación de las dependencias del sistema y del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalación explícita del servidor HTTP WSGI Gunicorn para producción
RUN pip install gunicorn

# Copia de todo el código fuente del proyecto al contenedor
COPY . .

# Exposición informativa del puerto interno del contenedor
EXPOSE 8000

# Comando de ejecución principal acoplado a la variable de entorno de Render
CMD gunicorn --bind 0.0.0.0:$PORT studentsync.wsgi:application