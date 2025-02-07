import wmi
import subprocess
import re
import os 

R = "\033[91;1m"  # Red
G = "\033[92;1m"  # Green
B = "\033[94;1m"  # Blue
Y = "\033[93;1m"  # Yellow
C = "\033[96;1m"  # Cyan
M = "\033[95;1m"  # Magenta
W = "\033[97;1m"  # White
D = "\033[90;1m"  # Grey
S = "\033[0m"     # Reset

sign = "\033[92;1m" + "[" + "\033[94;1m" + "*" + "\033[92;1m" + "]" + "\033[94;1m"
Enter = "\033[94;1m" + "[" + "\033[92;1m" + "+" + "\033[94;1m" + "]" + "\033[92;1m"
ERROR = "\033[93;1m" + "[" + "\033[91;1m" + "ERROR" + "\033[93;1m" + "]" + "\033[91;1m"
INFO = "\033[93;1m" + "[" + "\033[92;1m" + "INFO" + "\033[93;1m" + "]" + "\033[94;1m"
warning = "\033[93;1m" + "[" + "\033[91;1m" + "WARNING" + "\033[93;1m" + "]" + "\033[91;1m"
Complete = "\033[94;1m" + "[" + "\033[92;1m" + "COMPLETE" + "\033[94;1m" + "]" + "\033[92;1m"
Failed = "\033[93;1m" + "[" + "\033[91;1m" + "FAILED" + "\033[93;1m" + "]" + "\033[91;1m"
please = "\033[93;1m" + "[" + "\033[91;1m" + "!" + "\033[93;1m" + "]" + "\033[91;1m"
Question = "\033[95;1m" + "[" + "\033[96;1m" + "?" + "\033[95;1m" + "]" + "\033[97;1m"
Help = "\033[97;1m" + "To continue anyway press or click" + "\033[94;1m" + " [" + "\033[92;1m" + "Enter" + "\033[94;1m" + "] " + "\033[97;1m" + "and to stop or exit" + "\033[93;1m" + " [" + "Ctrl" + "\033[97;1m" + " + " + "\033[93;1m" + "C" + "]" + "\033[0m"

print(f"{INFO} system is {W}: {B}Windows{W}")

def get_wifi_info():
    wifi_info = {}
    
    try:
        c = wmi.WMI()
        for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=True):
            if interface.Description.lower().find('wireless') != -1:
                wifi_info[f'{sign} Adapter name{W}'] = interface.Description
                wifi_info[f'{sign} SSID{W}'] = interface.SettingID
                wifi_info[f'{sign} Connection type{W}'] = f'{Y}N/A{W}'
                wifi_info[f'{sign} IPv4 address{W}'] = interface.IPAddress[0]
                if len(interface.IPAddress) > 1:
                    wifi_info[f'{sign} IPv6 address{W}'] = interface.IPAddress[1]
                else:
                    wifi_info[f'{sign} IPv6 address{W}'] = f'{Y}N/A{W}'
                wifi_info[f'{sign} Manufacturer{W}'] = f'{Y}N/A{W}'
                wifi_info[f'{sign} Description{W}'] = interface.Description
                wifi_info[f'{sign} Driver version{W}'] = f'{Y}N/A{W}'
                wifi_info[f'{sign} Physical address (MAC){W}'] = interface.MACAddress

                netsh_output = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'], encoding='utf-8')
                ssid_match = re.search(r'^\s*SSID\s*:\s*(.+)\s*$', netsh_output, re.MULTILINE)
                if ssid_match:
                    wifi_info[f'{sign} SSID{W}'] = ssid_match.group(1).strip()

                netsh_output = subprocess.check_output(['netsh', 'wlan', 'show', 'network', 'mode=bssid'], encoding='utf-8')
                protocol_match = re.search(r'^\s*Protocol\s*:\s*(.+)\s*$', netsh_output, re.MULTILINE)
                security_type_match = re.search(r'^\s*Authentication\s*:\s*(.+)\s*$', netsh_output, re.MULTILINE)
                network_band_match = re.search(r'^\s*Radio type\s*:\s*(.+)\s*$', netsh_output, re.MULTILINE)
                network_channel_match = re.search(r'^\s*Channel\s*:\s*(.+)\s*$', netsh_output, re.MULTILINE)
                link_speed_match = re.search(r'^\s*Receive rate\s*:\s*(.+)\s*$', netsh_output, re.MULTILINE)
                transmit_speed_match = re.search(r'^\s*Transmit rate\s*:\s*(.+)\s*$', netsh_output, re.MULTILINE)
                ipv4_dns_servers_match = re.search(r'^\s*DNS Servers\s*:\s*(.+)\s*$', netsh_output, re.MULTILINE)
                
                if protocol_match:
                    wifi_info[f'{sign} Protocol{W}'] = protocol_match.group(1).strip()
                if security_type_match:
                    wifi_info[f'{sign} Security type{W}'] = security_type_match.group(1).strip()
                if network_band_match:
                    wifi_info[f'{sign} Network band{W}'] = network_band_match.group(1).strip()
                if network_channel_match:
                    wifi_info[f'{sign} Network channel{W}'] = network_channel_match.group(1).strip()
                if link_speed_match and transmit_speed_match:
                    wifi_info[f'{sign} Link speed (Receive/Transmit){W}'] = f"{link_speed_match.group(1).strip()}/{transmit_speed_match.group(1).strip()} (Mbps)"
                if ipv4_dns_servers_match:
                    wifi_info[f'{sign} IPv4 DNS servers{W}'] = ipv4_dns_servers_match.group(1).strip()
                
                return wifi_info
    except Exception as e:
        pass
    
    try:
        output = subprocess.check_output(['netsh', 'wlan', 'show', 'network', 'mode=bssid'], encoding='utf-8')

        ssid_match = re.search(r'^\s*SSID\s*:\s*(.+)\s*$', output, re.MULTILINE)
        protocol_match = re.search(r'^\s*Protocol\s*:\s*(.+)\s*$', output, re.MULTILINE)
        security_type_match = re.search(r'^\s*Authentication\s*:\s*(.+)\s*$', output, re.MULTILINE)
        network_band_match = re.search(r'^\s*Radio type\s*:\s*(.+)\s*$', output, re.MULTILINE)
        network_channel_match = re.search(r'^\s*Channel\s*:\s*(.+)\s*$', output, re.MULTILINE)
        link_speed_match = re.search(r'^\s*Receive rate\s*:\s*(.+)\s*$', output, re.MULTILINE)
        transmit_speed_match = re.search(r'^\s*Transmit rate\s*:\s*(.+)\s*$', output, re.MULTILINE)
        link_local_ipv6_match = re.search(r'^\s*IPv6 Address\s*:\s*(.+)\s*$', output, re.MULTILINE)
        ipv4_match = re.search(r'^\s*IPv4 Address\s*:\s*(.+)\s*$', output, re.MULTILINE)
        ipv4_dns_servers_match = re.search(r'^\s*DNS Servers\s*:\s*(.+)\s*$', output, re.MULTILINE)
        manufacturer_match = re.search(r'^\s*Vendor\s*:\s*(.+)\s*$', output, re.MULTILINE)
        description_match = re.search(r'^\s*Description\s*:\s*(.+)\s*$', output, re.MULTILINE)
        driver_version_match = re.search(r'^\s*Driver version\s*:\s*(.+)\s*$', output, re.MULTILINE)
        mac_address_match = re.search(r'^\s*Physical address\s*:\s*(.+)\s*$', output, re.MULTILINE)

        if ssid_match:
            wifi_info[f'{sign} SSID{W}'] = ssid_match.group(1).strip()
        if protocol_match:
            wifi_info[f'{sign} Protocol{W}'] = protocol_match.group(1).strip()
        if security_type_match:
            wifi_info[f'{sign} Security type{W}'] = security_type_match.group(1).strip()
        if network_band_match:
            wifi_info[f'{sign} Network band{W}'] = network_band_match.group(1).strip()
        if network_channel_match:
            wifi_info[f'{sign} Network channel{W}'] = network_channel_match.group(1).strip()
        if link_speed_match and transmit_speed_match:
            wifi_info[f'{sign} Link speed (Receive/Transmit){W}'] = f"{link_speed_match.group(1).strip()}/{transmit_speed_match.group(1).strip()} (Mbps)"
        if link_local_ipv6_match:
            wifi_info[f'{sign} Link-local IPv6 address{W}'] = link_local_ipv6_match.group(1).strip()
        if ipv4_match:
            wifi_info[f'{sign} IPv4 address{W}'] = ipv4_match.group(1).strip()
        if ipv4_dns_servers_match:
            wifi_info[f'{sign} IPv4 DNS servers{W}'] = ipv4_dns_servers_match.group(1).strip()
        if manufacturer_match:
            wifi_info[f'{sign} Manufacturer{W}'] = manufacturer_match.group(1).strip()
        if description_match:
            wifi_info[f'{sign} Description{W}'] = description_match.group(1).strip()
        if driver_version_match:
            wifi_info[f'{sign} Driver version{W}'] = driver_version_match.group(1).strip()
        if mac_address_match:
            wifi_info[f'{sign} Physical address (MAC){W}'] = mac_address_match.group(1).strip()
        
        return wifi_info
    except subprocess.CalledProcessError:
        return {"Error": "Failed to retrieve WiFi information"}

wifi_info = get_wifi_info()
for key, value in wifi_info.items():
    print(f"{key}: {value}")
