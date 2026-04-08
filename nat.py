# Configuración de NAT

# Importamos la librería Netmiko
from netmiko import ConnectHandler

# Creamos un diccionario con los datos de conexión al router R1
R1 = {
    'device_type': 'cisco_ios',
    'host': '192.168.80.100',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
    'timeout': 60,          # ← agrega esta línea
    'auth_timeout': 60,     # ← y esta línea
}  

# Lista de comandos para configurar NAT en R1

comandos_acl_r1 = [

    # ACL que define qué redes van a hacer NAT
    'ip access-list standard ACL-NAT',
    'permit 10.10.0.0 0.0.0.255',
    'permit 10.20.0.0 0.0.0.255',
    'permit 10.30.0.0 0.0.0.255',
    'permit 10.40.0.0 0.0.0.255',
    'exit',

]

comandos_nat_r1 = [

    # Definir interfaces inside y outside
    'interface ethernet 0/0',
    'ip nat inside',
    'exit',
    'interface ethernet 0/2',
    'ip nat inside',
    'exit',
    'interface ethernet 0/1',
    'ip nat inside',
    'exit',
    'interface ethernet 0/3',
    'ip nat outside',
    'exit',

    # Configurar NAT overload
    'ip nat inside source list ACL-NAT interface ethernet 0/3 overload',

]

#Conectamos al router R1 y ejecutamos los comandos de configuración de NAT
print("Conectando a R1 y configurando NAT...")
net_connect = ConnectHandler(**R1)
net_connect.enable()

resulado_acl = net_connect.send_config_set(comandos_acl_r1,read_timeout=60)
print(resulado_acl)

resultado_nat = net_connect.send_config_set(comandos_nat_r1,read_timeout=60)  
print(resultado_nat)

#Guardamos la configuración
print("Guardando configuración en R1...")
net_connect = ConnectHandler(**R1)
net_connect.enable()
net_connect.send_command('write memory')
net_connect.disconnect()
print("Configuración guardada en R1.")
print("NAT configurado correctamente en R1.")