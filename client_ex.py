import socket  # Import socket module
import sys
import os
import threading
import queue


def send_message(connection, message):
    try:
        connection.sendall(message)
    except socket.error:
        sys.exit(-1)


def peer_function(connection, address):
    """
    connect to a peer

    connection : connection socket
    address : (IP_address, port)
    """
    global sharing_directory

    incoming_buffer = ""

    while True:
        # parse message
        while "\0" not in incoming_buffer:
            incoming_buffer += connection.recv(4096)

        index = incoming_buffer.index("\0")
        message = incoming_buffer[0:index-1]
        incoming_buffer = incoming_buffer[index+1:]

        fields = message.split()
        command = fields[0]
        # handle and respond to the message
        if command == "GIVE":
            file_ = sharing_directory + "/" + fields[1]

            if os.path.isfile(file_):
                # get the file size
                file_size = os.path.getsize(file_)
                send_message(connection, "TAKE {}\n\0".format(str(file_size)))
                file__ = open(file_, "rb")
                file_buffer = ""
                file_buffer = file__.read(1024)
                while file_buffer:
                    print("sending: " + file_buffer)
                    connection.send(file_buffer)
                    file_buffer = file__.read(1024)
                file__.close()
            else:
                send_message(connection, "ERROR\n\0")
                connection.close()
                break

        elif command == "THANKS":
            connection.close()
            break

        else:
            send_message(connection, "ERROR\n\0")
            connection.close()
            break

    return


def listen(listening_ip, listening_port, queue):
    """
    create a server socket and start listening for incoming connections
    """
    try:
        listening_socket = socket.socket()
    except socket.error:
        sys.exit(-1)

    try:
        listening_socket.bind((listening_ip, listening_port))
    except socket.error:
        sys.exit(-1)
    # listen for incoming connections
    listening_socket.listen(5)
    # cli_output
    listening_port = listening_socket.getsockname()[1]
    # pass the listening_ip and listening_port to the main thread
    queue.put((listening_ip, listening_port))
    # handle incoming peer connections
    peer_counter = 0
    while True:
        connection, address = listening_socket.accept()

        peer_thread = threading.Thread(name="peer {}".format(peer_counter),
                target=peer_function, args=(connection, address))
        peer_thread.daemon = True
        peer_thread.start()
        peer_counter += 1


s = socket.socket()  # Create a socket object
host = socket.gethostname()  # Get local machine name
port = 12345  # Reserve a port for your service.
listening_ip = socket.gethostbyname()
listening_port = 0
sharing_directory = os.path.dirname(os.path.abspath(__file__)) + "\\sharing"
files_list = [file_ for file_ in os.listdir(sharing_directory) if os.path.isfile(os.path.join(sharing_directory, file_))]
print("Welcome to our P2P media sharing platform!")
inc_buffer = ""
s.connect(host, port)
s.send("NEW")
s.recv()
queue = queue.Queue()
listening_thread = threading.Thread(name="ListeningThread", target=listen,
            args=(listening_ip, listening_port, queue))
listening_thread.daemon = True
listening_thread.start()
listening_ip, listening_port = queue.get()
listening_message = "LISTENING {} {}\n\0".format(listening_ip, listening_port)
send_message(s, listening_message)
converse(server, incoming_buffer, "LISTENING")
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
