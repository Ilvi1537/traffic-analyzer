# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema y limpia la caché de apt
RUN apt-get update && \
    apt-get install -y iproute2 libpcap-dev libgtk-3-0 libnotify-dev libgstreamer1.0-0 libgstreamer-plugins-base1.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos y los instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu código al contenedor
COPY . .

# Comando por defecto para ejecutar el script
CMD ["python", "project.py", "--config", "config.json"]
