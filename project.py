from scapy.all import sniff, IP
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from collections import Counter
import logging
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import json
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_file):
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            logging.info("Configuración cargada desde el archivo.")
            return config
    else:
        logging.error("El archivo de configuración no existe.")
        exit(1)

def save_data_to_txt(packet_data, txt_file):
    with open(txt_file, 'w') as f:
        for packet in packet_data:
            f.write(f"Src IP: {packet['src_ip']}, Dst IP: {packet['dst_ip']}, Protocol: {packet['protocol']}, Size: {packet['size']} bytes\n")
    logging.info(f"Datos guardados en {txt_file}")

def plot_statistics():
    plt.figure(figsize=(14, 6))

    # Gráfico de Top 5 IPs de origen
    top_src_ips = src_ip_counter.most_common(5)
    src_ips, src_counts = zip(*top_src_ips)  

    plt.subplot(1, 2, 1)
    plt.bar(src_ips, src_counts, color='green')  
    plt.title('Top 5 Direcciones IP de Origen')
    plt.ylabel('Número de Paquetes')
    plt.xlabel('Direcciones IP')
    plt.xticks(rotation=45)
    plt.ylim(0, max(src_counts) + 1)  
    plt.grid(axis='y')

    # Gráfico de Top 5 IPs de destino
    top_dst_ips = dst_ip_counter.most_common(5)
    dst_ips, dst_counts = zip(*top_dst_ips) 

    plt.subplot(1, 2, 2)
    plt.bar(dst_ips, dst_counts, color='blue') 
    plt.title('Top 5 Direcciones IP de Destino')
    plt.ylabel('Número de Paquetes')
    plt.xlabel('Direcciones IP')
    plt.xticks(rotation=45)
    plt.ylim(0, max(dst_counts) + 1) 
    plt.grid(axis='y')

    plt.tight_layout()
    plt.show()

# Conexión a MongoDB
def connect_to_mongo(connection_string):
    try:
        client = MongoClient(connection_string)
        db = client['TestS3']
        packets_collection = db['packets']
        logging.info("Conectado a MongoDB con éxito.")
        return packets_collection
    except ConnectionFailure:
        logging.error("Error al conectar a MongoDB.")
        exit(1)

parser = argparse.ArgumentParser(description='Traffic Analyzer')
parser.add_argument('--config', type=str, default='config.json', help='Archivo de configuración JSON')
args = parser.parse_args()

config = load_config(args.config)
connection_string = config['mongodb_connection_string']
interface = config['network_interface']

packets_collection = connect_to_mongo(connection_string)

packet_count = 0
protocol_counter = Counter()
src_ip_counter = Counter()
dst_ip_counter = Counter()
packet_data = []

def packet_callback(packet):
    global packet_count
    if IP in packet:
        packet_count += 1
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = packet[IP].proto
        size = len(packet)
        
        # Verificación de calidad de datos
        if not src_ip or not dst_ip or proto is None or size <= 0:
            logging.warning("Datos del paquete incompletos, omitiendo.")
            return
        
        packet_info = {
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'protocol': proto,
            'size': size
        }


        try:
            packets_collection.insert_one(packet_info)
            packet_data.append(packet_info) 
            logging.info(f"Stored packet: {packet_info}")
        except DuplicateKeyError:
            logging.warning("Duplicate packet entry, skipping insert.")

        protocol_counter[proto] += 1
        src_ip_counter[src_ip] += 1
        dst_ip_counter[dst_ip] += 1

        if packet_count % 10 == 0:
            print_statistics()
            plot_statistics() 

def print_statistics():
    print(f"\nTotal de paquetes capturados: {packet_count}")
    print(f"Paquetes por protocolo: {protocol_counter}")
    print("Top 5 direcciones IP de origen:")
    for ip, count in src_ip_counter.most_common(5):
        print(f"{ip}: {count} paquetes")
    print("Top 5 direcciones IP de destino:")
    for ip, count in dst_ip_counter.most_common(5):
        print(f"{ip}: {count} paquetes")

    save_data_to_txt(packet_data, 'packets_data.txt')  
try:
    sniff(iface=interface, filter="ip", prn=packet_callback, store=0)
except PermissionError:
    logging.error(f"Permiso denegado. Asegúrate de que el contenedor tenga los permisos necesarios para capturar paquetes.")
except Exception as e:
    logging.error(f"Error en el proceso de sniffing: {e}")  
