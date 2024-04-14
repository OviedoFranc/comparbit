'''This component have to question all devices on network if have a port to conect to it
    and if have a port, it will be added to the list of devices to be monitored. '''

import socket
import asyncio
from all_devices import get_all_devices

connections_established = []

def open_listening_socket(local_address, port):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', port))
    print(f"Socket listening on {local_address}:{port}")

    while True:
        data, address = udp_socket.recvfrom(1024)
        print(f"Recived -> {data} from {address}")

async def connect_to_device(device):
    try:
        # Crea un objeto socket UDP
        transport, protocol = await asyncio.create_datagram_endpoint(
            lambda: asyncio.DatagramProtocol(),
            remote_addr=(device['LAN_IP'], 37596)
        )
        # Agrega la conexión establecida a la lista
        connections_established.append(device)
        print(f"Connection entablished with {device['LAN_IP']}")
    except ConnectionRefusedError:
        print(f"Error could not connect to {device['LAN_IP']}: Device refushed the connection.")
    except TimeoutError:
        print(f"Error could not connect to {device['LAN_IP']}: Time out.")
    except OSError as e:
        print(f"Error could not connect to {device['LAN_IP']}: {e.strerror}")

async def close_connections():
    for device, transport in connections_established:
        try:
            transport.close()
            print(f"Finish connection with {device['LAN_IP']}.")
        except Exception as e:
            print(f"Error trying to finish connection with {device['LAN_IP']}: {e}")

async def connect_to_others():
    devices = get_all_devices()
    connections = await asyncio.gather(*[connect_to_device(device) for device in devices if device])
    connections_established.extend(connections) 
