#!/usr/bin/env python3

import subprocess
import psutil
import json
import os
import sqlite3
import csv
import time
from prettytable import PrettyTable
import netifaces

R = "\033[91;1m"  # Red
G = "\033[92;1m"  # Green
B = "\033[94;1m"  # Blue
Y = "\033[93;1m"  # Yellow
M = "\033[95;1m"  # Magenta
W = "\033[97;1m"  # White
D = "\033[90;1m"  # Grey
S = "\033[0m"     # Reset

def convert_bytes(num_bytes):
    if num_bytes < 1024:
        return f"{num_bytes} {R}B{W}"
    elif num_bytes < 1024 ** 2:
        return f"{num_bytes / 1024:.2f} {M}KB{W}"
    elif num_bytes < 1024 ** 3:
        return f"{num_bytes / (1024 ** 2):.2f} {Y}MB{W}"
    else:
        return f"{num_bytes / (1024 ** 3):.2f} {B}GB{W}"

def setup_database(db_name="monitoring.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS traffic (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        interface TEXT,
        bytes_sent INTEGER,
        bytes_recv INTEGER
    )
    ''')
    conn.commit()
    return conn

def save_to_database(conn, data):
    cursor = conn.cursor()
    for interface, values in data.items():
        cursor.execute('''
        INSERT INTO traffic (interface, bytes_sent, bytes_recv)
        VALUES (?, ?, ?)
        ''', (interface, values['Inviati'], values['Ricevuti']))
    conn.commit()

def save_to_csv(filename, data):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as csv_file:
        fieldnames = ['timestamp', 'interface', 'bytes_sent', 'bytes_recv']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for interface, values in data.items():
            writer.writerow({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'interface': interface,
                'bytes_sent': values['Inviati'],
                'bytes_recv': values['Ricevuti']
            })

def monitor_traffico(intervallo=1, json_filename="monitoring.json", csv_filename="monitoring.csv", db_name="monitoring.db"):
    conn = setup_database(db_name)
    
    while True:
        stats_iniziali = psutil.net_io_counters(pernic=True)
        time.sleep(intervallo)
        stats_finali = psutil.net_io_counters(pernic=True)
        data = {}

        for interfaccia, stats in stats_finali.items():
            bytes_inviati = stats.bytes_sent - stats_iniziali[interfaccia].bytes_sent
            bytes_ricevuti = stats.bytes_recv - stats_iniziali[interfaccia].bytes_recv
            data[interfaccia] = {
                'Inviati': bytes_inviati,
                'Ricevuti': bytes_ricevuti
            }

        with open(json_filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        os.system('cls' if os.name == 'nt' else 'clear')
        
        table_network = get_network_info()
        
        table_traffic = PrettyTable()
        table_traffic.field_names = [f"{B}ID{W}", f"{G}Interfaccia{W}", f"{Y}Inviati{W}", f"{M}Ricevuti{W}"]
        
        id_counter = 1
        
        for interfaccia, values in data.items():
            table_traffic.add_row([id_counter, B + interfaccia + W, convert_bytes(values['Inviati']), convert_bytes(values['Ricevuti'])])
            id_counter += 1
        
        print("Traffic information:")
        print(table_traffic)
        
        print("\nNetwork information:")
        print(table_network)
        
        save_to_database(conn, data)
        
        save_to_csv(csv_filename, data)
        
        time.sleep(intervallo)

def get_signal_strength(interface):
    try:
        cmd = f"iwconfig {interface}"
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        for line in output.splitlines():
            if "Signal level" in line:
                return line.strip().split("=")[1].split()[0]
    except subprocess.CalledProcessError:
        return "-"

def get_network_info():
    interfaces = netifaces.interfaces()
    table = PrettyTable()
    table.field_names = [f"{B}Adapter name{W}", f"{Y}IPv4 address{W}", f"{Y}IPv6 address{W}", f"{Y}MAC address{W}", f"{G}Network name (SSID){W}", f"{G}Signal strength{W}"]

    for interface in interfaces:
        if interface.startswith('eth') or interface.startswith('wlan'):
            ipv4_address = "-"
            ipv6_address = "-"
            mac_address = "-"
            ssid = "-"
            signal_strength = "-"

            ipv4_addresses = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
            if ipv4_addresses:
                ipv4_address = ipv4_addresses[0]['addr']
            
            ipv6_addresses = netifaces.ifaddresses(interface).get(netifaces.AF_INET6)
            if ipv6_addresses:
                ipv6_address = ipv6_addresses[0]['addr']

            mac_addresses = netifaces.ifaddresses(interface).get(netifaces.AF_LINK)
            if mac_addresses:
                mac_address = mac_addresses[0]['addr']

            if interface.startswith('wlan'):
                signal_strength = get_signal_strength(interface)

            table.add_row([B + interface + W, ipv4_address, ipv6_address, mac_address, G + ssid + W, G + str(signal_strength) + "%" + W])

    return table

if __name__ == "__main__":
    monitor_traffico()
