import socket
import threading




class Listener(object):
    connections = []
    def __init__(self):
        self.host = ''
        self.port = 12345
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        threading.Thread(target=self.listen).start() #this is so we can listen and have execute commands from server console

    def listen(self):
        numberOfUsers = 5
        self.sock.listen(numberOfUsers)
        while True: #keep listening, start a new thread when a client connects
            client, address = self.sock.accept()
            print("\n[+]Connected to a new client at " + address[0] + ":" + str(address[1]) + "\n")
            #client.settimeout(60)
            t = threading.Thread(target = self.listenToClient,args = (client,address)).start()
            self.connections.append(address) #dont know why to do this, just seems right?

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data and (str(data.decode('ascii')).lower() != 'exit'):
                    recvData = str(data.decode('ascii')).lower()
                    print("RECIVED: " + recvData)
                    #response = self.executecommand(recvData.split())
                    response = recvData #echo the data
                    print("SENDING: " + response)
                    client.send(response.encode('ascii'))
                    #print("sent")
                else:
                    print("[+]Disconnected " + address[0] +":"+ str(address[1]))
                    raise error('Client disconnected')
            except:
                client.close()
                return False


