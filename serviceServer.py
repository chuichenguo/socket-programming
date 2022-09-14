import socket

SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

print('Welecome! Please input domain name.')
clientMessage = input()
# utf-8
client.sendall(clientMessage.encode())

while True:
    serverMessage = client.recv(1024)
    print("Server :", serverMessage.decode())
    print('Welecome! Please input domain name.')
    clientMessage = input()
    # utf-8
    client.sendall(clientMessage.encode())
    if clientMessage == 'bye':
        break
client.close()
