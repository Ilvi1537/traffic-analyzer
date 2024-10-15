from scapy.all import sniff, IP
from pymongo import MongoClient
from collections import Counter

client = MongoClient("mongodb+srv://ilsemartineziquo:CTbav5gCTJIA5B17@cluster0.np6aigt.mongodb.net/")
db = client['TestS3']
packets_collection = db['packets']

packet_count = 0
protocol_counter = Counter()
src_ip_counter = Counter()
dst_ip_counter = Counter()

def packet_callback(packet):
    global packet_count
    if IP in packet:
        packet_count += 1
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        proto = packet[IP].proto
        size = len(packet)
        
        packet_data = {
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'protocol': proto,
            'size': size
        }
        packets_collection.insert_one(packet_data)

        protocol_counter[proto] += 1
        src_ip_counter[src_ip] += 1
        dst_ip_counter[dst_ip] += 1

        print(f"Stored packet: {packet_data}")

        if packet_count % 10 == 0:
            print_statistics()

def print_statistics():
    print(f"\nTotal de paquetes capturados: {packet_count}")
    print(f"Paquetes por protocolo: {protocol_counter}")
    print("Top 5 direcciones IP de origen:")
    for ip, count in src_ip_counter.most_common(5):
        print(f"{ip}: {count} paquetes")
    print("Top 5 direcciones IP de destino:")
    for ip, count in dst_ip_counter.most_common(5):
        print(f"{ip}: {count} paquetes")

# Reemplaza 'Wi-Fi' con 'eth0'
sniff(iface="eth0", filter="ip", prn=packet_callback, store=0)

