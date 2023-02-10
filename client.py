import threading
import socket
import time, sys
alias = input('Choose a name: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 58000))


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
              client.send(alias.encode('utf-8'))
            else:
              print(message,end="\n")
        except:
            print('Error')
            client.close()
            break

 
def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))
receive_thread = threading.Thread(target = client_receive)
receive_thread.start()
send_thread = threading.Thread(target = client_send)
send_thread.start()
