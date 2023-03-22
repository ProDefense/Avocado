#!/usr/bin/env python3
import threading
from listener.listener import Listener
from queue import Queue

# handle new implants
def implantHandler(implantq):
    while True:
        new_implant = implantq.get()

        if new_implant:
            print("New implant connected!")
            # do whatever with the new implant

        else:
            break

# handle new session connections
def sessionHandler(sessionq, listener, output_received, session_closed):
    while True:
        new_session = sessionq.get()

        if new_session:
            print(f"Connected to session {new_session.addr}")
            session_closed.clear()
            output_received.set() 
            threading.Thread(target=inputHandler, args=(listener, output_received, session_closed, "Session")).start()

        else:
            break

# prints output messages received from the server
def outputHandler(outputq, output_received):
    while True:
        output = outputq.get()

        if not output:
            break

        else:
            print(output)

        output_received.set() 

def inputHandler(listener, output_received, session_closed, title):
    while True:
        output_received.wait()
        if (title=="Avocado"):
            session_closed.wait()

        msg = input(f"[{title}] > ")

        if not msg:
            continue

        output_received.clear()  
        listener.send(msg)

        if msg.lower() == "exit":
            print(f"[+]{title} Terminated")
            break

    session_closed.set()

def main():
    # TODO prompt the user to enter host/port instead
    hostname = "127.0.0.1"
    port = 12345

    implantq = Queue()
    sessionq = Queue()
    outputq = Queue()

    listener = Listener(hostname, port, outputq, implantq, sessionq)

    # output_received and session_closed are workarounds for some i/o issues
    # e.g. the server response overwrites the user input prompt
    output_received = threading.Event()  
    session_closed = threading.Event()  
    output_received.set()  
    session_closed.set()  

    threading.Thread(target=implantHandler, args=(implantq,)).start()
    threading.Thread(target=sessionHandler, args=(sessionq,listener, output_received, session_closed)).start()
    threading.Thread(target=outputHandler, args=(outputq, output_received)).start()
    threading.Thread(target=inputHandler, args=(listener, output_received, session_closed, "Avocado")).start()

if __name__ == '__main__':
    main()
