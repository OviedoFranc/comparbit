from all_devices import install_arp
from autoconfig_connections import add_host_entry, get_ip_address
import asyncio
from tracker import connect_to_others

install_arp()
add_host_entry('comparbit', f"{get_ip_address()}:37596")
asyncio.run(connect_to_others())