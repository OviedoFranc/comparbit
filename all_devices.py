''' This file gives you the list of all devices connected to your network.'''
import os
import re
import platform
import subprocess

def is_arp_installed():
    system = platform.system()
    if system == 'Linux':
        try:
            # Ejecutar 'which arp' para obtener la ubicación del comando arp
            subprocess.run(['which', 'arp'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True 
        except subprocess.CalledProcessError:
            return False 
    elif system == 'Windows':    
        # Dividir las rutas en la variable de entorno PATH
        paths = os.environ['PATH'].split(os.pathsep)
    
        # Verificar si 'arp.exe' está en alguna de las rutas
        for path in paths:
            arp_path = os.path.join(path, 'arp.exe')
            if os.path.exists(arp_path):
                return True      
    return False

def install_arp():
    
    # Verificar si arp está instalado
    if(not is_arp_installed()):
        print("ARP no está instalado en el sistema.")
        system = platform.system()
        if system == 'Linux':
            # Instalar arp en sistemas basados en Debian
            os.system('sudo apt-get install -y net-tools')
        if system == 'Windows':
            try:
                # Instalar arp en sistemas Windows
                os.system('choco install -y microsoft-windows-net* --includeRecommended')
            except:
                print('''ARP no está instalado en Windows.
                Por favor, instale las herramientas de red de Microsoft que incluyen ARP.
                Puede descargarlas desde el siguiente enlace:
                https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/netsh#BKMK_1''')
        else:
            print(f"No se puede instalar arp en {system}.")

# Intentar instalar arp
# DESCODE ---- install_arp()

def get_all_devices():
    print('RASTREANDO TODOS LOS DISPOSITIVOS EN LA RED LOCAL...')
    full_results = [re.findall('^[\w\?\.]+|(?<=\s)\([\d\.]+\)|(?<=at\s)[\w\:]+', i) for i in os.popen('arp -a')]
    final_results = [dict(zip(['IP', 'LAN_IP', 'MAC_ADDRESS'], i)) for i in full_results]
    final = [{**i, **{'LAN_IP':i['LAN_IP'][1:-1]}} for i in final_results]
    return final