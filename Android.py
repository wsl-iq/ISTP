import sys
import os
import time
import datetime
import speedtest
import requests
from time import sleep
from tqdm import tqdm
from colorama import Back, init
from termcolor import colored
from prettytable import PrettyTable
import threading

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

now = datetime.datetime.now()
formatted_time = now.strftime("%I:%M %p")
formatted_day = now.strftime("%A")

date_day = "\033[94;1m" + "[" + "\033[92;1m" + "Today" + "\033[94;1m" + "]" + "\033[97;1m" + "(" + "\033[93;1m" + formatted_day + "\033[95;1m" + f" {now:%B %D %Y}" + "\033[97;1m" + ")" + "\033[94;1m" + "[" + "\033[92;1m" + "Time" + "\033[94;1m" + "]" + "\033[93;1m" + "[" + "\033[91;1m" + formatted_time + "\033[93;1m" + "]" + "\033[97;1m"

os.system('cls' if os.name == 'nt' else 'clear')

def spin():
    delay = 0.25
    spinner = ['█■■■■', '■█■■■', '■■█■■', '■■■█■', '■■■■█']

    for _ in range(1):
        for i in spinner:
            message = f"[*] {B}Checking your internet connection...[{i}]{W}"
            colored_message = colored(message, 'blue', attrs=['bold'])
            sys.stdout.write(f"\r{colored_message}   ")
            sys.stdout.flush()
            time.sleep(delay)

    sys.stdout.write("\r")
    sys.stdout.flush()
    done_message = colored("[+] Your Internet connection has been verified", 'yellow', attrs=['bold'])
    sys.stdout.write("\033[K")
    print(done_message)
    time.sleep(1)

spin()

def check_internet_connection():
    try:
        response = requests.get('http://www.google.com', timeout=5)
        return True
    except requests.ConnectionError:
        return False

if check_internet_connection():
    print(f"{sign} Internet connection is available. You can proceed with execution.{W}")
    time.sleep(0.25)
else:
    print(f"{please} No internet connection !{W}")
    exit()
os.system('cls' if os.name == 'nt' else 'clear')
print(f"""
      {G}\ | /{W}                                                     
     {B}-- {R}O{B} --{W}                                                    
       {G}/|\       {B} ___  ____________________________{W}             
      {G}/\|/\      {B}|   |/   _____/__    ___/______   \{W}            
     {G}/  |  \     {B}|   |\_____  \  |    |   |     ___/{W}            
    {G}/\/\|/\/\    {B}|   |/        \ |    |   |    |{W}                
   {G}/    |    \   {B}|___|_______  / |____|   |____| {Y}Version : 6{W}
  -     -     -        {B}      \/{W}                  {Y}My INSTAGRAM {W}: {M}wsl.iq{W}          
 {Back.RED}{W} [Internet Speed Test Ping] {S}{W}
""")
print(f"{INFO} system is: {G}Android{W}")
print(f"{INFO} application: {G}Termux{W}")
input(f"{Enter} {Help}{W}")
init(autoreset=True)
print(f"{sign} {Y}Downloading to servers and information at internet speed.{W}")

def show_loading():
    spinner = [f'{R}-{W}', f'{G}\\{W}', f'{B}|{W}', f'{Y}/{W}']
    index = 0
    while not stop_loading:
        print(f"{sign}{W} Please waiting {spinner[index]}", end='\r', flush=True)
        index = (index + 1) % len(spinner)
        time.sleep(0.2)

def main_task():
    global stop_loading
    stop_loading = False
    loading_thread = threading.Thread(target=show_loading)
    loading_thread.start()

    st = speedtest.Speedtest()
    st.get_best_server()
    stop_loading = True
    loading_thread.join()
    
    sys.stdout.write("\r\033[K")
    print(date_day)
    for _ in tqdm(range(10), colour="green", desc=f"{INFO} Finding  Optimal  Server"):
        sleep(0.05)

    st.download()
    for _ in tqdm(range(10), colour="yellow", desc=f"{INFO} Getting {W}[{Y}Download{W}] {M}Speed"):
        sleep(0.05)

    st.upload()
    for _ in tqdm(range(10), colour="red", desc=f"{INFO} Getting  {W}[{Y}Upload{W}] {M} Speed"):
        sleep(0.05)

    res_dict = st.results.dict()

    dwnl = f"{res_dict['download'] / 10**6:.2f}"
    upl = f"{res_dict['upload'] / 10**6:.2f}"
    print("                                  ")
    table = PrettyTable()

    table.field_names = [f"{M}ID{W}", f"{B}INFORMATION{W}", f"{R}Information results{W}"]

    table.add_row([f"{G}1{W}", f"{Y}Download{W}", f"{B}{dwnl} {M}Mbps{W} ({B}{float(dwnl) * 0.125:.2f} {G}MB/s{W})"])
    table.add_row([f"{G}2{W}", f"{Y}Upload{W}", f"{B}{upl} {M}Mbps{W} ({B}{float(upl) * 0.125:.2f} {G}MB/s{W})"])
    table.add_row([f"{G}3{W}", f"{Y}Ping{W}", f"{B}{res_dict['ping']:.2f} {G}ms{W}"])
    table.add_row([f"{G}4{W}", f"{Y}HOST{W}", res_dict['server']['host']])
    table.add_row([f"{G}5{W}", f"{Y}SPONSOR{W}", res_dict['server']['sponsor']])
    table.add_row([f"{G}6{W}", f"{Y}ISP{W}", res_dict['client']['isp']])
    table.add_row([f"{G}7{W}", f"{Y}Country{W}", res_dict['client']['country']])
    table.add_row([f"{G}8{W}", f"{Y}URL{W}", st.results.share()])
    table.add_row([f"{G}9{W}", f"{Y}Hosted By{W}", res_dict['server']['host']])
    packet_loss = res_dict.get('packetLoss', 'N/A')
    table.add_row([f"{G}10{W}", f"{Y}Packet Loss{W}", f"{B}{packet_loss}%{W}"])
    table.add_row([f"{G}11{W}", f"{Y}Server ID{W}", res_dict['server']['id']])
    table.add_row([f"{G}12{W}", f"{Y}ISP Rating{W}", res_dict['client']['isprating']])

    for field in table.field_names:
        table.align[field] = "l"
    print(table)

    now = datetime.datetime.now()
    formatted_time = now.strftime("%I:%M %p")
    formatted_day = now.strftime("%A")
    print(f"{B}[{G}Today{B}] {W}({Y}{formatted_day}{W} {M}{now:%B %D %Y}{W}) {B}[{G}Time{B}] {Y}[{R}{formatted_time}{Y}]{W}")

main_task()
