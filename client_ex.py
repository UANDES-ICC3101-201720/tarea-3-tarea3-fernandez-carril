# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 19:43:15 2018

@author: carri
"""

import socket  # Import socket module
import sys

s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.

print("Welcome to our P2P media sharing platform!")
while (True):
    print("Select your option:")
    print("1.- Find a File.")
    print("2.- Exit.")
    print("3.- Tests")
    ans = input()
    if ans == "1":
        file = input("Please, select the name of the file you want to search and download.")
        s.connect((host, port))
        rev_dec = s.recv(1024).decode()
        print(rev_dec)
        fileEncode = file.encode()
        s.send(fileEncode)
        s.close
    elif ans == "3":
        s.connect((host, port))
        filename = input("Which file do you want? (type 'q' to quit) -> ")
        if filename != 'q':
            s.send(filename.encode())
            server_resp = s.recv(1024).decode()
            if server_resp == 'EXISTS':
                file_size = int(s.recv(1024).decode())
                message = input("File Exists " + str(file_size) +
                                " Bytes, download? (y/n) -> ")
                if message == 'y':
                    f = open('d_' + filename, 'wb')
                    data = s.recv(1024)
                    totalRecv = sys.getsizeof(data)
                    f.write(data)
                    while totalRecv < file_size:
                        data = s.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                    f.close()
                    print("download successful")
        else:
            print("File doesn't exist!")
s.close()
