# Análisis de Tráfico de Red

## Descripción del Proyecto
Este proyecto es una aplicación para el análisis de tráfico de red, diseñada para capturar paquetes desde una interfaz de red específica y mostrar estadísticas básicas. Utiliza Python junto con la biblioteca Scapy para la captura de paquetes, y se implementa en un contenedor Docker para facilitar su despliegue. Además, los datos capturados se almacenan en una base de datos MongoDB para su análisis posterior.

## Requisitos

### Funcionalidades Clave
1. **Captura de paquetes**:
    - Captura paquetes desde una interfaz de red específica.
    - Utiliza Scapy para la captura.
    - Captura los siguientes campos:
        - Dirección IP de origen
        - Dirección IP de destino
        - Protocolo
        - Tamaño del paquete

2. **Análisis de tráfico**:
    - Muestra estadísticas básicas sobre el tráfico capturado:
        - Número total de paquetes capturados.
        - Número de paquetes por protocolo (TCP, UDP, etc.).
        - Las 5 principales direcciones IP de origen con mayor tráfico.
        - Las 5 principales direcciones IP de destino con mayor tráfico.

3. **Almacenamiento de datos**:
    - Almacena los paquetes capturados en una base de datos MongoDB (opcional).

## Tecnologías Utilizadas
- **Python**: Lenguaje de programación para desarrollar la aplicación.
- **Scapy**: Biblioteca para captura y manipulación de paquetes de red.
- **MongoDB**: Base de datos NoSQL para almacenar los datos capturados.
- **Docker**: Plataforma para desarrollar, enviar y ejecutar aplicaciones en contenedores.
- **Wireshark**: Herramienta para la captura y análisis visual del tráfico de red.

## Configuración

### 1. Clonar el Repositorio
Clona el proyecto en tu máquina local:

git clone https://github.com/Ilvi1537/traffic-analyzer.git
cd traffic-analyzer

Si decides no clonar el repositorio, puedes seguir estos pasos alternativos para desarrollar el proyecto desde cero:

### 2. Crear el Archivo requirements.txt

Asegúrate de que tu archivo requirements.txt contenga las siguientes líneas:

txt
Copiar código
scapy
pymongo
### 3. Crear el Dockerfile
Crea un archivo Dockerfile en el directorio del proyecto con el siguiente contenido:

Dockerfile

- Usa una imagen base de Python
  
FROM python:3.9-slim

- Establece el directorio de trabajo
  
WORKDIR /app

- Copia el archivo de requerimientos y los instala
  
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

- Copia el resto de tu código al contenedor
  
COPY . ./

- Instala iproute2 para el comando 'ip'
  
RUN apt-get update && apt-get install -y iproute2

- Comando por defecto para ejecutar el script
  
CMD ["python", "project.py"]

### 4. Construir la Imagen de Docker
Desde el directorio donde se encuentra el Dockerfile, ejecuta el siguiente comando para construir la imagen de Docker:
docker build -t traffic-analyzer .

### 5. Iniciar MongoDB
Asegúrate de que el servicio esté funcionando. Puedes iniciarlo en una terminal:
mongod

## Ejecución de la Aplicación
Para ejecutar el analizador de tráfico, usa el siguiente comando. Asegúrate de que tu contenedor tenga los permisos necesarios para capturar paquetes y acceder a la red:
docker run --cap-add=NET_ADMIN --rm traffic-analyzer

## Uso de Wireshark

### Instalación de Wireshark
Descarga: Ve al sitio oficial de Wireshark y descarga la versión correspondiente a tu sistema operativo.
Instalación: Sigue las instrucciones para instalarlo en tu máquina.

### Captura de Tráfico
Abre Wireshark y selecciona la interfaz de red que deseas monitorear.
Haz clic en el botón de captura (ícono de tiburón).
Puedes aplicar filtros de visualización, como ip, para enfocarte en el tráfico IP.

## Conclusión
Este proyecto proporciona una forma efectiva de analizar el tráfico de red mediante la captura de paquetes y su almacenamiento en MongoDB. La implementación en Docker facilita el desarrollo y la ejecución de la aplicación. Wireshark complementa la funcionalidad al permitir un análisis visual del tráfico.
