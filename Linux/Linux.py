import subprocess
import re

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


print(f"{INFO} system is {W}: {B}Linux{W}")

def get_wifi_info():
    wifi_info = {}

    try:
        output = subprocess.check_output(['iwconfig'], encoding='utf-8', stderr=subprocess.STDOUT)
        interface_match = re.search(r'^(\w+)\s+IEEE 802.11', output, re.MULTILINE)
        if interface_match:
            interface_name = interface_match.group(1)
            wifi_info[f'{sign} Adapter name{W}'] = interface_name

            ssid_match = re.search(r'ESSID:"([^"]+)"', output)
            if ssid_match:
                wifi_info[f'{sign} SSID{W}'] = ssid_match.group(1)

            protocol_match = re.search(r'IEEE (\d+\.\d+)', output)
            if protocol_match:
                wifi_info[f'{sign} Protocol{W}'] = f"Wi-Fi {protocol_match.group(1)}"

            nmcli_output = subprocess.check_output(['nmcli', '-t', '-f', 'SECURITY,CHAN,FREQ,RATE,IP4,IP6,DNS4,DEV,SSID', 'device', 'wifi', 'list', 'ifname', interface_name], encoding='utf-8', stderr=subprocess.STDOUT)
            for line in nmcli_output.strip().split('\n'):
                fields = line.split(':')
                if len(fields) == 9:
                    wifi_info[f'{sign} Security type{W}'] = fields[0]
                    wifi_info[f'{sign} Network channel{W}'] = fields[1]
                    wifi_info[f'{sign} Network band{W}'] = fields[2]
                    wifi_info[f'{sign} Link speed (Receive/Transmit){W}'] = fields[3]
                    wifi_info[f'{sign} IPv4 address{W}'] = fields[4]
                    wifi_info[f'{sign} IPv6 address{W}'] = fields[5]
                    wifi_info[f'{sign} IPv4 DNS servers'] = fields[6]
                    wifi_info[f'{sign} Manufacturer{W}'] = 'N/A'
                    wifi_info[f'{sign} Description{W}'] = fields[7]
                    wifi_info[f'{sign} Driver version{W}'] = 'N/A'
                    wifi_info[f'vPhysical address (MAC){W}'] = 'N/A'
            if wifi_info:
                return wifi_info
    except subprocess.CalledProcessError as e:
        print(f"iwconfig/nmcli failed: {e}")

    try:
        output = subprocess.check_output(['iwlist', 'scan'], encoding='utf-8', stderr=subprocess.STDOUT)

        ssid_match = re.search(r'ESSID:"([^"]+)"', output)
        protocol_match = re.search(r'IE: IEEE (\d+\.\d+)', output)
        security_type_match = re.search(r'IE: WPA Version (\d)', output)
        network_band_match = re.search(r'Frequency:(\d+\.\d+) GHz', output)
        network_channel_match = re.search(r'Channel:(\d+)', output)
        link_speed_match = re.search(r'Bit Rates:(.+)', output)
        ipv4_match = re.search(r'inet addr:(\d+\.\d+\.\d+\.\d+)', output)
        ipv6_match = re.search(r'inet6 addr: ([\da-f:]+)', output)
        dns_servers_match = re.search(r'DNS Servers:\s*(.+)', output)
        mac_address_match = re.search(r'Address: ([\da-f:]+)', output)

        if ssid_match:
            wifi_info[f'{sign} SSID{W}'] = ssid_match.group(1).strip()
        if protocol_match:
            wifi_info[f'{sign} Protocol{W}'] = f"Wi-Fi {protocol_match.group(1).strip()}"
        if security_type_match:
            wifi_info[f'{sign} Security type{W}'] = f"WPA{security_type_match.group(1).strip()}"
        if network_band_match:
            wifi_info[f'{sign} Network band{W}'] = f"{network_band_match.group(1).strip()} GHz"
        if network_channel_match:
            wifi_info[f'{sign} Network channel{W}'] = network_channel_match.group(1).strip()
        if link_speed_match:
            wifi_info[f'{sign} Link speed (Receive/Transmit){W}'] = f"{link_speed_match.group(1).strip()} (Mbps)"
        if ipv4_match:
            wifi_info[f'{sign} IPv4 address{W}'] = ipv4_match.group(1).strip()
        if ipv6_match:
            wifi_info[f'{sign} IPv6 address{W}'] = ipv6_match.group(1).strip()
        if dns_servers_match:
            wifi_info[f'{sign} IPv4 DNS servers{W}'] = dns_servers_match.group(1).strip()
        if mac_address_match:
            wifi_info[f'{sign} Physical address (MAC){W}'] = mac_address_match.group(1).strip()

        if wifi_info:
            return wifi_info
    except subprocess.CalledProcessError as e:
        print(f"iwlist failed: {e}")

    try:
        output = subprocess.check_output(['ip', 'addr', 'show'], encoding='utf-8', stderr=subprocess.STDOUT)

        interface_match = re.search(r'^\d+: (\w+):.*state UP', output, re.MULTILINE)
        if interface_match:
            interface_name = interface_match.group(1)
            wifi_info[f'{sign} Adapter name{W}'] = interface_name

            ssid_match = re.search(r'^\s+link/ether ([\da-f:]+)', output, re.MULTILINE)
            if ssid_match:
                wifi_info[f'{sign} Physical address (MAC){W}'] = ssid_match.group(1)

            ipv4_match = re.search(r'^\s+inet (\d+\.\d+\.\d+\.\d+)', output, re.MULTILINE)
            if ipv4_match:
                wifi_info[f'{sign} IPv4 address{W}'] = ipv4_match.group(1)

            ipv6_match = re.search(r'^\s+inet6 ([\da-f:]+)', output, re.MULTILINE)
            if ipv6_match:
                wifi_info[f'{sign} IPv6 address{W}'] = ipv6_match.group(1)

        if wifi_info:
            return wifi_info
    except subprocess.CalledProcessError as e:
        print(f"ip addr show failed: {e}")

    try:
        output = subprocess.check_output(['ifconfig'], encoding='utf-8', stderr=subprocess.STDOUT)

        interface_match = re.search(r'^(\w+):\s+flags=.*mtu', output, re.MULTILINE)
        if interface_match:
            interface_name = interface_match.group(1)
            wifi_info[f'{sign} Adapter name{W}'] = interface_name

            ssid_match = re.search(r'^\s+ether ([\da-f:]+)', output, re.MULTILINE)
            if ssid_match:
                wifi_info[f'{sign} Physical address (MAC){W}'] = ssid_match.group(1)

            ipv4_match = re.search(r'^\s+inet (\d+\.\d+\.\d+\.\d+)', output, re.MULTILINE)
            if ipv4_match:
                wifi_info[f'{sign} IPv4 address{W}'] = ipv4_match.group(1)

            ipv6_match = re.search(r'^\s+inet6 ([\da-f:]+)', output, re.MULTILINE)
            if ipv6_match:
                wifi_info[f'{sign} IPv6 address{W}'] = ipv6_match.group(1)

        if wifi_info:
            return wifi_info
    except subprocess.CalledProcessError as e:
        return {"Error": f"ifconfig failed: {e}"}

    return {"Error": "Failed to retrieve WiFi information"}

wifi_info = get_wifi_info()
for key, value in wifi_info.items():
    print(f"{key}: {value}")
