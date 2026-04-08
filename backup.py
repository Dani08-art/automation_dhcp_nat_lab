# Script de backup de configuraciones AMG-Lab
# Guarda el running-config de cada dispositivo

from netmiko import ConnectHandler
from datetime import datetime
import os

# Fecha actual para nombrar los archivos
fecha = datetime.now().strftime('%Y-%m-%d')

# Crear carpeta backups si no existe
os.makedirs('backups', exist_ok=True)

# Lista de todos los dispositivos con sus datos de conexión
dispositivos = [
    {'nombre': 'R1',       'host': '192.168.80.100'},
    {'nombre': 'R2-LEFT',  'host': '10.0.12.2'},
    {'nombre': 'R3-RIGHT', 'host': '10.0.13.2'},
]

# Datos comunes de conexión
credenciales = {
    'device_type': 'cisco_ios',
    'username': 'admin',
    'password': 'cisco123',
    'secret': 'cisco123',
}

for dispositivo in dispositivos:

    datos_conexion = {**credenciales, 'host': dispositivo['host']}
    print(f"Conectando a {dispositivo['nombre']} ({dispositivo['host']})...")

    #conectamos al dispositivo
    net_connect = ConnectHandler(**datos_conexion)

    #obtenemos el running-config
    running_config = net_connect.send_command('show running-config')

    #Creamos el nombre del archivo
    nombre_archivo = f"backups/{dispositivo['nombre']}_backup_{fecha}.txt"

    #Guardamos el running-config en un archivo
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(running_config)

    print(f"Backup de {dispositivo['nombre']} guardado en {nombre_archivo}\n")

    net_connect.disconnect()

    print("\nBackup completado para todos los dispositivos.")