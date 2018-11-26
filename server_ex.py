# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import socket
import threading
import os

def RetrFile (name, sock):
    filename = sock.recv(1024).decode()
    if os.path.isfile(filename):
        sock.send(("EXISTS " + str(os.path.getsize(filename))).encode())
        userResponse = sock.recv(1024).decode()
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR".encode())

    sock.close()



print('Server started')
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print(host)
s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()
    print ("client connected ip: " + str(addr))
    file_thread = threading.Thread(target=RetrFile, args=("retrThread", c))
    file_thread.start()
s.close()
