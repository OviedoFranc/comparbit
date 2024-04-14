'''This component have to question all devices on network if have a port to conect to it
    and if have a port, it will be added to the list of devices to be monitored. '''

# In next version, will we use UDP not TCP

import socket
import asyncio
from all_devices import get_all_devices

connections_established = []

async def connect_to_device(device):
    try:
        # Crear un objeto socket
        reader, writer = await asyncio.open_connection(device['LAN_IP'], 37596)
        # Agregar la conexión establecida a la lista
        connections_established.append(device)
        print(f"Conexión establecida con {device['LAN_IP']}")
        writer.close()
        await writer.wait_closed()
    except ConnectionRefusedError:
        print(f"No se pudo conectar a {device['LAN_IP']}: El dispositivo rechazó la conexión.")
    except TimeoutError:
        print(f"No se pudo conectar a {device['LAN_IP']}: Tiempo de espera de conexión agotado.")
    except OSError as e:
        print(f"No se pudo conectar a {device['LAN_IP']}: {e.strerror}")

async def connect_to_others():
    devices = get_all_devices()
    connections = await asyncio.gather(*[connect_to_device(device) for device in devices if device])
    connections_established.extend(connections) 

# Ejecuta la función connect_to_others en un bucle de eventos asyncio 
asyncio.run(connect_to_others())