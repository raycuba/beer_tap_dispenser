# Usamos una imagen ligera de Python
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc y fuerza el buffer de salida para ver los logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias para compilar ciertos paquetes de Python (como psycopg2 si aplica)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos e instalamos los requerimientos
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del backend
COPY . /app/

# Exponemos el puerto de Django
EXPOSE 8000

# Comando por defecto para arrancar la API
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]