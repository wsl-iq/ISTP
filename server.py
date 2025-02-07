import http.server
import socketserver
import webbrowser
import datetime
import time
import threading
import os

R = "\033[91;1m"  # Red
G = "\033[92;1m"  # Green
B = "\033[94;1m"  # Blue
Y = "\033[93;1m"  # Yellow
C = "\033[96;1m"  # Cyan
M = "\033[95;1m"  # Magenta
W = "\033[97;1m"  # White
D = "\033[90;1m"  # Grey
S = "\033[0m"     # Rest

ERROR = "\033[93;1m" + "[" + "\033[91;1m" + "ERROR" + "\033[93;1m" + "]" + "\033[91;1m"
INFO = "\033[93;1m" + "[" + "\033[92;1m" + "INFO" + "\033[93;1m" + "]" + "\033[94;1m"
please = "\033[93;1m" + "[" + "\033[91;1m" + "!" + "\033[93;1m" + "]" + "\033[91;1m"

now = datetime.datetime.now()
formatted_time = now.strftime("%I:%M %p")
formatted_day = now.strftime("%A")

date_day = "\033[94;1m" + "[" + "\033[92;1m" + "Today" + "\033[94;1m" + "]" + "\033[97;1m" + "(" + "\033[93;1m" + formatted_day + "\033[95;1m" + f" {now:%B %D %Y}" + "\033[97;1m" + ")" + "\033[94;1m" + "[" + "\033[92;1m" + "Time" + "\033[94;1m" + "]" + "\033[93;1m" + "[" + "\033[91;1m" + formatted_time + "\033[93;1m" + "]" + "\033[97;1m"


def Banner():
    operating_system = os.name
    try:
        if (operating_system == 'posix'):
            os.system('clear')
        elif (operating_system == 'nt'):
            os.system('cls')
        else:
            print(f"{please} System unknown!{S}")
    except Exception as e:
        print(f"{ERROR}{W}: {e}")

    print(rf"""{Y}
 __            ___              
|__| ____   __| _/ ____ ___  ___
|  |/    \ / __ |_/ __ \\  \/  /
|  |   |  \ /_/ |\  ___/_\    / 
|__|___|  /____ | \___  /__/\_ \
        \/     \/     \/      \/
          
{date_day}
{Y}""")
    
Banner()

Localhost = '127.0.0.1'
Port = 8000

def slowprint(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)

slowprint(f"{B}$ {G}index.html{W}\r\n")

FILENAME = "index.html"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = FILENAME
        return super().do_GET()

os.chdir('server')

handler_object = CustomHTTPRequestHandler

def run_server():
    with socketserver.TCPServer(("", Port), handler_object) as httpd:
        print(f"{INFO} Serving at port {G}{Port}{W}")
        httpd.serve_forever()

print(f'{B}$ {G}http://{Localhost}{W}:{Y}{Port}{W}')

def open_browser():
    webbrowser.open(f"http://localhost:{Port}")

server_thread = threading.Thread(target=run_server)
server_thread.start()

open_browser()
