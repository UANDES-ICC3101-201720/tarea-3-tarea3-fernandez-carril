# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 19:43:15 2018

@author: carri
"""

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
rev_dec = s.recv(1024).decode()
print(rev_dec)
st = 'dis conect'
byt = st.encode()
s.send(byt)
s.close  