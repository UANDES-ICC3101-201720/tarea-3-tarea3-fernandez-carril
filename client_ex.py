import socket               # Import socket module
import threading
import os

def checkFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        response = ("EXISTS " + str(os.path.getsize(filename)))
        response = response.encode()
        sock.send(response)


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
    if (ans=="1"):
        file = input("Please, select the name of the file you want to search and download.\n")
        s.connect((host, port))
        rev_dec = s.recv(1024).decode()
        print(rev_dec)
        fileEncode = file.encode()
        s.sendall(fileEncode)
        s.send(fileEncode)
    elif (ans == "3"):
        s.connect((host, port))
        filename = input("Which file do you want? (type 'q' to quit) -> ")
        if filename != 'q':
            s.send(filename.encode())
            data = s.recv(1024)
            dec_data = data.decode()
            if dec_data[:6] == 'EXISTS':
                filesize = len(data)
                message = input("File Exists " + str(filesize) +
                                " Bytes, download? (y/n) -> ")
                if message == 'y':
                    s.send('OK'.encode())
                    f = open('d_' + filename, 'wb')
                    data = s.recv(1024)
                    totalRecv = len(data)
                    f.write(data)
                    while totalRecv < filesize:
                        data = s.recv(1024).decode()
                        totalRecv += len(data)
                        f.write(data)
                    print("download successful")
        else:
            print("File doesn't exist!")
s.close()
