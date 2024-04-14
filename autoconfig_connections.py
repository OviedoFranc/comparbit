''' This file configure the name of port to be monitored for others, 
    configured on host file and the IP address of the device.'''
import os
import platform
import socket
import subprocess

def add_host_entry(ip, port):
    if platform.system() == 'Windows':
        # Obtengo la unidad en la que esta instalado Windows
        windows_drive_disk = os.environ.get('SystemDrive')
        hosts_path = os.path.join(windows_drive_disk, r'\Windows\System32\drivers\etc\hosts')
    elif platform.system() == 'Linux':
        hosts_path = '/etc/hosts'
    else:
        print("system not supported.")
        return
    
    # Agregar una nueva entrada al archivo hosts
    with open(hosts_path, 'r') as file:
        existing_hosts = file.read()
        if f"{ip} {port}" in existing_hosts:
            print("entry was already on to hosts file.")
        else:
            try:
                system = platform.system()
                if system == 'Linux':
                    subprocess.run(['sudo', 'bash', '-c', f'echo "{ip} {port}" >> /etc/hosts'])
                if system == 'Windows':
                    subprocess.run(['runas', '/user:Administrator', 'cmd', '/c', f'echo {ip} {port}>>{hosts_path}'], shell=True)
                    print("Host entry added successfully.")
            except (IOError,PermissionError):
                print("Host entry already exists.")

def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.error:
        return "Error getting IP address."