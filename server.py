import threading
import socket
import time, sys
host = '127.0.0.1'
port = 58000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []
clients_ID =[]


def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle clients'connections
def handle_client(client):
    while True :
        try:
           message = client.recv(1024).decode('utf-8')
           if 'alias?' in message :
             for x in range(len(aliases)) :
               client.send(aliases[x].encode('utf-8'))
           elif 'id' in message :
             for x in clients_ID :
               client.send(str(x).encode('utf-8'))
           elif 'private' in message :
             private(client, message)
           elif 'group' in message :
             private_group(clients, message)
           elif 'file' in message :
             open_file(message)
           else:
            broadcast(message.encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            clients_ID.remove(clients_ID[index])
            break
# Main function to receive the clients connection

def private(client, message):
   name = message.split(" ")
   name1 = name[2]
   index = aliases.index(name1)
   clients[index].send(message.encode('utf-8'))    
   
def private_group(clients, message):
   names = message.split(" ")
   for i in range(2, len(names)) :
     name1 = names[i]
     if name1 not in aliases:
       break
     index = aliases.index(name1)
     clients[index].send(message.encode('utf-8'))


def receive():
    i =0
    while True:
        print('Server is listening ...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        clients_ID.append(i)
        i+=1
        
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
def open_file(message):
         name = message.split(" ")
         file_name = name[2]
         with open(file_name,'r') as f:
          lines = f.read()
         broadcast(lines.encode('utf-8'))


if __name__=="__main__":
    receive()