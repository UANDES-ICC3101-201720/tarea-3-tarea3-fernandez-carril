# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import socket               # Import socket module

print('Server started')
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print(host)
s.listen(60)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ('Got connection from', addr)
   msg = 'You are connected to the Server!'
   msg_enc = msg.encode()
   c.send(msg_enc)
   rev_dec = s.recv(1024).decode()
   print(rev_dec)
   c.close()                # Close the connection
