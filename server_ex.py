import socket            
import threading
import sys


client_list = {} # {nickname: {files: [files], listening_ip: listening IP address, listening_port: listening port}}
clients = {}  # {(IP_address, port): nickname}
client_num = 0

def codedSend(connection, message):
    message = message.encode()
    try:
        connection.sendall(message)
    except socket.error:
        sys.exit(-1)


def talk(connection, address, msg_buffer, command):

  global client_list
  global clients
  global client_num

  if "\0" not in msg_buffer:
    return "", msg_buffer
  else:
    index = msg_buffer.index("\0")
    message = msg_buffer[0:index-1]
    msg_buffer = msg_buffer[index+1:]

  line = message.split("\n")
  field = line[0].split()
  order = field[0]

  #Client gets a nickname and has its data saved.
  if order == "NEW":
    nickname = "client_{}".format(client_num)
    client_list[nickname] = {"files": [], "listening_ip": "", "listening_port": None}
    clients[address] = nickname

    codedSend(connection, "ENTER\n\0")
    return msg_buffer, "ENTER"

  #Saves the ip and port  
  elif order == "LISTEN":
    print(client_list[clients[address]]["listening_ip"])
    client_list[clients[address]]["listening_ip"] = field[1]
    client_list[clients[address]]["listening_port"] = field[2]

    codedSend(connection, "OK\n\0")
    return msg_buffer, "OK"

  #Saves list of available files  
  elif  order == "FILES":
    total = int(field[1])
    if total != (len(line) - 1):
      codedSend(connection, "ERROR\n\0")
      sys.exit(-1)
    else:
      client_list[clients[address]]["files"] = line[1:]

    codedSend(connection, "OK\n\0")
    return msg_buffer, "OK"

  elif order == "FILE_LIST":
    count = 0
    for client in client_list:
      count += len(client_list[client]["files"])
    msg = "FULLLIST {}\n".format(str(count))
    for client in client_list:
      for file in client_list[client]["files"]:
        msg += str(client) + " " + str(file) + "\n"
    msg += "\0"

    codedSend(connection, msg)
    return talk(connection, address, msg_buffer, "FULLLIST")

  elif order == "PEER":
    peer = field[1]

    if peer in client_list:
      peer_ip = client_list[peer]["listening_ip"]
      peer_port = client_list[peer]["listening_port"]


      msg = "DATA {} {}\n\0".format(peer_ip, peer_port)

      codedSend(connection, msg)
      return msg_buffer, "PEER"
    else:
      codedSend(connection, "EMPTY\n\0")
      return msg_buffer, "EMPTY"
  elif order == "ERROR":
    sys.exit(-1)


def client_function(connection, address):

  msg_buffer = ""
  command = ""

  while True:
    incoming = connection.recv(4096)
    incoming = incoming.decode()
    if len(incoming) == 0:
      break
    else:
      msg_buffer += incoming
    msg_buffer, command = talk(connection, address, msg_buffer, command)


def main():
  
  global client_list
  global clients
  global client_num

  host = "MSI" #Cambiar al adecuado
  port = 45000 #Cambiar al adecuado

  try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  except socket.error:
    sys.exit(-1)

  try:
    server_socket.bind( (host, port) )
  except socket.error:
    sys.exit(-1)

  print('Server started')
  server_socket.listen(5)
  while True:
    connection, address = server_socket.accept()

    # create a thread that runs the client_function
    client_thread = threading.Thread(name="client {}".format(client_num),
            target=client_function, args=(connection, address))

    client_thread.daemon = True
    client_thread.start()
    client_num += 1


if __name__ == "__main__":
  main()