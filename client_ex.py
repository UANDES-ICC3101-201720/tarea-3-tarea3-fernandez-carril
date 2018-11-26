import socket               # Import socket module
import threading
import os

def checkFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        response = ("EXISTS " + str(os.path.getsize(filename)))
        response = response.encode()
        sock.send(response)


s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345                # Reserve a port for your service.

print("Welcome to our P2P media sharing platform!")
while(True):
    print("Select your option:")
    print("1.- Find a File.")
    print("2.- Exit.")
    ans = input()
    if (ans=="1"):
        file = input("Please, select the name of the file you want to search and download.\n")
        s.connect((host, port))
        rev_dec = s.recv(1024).decode()
        print(rev_dec)
        fileEncode = file.encode()
        s.sendall(fileEncode)
    if (ans=="2"):
        break


