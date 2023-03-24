#!/usr/bin/env python3
# TODO: Convert CLI to CMD2
import logging
from console import console
from mtls import mtls
# from compile.generate import generate
from queue import Queue
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

    logging.basicConfig(filename="Command Log.txt", level=logging.INFO)

    console.console(obj=listener)


if __name__ == "__main__":
    main()
