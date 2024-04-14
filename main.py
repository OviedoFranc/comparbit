from all_devices import install_arp
from autoconfig_connections import add_host_entry, get_ip_address
import asyncio
from tracker import connect_to_others, open_listening_socket, close_connections

local_address = get_ip_address()
port = 37596

get_ip_address()
add_host_entry('comparbit', f"{local_address}:{port}")
open_listening_socket(local_address, port)
asyncio.run(connect_to_others())

# close_connections() 