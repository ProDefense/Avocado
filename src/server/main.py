#!/usr/bin/env python3
# TODO: Convert CLI to CMD2
import logging
from mtls import mtls
from queue import Queue
from handler.handler import Handler


def main():
    requestq = Queue()
    handler = Handler(requestq)
    handler.start()
    listener = mtls.Listener(requestq)

    while True:
        userin = input("> ")
        userin = userin.split()

        logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
        commandStr = ' '.join(userin)
        logging.info("Command: " + commandStr)

        # Print sessions
        if len(userin) < 1:
            continue
        elif userin[0] == "sessions":
            for id in listener.sessions.list():
                print(id)
        elif userin[0] == "use":
            if len(userin) == 2:
                conn, addr = listener.sessions.get(userin[1])
                print(f"Using session with {addr}")
                mtls.session(conn)


if __name__ == "__main__":
    main()
