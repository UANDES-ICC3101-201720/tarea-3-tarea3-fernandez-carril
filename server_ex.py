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

s.listen(60)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ('Got connection from', addr)
   msg = 'Thank you for connecting'
   msg_enc = msg.encode()
   c.sendto(msg_enc, ())
   s.listen(1)
   conn, addr = s.accept()
   data = conn.recv(2000)
   data.decode()
   print(data)
   c.close()                # Close the connection
