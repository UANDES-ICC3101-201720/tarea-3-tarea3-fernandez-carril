# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 19:43:15 2018

@author: carri
"""

import socket               # Import socket module

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
        file = input("Please, select the name of the file you want to search and download.")
        s.connect((host, port))
        rev_dec = s.recv(1024).decode()
        print(rev_dec)
        fileEncode = file.encode()
        s.send(fileEncode)
        s.close



