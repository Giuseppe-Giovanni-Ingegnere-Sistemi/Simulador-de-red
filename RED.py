import random
import socket
import threading
import time

class DHCPServer:
    def __init__(self, ip_pool_start, ip_pool_end, subnet_mask):
        self.ip_pool = self.generate_ip_pool(ip_pool_start, ip_pool_end)
        self.subnet_mask = subnet_mask
        self.leased_ips = {}

    def generate_ip_pool(self, start, end):
        start_octets = list(map(int, start.split('.')))
        end_octets = list(map(int, end.split('.')))
        ip_pool = []

        for i in range(start_octets[-1], end_octets[-1] + 1):
            ip = f"{start_octets[0]}.{start_octets[1]}.{start_octets[2]}.{i}"
            ip_pool.append(ip)
        
        return ip_pool

    def request_ip(self, mac_address):
        if mac_address in self.leased_ips:
            return self.leased_ips[mac_address]
        
        if self.ip_pool:
            assigned_ip = self.ip_pool.pop(0)
            self.leased_ips[mac_address] = assigned_ip
            print(f"Assigned IP {assigned_ip} to {mac_address}")
            return assigned_ip
        
        raise Exception("No IP addresses available")

    def release_ip(self, mac_address):
        if mac_address in self.leased_ips:
            ip = self.leased_ips.pop(mac_address)
            self.ip_pool.append(ip)
            print(f"Released IP {ip} from {mac_address}")
        else:
            print(f"{mac_address} does not have an IP to release")


class Device:
    def __init__(self, name, mac_address):
        self.name = name
        self.mac_address = mac_address
        self.ip_address = None

    def request_ip(self, dhcp_server):
        self.ip_address = dhcp_server.request_ip(self.mac_address)
    
    def release_ip(self, dhcp_server):
        dhcp_server.release_ip(self.mac_address)
        self.ip_address = None

    def send_packet(self, network, destination_ip, data):
        if self.ip_address is None:
            print(f"{self.name} does not have an IP address.")
            return
        
        print(f"{self.name} (IP: {self.ip_address}) is sending data to {destination_ip}")
        network.route_packet(self.ip_address, destination_ip, data)

    def receive_packet(self, data, source_ip):
        print(f"{self.name} (IP: {self.ip_address}) received data from {source_ip}: {data}")


class Router:
    def __init__(self, devices):
        self.devices = devices

    def route_packet(self, source_ip, destination_ip, data):
        for device in self.devices:
            if device.ip_address == destination_ip:
                print(f"Routing packet from {source_ip} to {destination_ip} via router")
                device.receive_packet(data, source_ip)
                return

        print(f"Destination IP {destination_ip} not found in routing table.")


class Network:
    def __init__(self):
        self.devices = []
        self.router = None

    def add_device(self, device):
        self.devices.append(device)

    def connect_router(self, router):
        self.router = router

    def route_packet(self, source_ip, destination_ip, data):
        if self.router:
            self.router.route_packet(source_ip, destination_ip, data)
        else:
            for device in self.devices:
                if device.ip_address == destination_ip:
                    device.receive_packet(data, source_ip)
                    return
            print(f"Device with IP {destination_ip} not found in the network.")


# Crear y configurar la red
network = Network()

# Crear el servidor DHCP
dhcp_server = DHCPServer(ip_pool_start="192.168.1.2", ip_pool_end="192.168.1.254", subnet_mask="255.255.255.0")

# Crear los dispositivos
device1 = Device(name="Device1", mac_address="00:1B:44:11:3A:B7")
device2 = Device(name="Device2", mac_address="00:1B:44:11:3A:B8")
device3 = Device(name="Device3", mac_address="00:1B:44:11:3A:B9")

# Agregar los dispositivos a la red
network.add_device(device1)
network.add_device(device2)
network.add_device(device3)

# Solicitar IPs a través del servidor DHCP
device1.request_ip(dhcp_server)
device2.request_ip(dhcp_server)
device3.request_ip(dhcp_server)

# Crear un router y conectarlo a la red
router = Router(network.devices)
network.connect_router(router)

# Simular envío de datos entre dispositivos
device1.send_packet(network, device2.ip_address, "Hello from Device1")
device2.send_packet(network, device1.ip_address, "Hello back from Device2")
device3.send_packet(network, device1.ip_address, "Device3 checking in")

# Liberar una IP
device2.release_ip(dhcp_server)
