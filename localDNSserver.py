import socket
import threading
import json
# http://net-informations.com/python/net/thread.htm


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from: ", clientAddress)
        FIFOIP = []
        FIFODomainName = []
        LRUIP = []
        LRUDomainName = []
        serviceServerMessage = ''
        serverMessage = ''
        # read json file local_DNS_data
        with open('local_DNS_data_example.json') as file:
            local_DNS_data = json.load(file)
        # LRU
        for i in range(len(local_DNS_data)):
            if i >= 5:
                break
            LRUIP.append(local_DNS_data[i]["ip_address"])
            LRUDomainName.append(local_DNS_data[i]["domain_name"])
        print(LRUIP)
        print(LRUDomainName)

        # FIFO
        # for i in range(len(local_DNS_data)):
        #     if i >= 5:
        #         break
        #     FIFOIP.append(local_DNS_data[i]["ip_address"])
        #     FIFODomainName.append(local_DNS_data[i]["domain_name"])
        # print(FIFOIP)
        # print(FIFODomainName)

        while True:
            data = self.clientSocket.recv(2048)
            serviceServerMessage = data.decode()
            if serviceServerMessage == 'bye':
                break
            print("Service server: ", serviceServerMessage)
            for i in range(len(LRUDomainName)):
            # for i in range(len(FIFODomainName)):
                if serviceServerMessage == LRUDomainName[i]:
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
                    self.clientSocket.sendall(serverMessage.encode())
                    break
                else:
                    serverMessage = "Not found."
                # if serviceServerMessage == FIFODomainName[i]:
                #     serverMessage = FIFOIP[i]
                #     # FIFO
                #     tempDomainName = FIFODomainName[i]
                #     FIFODomainName.remove(tempDomainName)
                #     FIFODomainName.append(tempDomainName)
                #     tempIP = FIFOIP[i]
                #     FIFOIP.remove(tempIP)
                #     FIFOIP.append(tempIP)
                #     print(FIFOIP)
                #     print(FIFODomainName)
                #     self.clientSocket.sendall(serverMessage.encode())
                #     break
                # else:
                #     serverMessage = "Not found."
            if serverMessage == "Not found.":
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((LOCALHOST, 8000))
                askRoot = serviceServerMessage
                client.sendall(askRoot.encode())
                RootMessage = client.recv(2048)
                RootMessage = RootMessage.decode()
                if RootMessage != "Not found.":
                    # LRU
                    LRUDomainName.pop()
                    LRUDomainName.insert(0, serviceServerMessage)
                    LRUIP.pop()
                    LRUIP.insert(0, RootMessage)
                    print(LRUIP)
                    print(LRUDomainName)

                    # FIFO
                    # FIFODomainName.pop(0)
                    # FIFODomainName.append(serviceServerMessage)
                    # FIFOIP.pop(0)
                    # FIFOIP.append(RootMessage)
                    # print(FIFOIP)
                    # print(FIFODomainName)

                self.clientSocket.sendall(RootMessage.encode())
        print("Service server at ", clientAddress, " disconnected.")


LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Local DNS server started!")
print("Waiting for service server.")
while True:
    server.listen(5)
    clientSocket, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientSocket)
    newthread.start()
