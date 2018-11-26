import socket               # Import socket module
import threading
import os
import sys
import Queue
from threading import Thread

file_list = []
requested_file = ""


def codedSend(connection, message):
    message = message.encode()
    try:
        connection.sendall(message)
    except socket.error:
        logging.error("error, send_message")
        sys.exit(-1)



def talk(server, msg_buffer, command):
    global file_list
    global requested_file

    if "\0" not in msg_buffer:
        msg_buffer += server.recv(4096).decode()
        return talk(server, msg_buffer, command)
    else:
        index = msg_buffer.index("\0")
        message = msg_buffer[0:index-1]
        msg_buffer = msg_buffer[index+1:]

    line = message.split("\n")
    field = line[0].split()
    order = field[0]

    if order == "NEW":
        print("You succesfully joined the server")

        return None, msg_buffer

    elif order == "FULLLIST" and command == "SENDLIST":
        count = int(field[1])

        if count != (len(line) - 1):
            codedSend(server, "ERROR\n\0")
            sys.exit(-1)
        else:
            file_list = line[1:]

            print("FILE LIST:")
            for l in line[1:]:
                print(str(l))

        return None, msg_buffer

    elif order == "OK" and command in ("LIST", "LISTENING"):
        return None, msg_buffer

    elif order == "DATA" and command == "PEER":
        peer_ip = field[1]
        peer_port = int(field[2])

        return(peer_ip, peer_port), msg_buffer

    elif order == "ERROR":
        sys.exit(-1)
    else:
        sys.exit(-1)

