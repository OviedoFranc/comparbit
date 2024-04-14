''' This file configure the name of port to be monitored for others, 
    configured on host file and the IP address of the device.'''
import fileinput
import os
import platform
import socket

def add_host_entry(host, ip):
    if platform.system() == 'Windows':
        # Obtengo la unidad en la que esta instalado Windows
        windows_drive_disk = os.environ.get('SystemDrive')
        hosts_path = os.path.join(windows_drive_disk, r'Windows\System32\drivers\etc\hosts')
    elif platform.system() == 'Linux':
        hosts_path = '/etc/hosts'
    else:
        print("No se pudo determinar el sistema operativo.")
        return
    
    # Agregar una nueva entrada al archivo hosts
    with fileinput.FileInput(hosts_path, inplace=True) as file:
        found = False
        for line in file:
            if host in line:
                found = True
                break
        if not found:
            print(f"{ip} {host}", end='\n', sep=' ')
            print("New entry added to hosts file.")
        else:
            print("Host entry already exists.")

def get_ip_address():
    # Obtenengo el nombre de host del sistema local
    hostname = socket.gethostname()
    # Obtenengo la dirección IP asociada al nombre de host
    ip_address = socket.gethostbyname(hostname)
    return ip_address

# Agrega la entrada de host personalizada
#DESCODE --- add_host_entry('comparbit', f"{get_ip_address()}:37596")
