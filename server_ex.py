import socket               # Import socket module
import threading

def checkForFile(name, sock):
   flag = False
   filename = sock.recv().decode()
   for client in clients:
      client.send(filename)
      data = client.recv(1024).decode()
      if data[:6] == 'EXISTS':
         flag = True
         filesize = long(data[6:])
         filesize = filesize.encode()
         sock.send(filesize)
         break
   if not flag:
      message = "ERROR"
      message = message.encode()
      sock.send(message)



clients = []

print('Server started')
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(60)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print ('Got connection from', addr)
   msg = 'You are connected to the Server!'
   msgEncode = msg.encode()
   c.send(msgEncode)
   clients.append(c)
   t = threading.Thread(target=checkForFile, args=("retrThread", c))
   c.close()                # Close the connection
