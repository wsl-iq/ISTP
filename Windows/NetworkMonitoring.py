import psutil
import time
import json
import os
import sqlite3
import csv
from prettytable import PrettyTable

R = "\033[91;1m"  # Red
G = "\033[92;1m"  # Green
B = "\033[94;1m"  # Blue
Y = "\033[93;1m"  # Yellow
C = "\033[96;1m"  # Cyan
M = "\033[95;1m"  # Magenta
W = "\033[97;1m"  # White
D = "\033[90;1m"  # Grey
S = "\033[0m"     # Reset

def convert_bytes(num_bytes):
    if num_bytes < 1024:
        return f"{num_bytes} {B}B{W}"
    elif num_bytes < 1024 ** 2:
        return f"{num_bytes / 1024:.2f} {Y}KB{W}"
    elif num_bytes < 1024 ** 3:
        return f"{num_bytes / (1024 ** 2):.2f} {C}MB{W}"
    else:
        return f"{num_bytes / (1024 ** 3):.2f} {G}GB{W}"

def setup_database(db_name="network_traffic.db"):
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

def monitor_traffico(intervallo=1, json_filename="network_traffic.json", csv_filename="network_traffic.csv", db_name="network_traffic.db"):
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
        
        table = PrettyTable()
        table.field_names = [f"{Y}ID{W}", f"{B}Interfaccia{W}", f"{M}Inviati{W}", f"{G}Ricevuti{W}"]
        
        id_counter = 1
        
        for interfaccia, values in data.items():
            table.add_row([id_counter, M + interfaccia + W, convert_bytes(values['Inviati']), convert_bytes(values['Ricevuti'])])
            id_counter += 1
        
        print(table)
        
        save_to_database(conn, data)
        
        save_to_csv(csv_filename, data)
        
        time.sleep(intervallo)

monitor_traffico(1)
