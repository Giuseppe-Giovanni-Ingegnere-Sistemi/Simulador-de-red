# Simulación de Red con Servidor DHCP y Enrutamiento

Este proyecto simula una red simple con un servidor DHCP que asigna direcciones IP a dispositivos, y un router que gestiona el enrutamiento de paquetes entre los dispositivos. La simulación incluye la solicitud de IPs, el envío de datos entre dispositivos y la liberación de IPs.

## Características

- **Servidor DHCP:** Asigna dinámicamente direcciones IP a los dispositivos en función de sus direcciones MAC.
- **Dispositivos:** Pueden solicitar y liberar direcciones IP del servidor DHCP, así como enviar y recibir datos en la red.
- **Router:** Gestiona el enrutamiento de paquetes entre los dispositivos de la red.
- **Red:** Administra los dispositivos y el enrutamiento de los paquetes.

## Estructura del Código

### Clases Principales

- **DHCPServer:**
  - `__init__(ip_pool_start, ip_pool_end, subnet_mask)`: Inicializa el servidor DHCP con un rango de IPs y una máscara de subred.
  - `generate_ip_pool(start, end)`: Genera un pool de direcciones IP.
  - `request_ip(mac_address)`: Asigna una dirección IP a un dispositivo basado en su dirección MAC.
  - `release_ip(mac_address)`: Libera una dirección IP previamente asignada.

- **Device:**
  - `__init__(name, mac_address)`: Inicializa un dispositivo con un nombre y una dirección MAC.
  - `request_ip(dhcp_server)`: Solicita una dirección IP al servidor DHCP.
  - `release_ip(dhcp_server)`: Libera la dirección IP asignada.
  - `send_packet(network, destination_ip, data)`: Envía un paquete de datos a otro dispositivo en la red.
  - `receive_packet(data, source_ip)`: Recibe un paquete de datos desde otro dispositivo.

- **Router:**
  - `__init__(devices)`: Inicializa el router con una lista de dispositivos conectados.
  - `route_packet(source_ip, destination_ip, data)`: Enruta un paquete desde un dispositivo fuente a un dispositivo destino.

- **Network:**
  - `__init__()`: Inicializa la red.
  - `add_device(device)`: Agrega un dispositivo a la red.
  - `connect_router(router)`: Conecta un router a la red.
  - `route_packet(source_ip, destination_ip, data)`: Enruta paquetes dentro de la red.

## Ejecución

1. **Crear y Configurar la Red:**
   - Crear una instancia de `Network`.
   - Crear un servidor DHCP con un rango de IPs definido.
   
2. **Agregar Dispositivos:**
   - Crear instancias de `Device` y agregarlas a la red.
   - Solicitar IPs para cada dispositivo usando el servidor DHCP.
   
3. **Enrutamiento de Paquetes:**
   - Crear un `Router` y conectarlo a la red.
   - Enviar paquetes de datos entre los dispositivos.

4. **Liberar IPs:**
   - Los dispositivos pueden liberar sus IPs cuando ya no las necesiten.

## Ejemplo de Uso

```python
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
````
