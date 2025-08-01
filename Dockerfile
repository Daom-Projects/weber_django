# Dockerfile

# ---- Fase 1: La Base ----
# Usamos una imagen oficial de Python. La etiqueta 'slim' es más ligera.
FROM python:3.13-slim-bullseye

# Establecemos variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ---- Fase 2: Instalación de Dependencias ----
# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# --- PASO NUEVO Y CRUCIAL: Instalar dependencias del sistema operativo ---
# Actualizamos la lista de paquetes e instalamos las herramientas de compilación
# y las librerías de desarrollo de MariaDB (compatible con MySQL).
RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

# Primero, instalamos uv usando pip. Es la única vez que usaremos pip.
RUN pip install uv

# Copiamos primero el archivo de requerimientos
# Esto aprovecha el caché de Docker: si este archivo no cambia, no se reinstalan las dependencias.
COPY requirements.txt .

# Usamos 'uv pip install' que es mucho más rápido.
# --system: Instala los paquetes en el entorno global de Python del contenedor,
# lo cual es la práctica estándar dentro de Docker.
RUN uv pip install --system --no-cache -r requirements.txt

# ---- Fase 3: Copiar el Código de la Aplicación ----
# Copiamos todo el contenido del directorio actual ('.') al directorio de trabajo del contenedor ('/app')
COPY . .

# ---- Fase 4: Exponer el Puerto ----
# Le informamos a Docker que nuestra aplicación escuchará en el puerto 8000
EXPOSE 8000

# NOTA: El comando para iniciar la aplicación (CMD) lo definiremos más adelante en docker-compose.
# Esto nos da más flexibilidad.