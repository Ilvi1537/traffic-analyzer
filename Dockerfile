# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y iproute2 libpcap-dev && \
    rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos y los instala
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu código al contenedor
COPY . .

# Comando por defecto para ejecutar el script
CMD ["python", "project.py"]

