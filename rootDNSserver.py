import socket
import threading
import json


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientsocket
        print("\nNew connection added: ", clientAddress)

    def run(self):
        localDNSMessage = ''
        serverMessage = ''
        LRUIP = []
        LRUDomainName = []
        alias = []
        canonicalName = []
        with open('root_DNS_data.json') as file:
            root_DNS_data = json.load(file)
        # LRU
        for i in range(len(root_DNS_data)):
            if root_DNS_data[i]["type"] == 'A':
                LRUIP.append(root_DNS_data[i]["ip_address"])
                LRUDomainName.append(root_DNS_data[i]["domain_name"])
            elif root_DNS_data[i]["type"] == 'CNAME':
                alias.append(root_DNS_data[i]["alias"])
                canonicalName.append(root_DNS_data[i]["canonical name"])
        print(LRUIP)
        print(LRUDomainName)
        # print(alias)
        # print(canonicalName)

        data = self.clientSocket.recv(2048)
        localDNSMessage = data.decode()
        print("Local DNS server: ", localDNSMessage)

        # alias to canonical name
        for i in range(len(alias)):
            if localDNSMessage == alias[i]:
                localDNSMessage = canonicalName[i]
        # find
        for i in range(len(LRUDomainName)):
            if localDNSMessage == LRUDomainName[i]:
                serverMessage = LRUIP[i]
                # LRU
                tempDomainName = LRUDomainName[i]
                LRUDomainName.remove(tempDomainName)
                LRUDomainName.insert(0, tempDomainName)
                tempIP = LRUIP[i]
                LRUIP.remove(tempIP)
                LRUIP.insert(0, tempIP)
                print(LRUIP)
                print(LRUDomainName)
                break
            else:
                serverMessage = "Not found."
        self.clientSocket.sendall(serverMessage.encode())
        print("Local DNS server ", clientAddress, " disconnected.\n")


LOCALHOST = "127.0.0.1"
PORT = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Root DNS server started!")
print("Waiting for local DNS server.")
while True:
    server.listen(5)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
