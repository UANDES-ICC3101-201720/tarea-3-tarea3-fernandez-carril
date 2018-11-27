import socket  # Import socket module
import sys
import queue
import threading
import os

file_list = []
requested_file = ""


def codedSend(connection, message):
    message = message.encode()
    try:
        connection.sendall(message)
    except socket.error:
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

    if order == "ENTER":
        print("You succesfully joined the server")

        return None, msg_buffer

    elif order == "FULLLIST" and command == "FILE_LIST":
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

    elif order == "OK" and command in ("FILES", "LISTEN"):
        return None, msg_buffer

    elif order == "DATA" and command == "PEER":
        peer_ip = field[1]
        peer_port = int(field[2])

        return(peer_ip, peer_port), msg_buffer

    elif order == "ERROR":
        sys.exit(-1)
    else:
        sys.exit(-1)


def send_message(connection, message):
    message = message.encode()
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
port = 45000  # Reserve a port for your service.
listening_ip = socket.gethostname()
listening_port = 0
sharing_directory = os.path.dirname(os.path.abspath(__file__)) + "\\sharing"
files_list = [file_ for file_ in os.listdir(sharing_directory) if os.path.isfile(os.path.join(sharing_directory, file_))]
print("Welcome to our P2P media sharing platform!")
inc_buffer = ""
s.connect((host, port))
s.send("NEW\n\0".encode())
unneeded, inc_buffer = talk(s, inc_buffer, "NEW")
queue = queue.Queue()
listening_thread = threading.Thread(name="ListeningThread", target=listen,
            args=(listening_ip, listening_port, queue))
listening_thread.daemon = True
listening_thread.start()
listening_ip, listening_port = queue.get()
listening_message = "LISTEN {} {}\n\0".format(listening_ip, listening_port)

send_message(s, listening_message)
talk(s, inc_buffer, "LISTEN")
print("Server is correctly listening")


list_message = "FILES {}\n".format(len(files_list))
for file in files_list:
    list_message += file + "\n"
list_message += "\0"
send_message(s, list_message)
talk(s, inc_buffer, "FILES")
print("Server received file info")

send_message(s, "FILE_LIST " + "\n\0")
talk(s, inc_buffer, "FILE_LIST")

while True:
        print()
        print("options:")
        print("1: SENDLIST : request the list of clients and shared files")
        print("2: WHERE : request the IP address and port of the specified client")
        print("5: QUIT : exit the program")

        option = input()
        if option in ["1", "sendlist", "SENDLIST"]:
            send_message(s, "SENDLIST " + "\n\0")

            talk(s, inc_buffer, "SENDLIST")

        elif option in ["2", "where", "WHERE"]:
            print("Enter the username of the client:")

            client = input()

            print("{} is an invalid client username, try again: ".format(client))

            send_message(s, "WHERE " + client + "\n\0")

            (peer_ip, peer_port), incoming_buffer = talk(s, inc_buffer, "WHERE")

            peer = connection_init( (peer_ip, peer_port) )

            give_me(peer)

        elif option in ["5", "quit", "QUIT"]:
            sys.exit(0)

        else:
            print("invalid option, try again")


