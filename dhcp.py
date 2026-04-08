# Configuración de DHCP centralizado y NAT en R1 utilizando Netmiko
# Configurar ip helper-address en R2 y R3 para que puedan obtener IP del DHCP de R1

# Importamos la librería Netmiko
from netmiko import ConnectHandler

# Creamos un diccionario con los datos de conexión al router R1
R1 = {
    'device_type': 'cisco_ios',
    'host': '192.168.80.100',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
}  

R2 = {
    'device_type': 'cisco_ios',
    'host': '10.0.12.2',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
}  

R3 = {
    'device_type': 'cisco_ios',
    'host': '10.0.13.2',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
}  

# Creacion de Pool DHCP
# Lista de comandos para configurar DHCP en R1
comandos_dhcp_r1 = [

    # Vlan 10
    'ip dhcp excluded-address 10.10.0.1 10.10.0.10',
    'ip dhcp pool VLAN10-VENTAS',
    'network 10.10.0.0 255.255.255.0',
    'default-router 10.10.0.1',
    'dns-server 8.8.8.8',
    'exit',

    # Vlan 20
    'ip dhcp excluded-address 10.20.0.1 10.20.0.10',
    'ip dhcp pool VLAN20-RRHH',
    'network 10.20.0.0 255.255.255.0',
    'default-router 10.20.0.1',
    'dns-server 8.8.8.8',
    'exit',

    # Vlan 30
    'ip dhcp excluded-address 10.30.0.1 10.30.0.10',
    'ip dhcp pool VLAN30-IT',
    'network 10.30.0.0 255.255.255.0',
    'default-router 10.30.0.1',
    'dns-server 8.8.8.8',
    'exit',

    # Vlan 40
      'ip dhcp excluded-address 10.40.0.1 10.40.0.10',
    'ip dhcp pool VLAN40-MGMT',
    'network 10.40.0.0 255.255.255.0',
    'default-router 10.40.0.1',
    'dns-server 8.8.8.8',
    'exit',
]

# Configuración de ip helper-address en R2 y R3
comandos_helper_r2 = [

    'interface ethernet 0/1.10',
    'ip helper-address 1.1.1.1',
    'exit',
    'interface ethernet 0/1.20',
    'ip helper-address 1.1.1.1',
    'exit',
]

comandos_helper_r3 = [

    'interface ethernet 0/1.30',
    'ip helper-address 1.1.1.1',
    'exit',
    'interface ethernet 0/1.40',
    'ip helper-address 1.1.1.1',
    'exit',
] 

# Nos conectamos al router R1 utilizando el diccionario de conexión
print("Conectando al router R1...")
connection_r1 = ConnectHandler(**R1)
# Entramos al modo privilegiado
connection_r1.enable()

# Ejecutamos los comandos de configuración DHCP en R1
print("\nConfigurando DHCP en R1...")
output_dhcp_r1 = connection_r1.send_config_set(comandos_dhcp_r1)
print(output_dhcp_r1) 

connection_r1.disconnect()
print("DHCP configurado en R1. Conexión cerrada.")

# Nos conectamos al router R2 utilizando el diccionario de conexión
print("\nConectando al router R2...")
connection_r2 = ConnectHandler(**R2)
# Entramos al modo privilegiado
connection_r2.enable()

# Ejecutamos los comandos de configuración ip helper-address en R2
print("\nConfigurando ip helper-address en R2...") 
output_helper_r2 = connection_r2.send_config_set(comandos_helper_r2)
print(output_helper_r2)

connection_r2.disconnect()
print("ip helper-address configurado en R2. Conexión cerrada.")

# Nos conectamos al router R3 utilizando el diccionario de conexión
print("\nConectando al router R3...")
connection_r3 = ConnectHandler(**R3)
# Entramos al modo privilegiado
connection_r3.enable()

# Ejecutamos los comandos de configuración ip helper-address en R3
print("\nConfigurando ip helper-address en R3...")
output_helper_r3 = connection_r3.send_config_set(comandos_helper_r3)
print(output_helper_r3)

connection_r3.disconnect()
print("ip helper-address configurado en R3. Conexión cerrada.")

#Guardamos la configuración de DHCP y ip helper-address en un archivo de texto

routers = [R1, R2, R3]
print("\nGuardando configuraciones en los routers...")
for dispositivo in routers:
        conexion = ConnectHandler(**dispositivo)
        conexion.enable()
        conexion.send_command('write memory')
        conexion.disconnect()

print("Configuraciones guardadas en todos los routers")
print("Script finalizado.")

